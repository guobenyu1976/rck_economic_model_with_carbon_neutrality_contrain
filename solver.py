# carbon_neutrality_model/solver.py

import numpy as np
from numba import jit
from .model import PlanningProblem_alpha, neu_ability
import pandas as pd

@jit
def shooting(pp: PlanningProblem_alpha, c0, k0, T, λTN1=0.01):
    """
    根据初始猜测值，计算T期内的经济路径。
    """
    if c0 > pp.f(k0) + (1 - pp.δ) * k0 or c0 <= 0: # 增加 c0 > 0 的检查
        # 返回一个明确的“失败”元组，而不是 None
        # 所有数组都用 NaN 填充，长度与成功时一致
        nan_vec_T1 = np.full(T + 1, np.nan)
        nan_vec_T2 = np.full(T + 2, np.nan)
        return nan_vec_T1, nan_vec_T1, nan_vec_T2, nan_vec_T2, nan_vec_T2, nan_vec_T2, False  # 添加一个失败标志

    y_vec = np.empty(T + 1)
    c_vec = np.empty(T + 1)
    k_vec = np.empty(T + 2)
    Ir_vec = np.empty(T + 2)
    Ic_vec = np.empty(T + 2)
    If_vec = np.empty(T + 2)

    y_vec[0] = pp.f(k0)
    c_vec[0] = c0
    k_vec[0] = k0
    Ir_vec[0], Ic_vec[0], If_vec[0] = pp.c_to_Ir_Ic_If(c0, λTN1)

    for t in range(T):
        y_next, c_next, Ir_next, Ic_next, If_next, k_next = pp.next_y_c_Ir_Ic_If_k(c_vec[t], k_vec[t], λTN1)
        if not np.isfinite(k_next) or k_next < 0:  # 增加对路径中资本的检查
            nan_vec_T1 = np.full(T + 1, np.nan)
            nan_vec_T2 = np.full(T + 2, np.nan)
            return nan_vec_T1, nan_vec_T1, nan_vec_T2, nan_vec_T2, nan_vec_T2, nan_vec_T2, False

        y_vec[t + 1], c_vec[t + 1], Ir_vec[t + 1], Ic_vec[t + 1], If_vec[t + 1], k_vec[t + 1] = y_next, c_next, Ir_next, Ic_next, If_next, k_next

    A, β, δ, α = pp.A, pp.β, pp.δ, pp.α
    factor = (β * (A + 1 - δ)) ** (1 / α)
    Ir_vec[T + 1] = Ir_vec[T] * factor
    Ic_vec[T + 1] = Ic_vec[T] * factor
    If_vec[T + 1] = If_vec[T] * factor
    k_vec[T + 1] = k_vec[T] * (A + 1 - δ) - (c_vec[T] + Ir_vec[T + 1] + Ic_vec[T + 1] + If_vec[T + 1])

    return y_vec, c_vec, k_vec, Ir_vec, Ic_vec, If_vec, True  # 添加一个成功标志


@jit
def bisection(pp: PlanningProblem_alpha, c0, k0, T, λTN1, k_ter, tol=1e-3, max_iter=500):
    """
    一重循环：寻找c0以满足期末资本约束k_ter。
    """
    c0_upper = pp.f(k0) + (1 - pp.δ) * k0
    c0_lower = 0.0

    current_c0 = c0
    for i in range(max_iter):
        res = shooting(pp, current_c0, k0, T, λTN1)

        # 使用布尔标志来判断成功与否
        y_vec, c_vec, k_vec, Ir_vec, Ic_vec, If_vec, success = res

        if not success:
            # 如果 shooting 失败，通常是因为 c0 太高，我们降低上界
            c0_upper = current_c0
            current_c0 = (c0_lower + c0_upper) / 2
            continue

        error = k_vec[-1] - k_ter    # 需要删除k_ter

        if np.abs(error) < tol:
            return y_vec, c_vec, k_vec, Ir_vec, Ic_vec, If_vec, True

        if error > 0:
            c0_lower = current_c0
        else:
            c0_upper = current_c0
        current_c0 = (c0_lower + c0_upper) / 2

    # 如果循环结束仍未收敛，返回最后一次成功或失败的结果
    return res


# @jit
def solve_model(pp: PlanningProblem_alpha, c0_guess, k0, λTN1_guess, T, k_ter, tol=1e-6, max_iter=500):
    """
    二重循环：寻找λTN1以满足期末碳中和约束。
    """
    λTN1_upper = 100.0
    λTN1_lower = 0.0
    λTN1 = λTN1_guess

    num_res = []
    for i in range(max_iter):
        res = bisection(pp, c0_guess, k0, T, λTN1, k_ter)

        y_vec, c_vec, k_vec, Ir_vec, Ic_vec, If_vec, success = res

        print(k_vec[-1], c_vec[-1], λTN1)
        num_res.append([k_vec[-1], c_vec[-1], λTN1])

        if not success:
            λTN1_upper = λTN1
            λTN1 = (λTN1_lower + λTN1_upper) / 2
            continue

        ability_Ir = neu_ability(pp.θr, pp.α, Ir_vec)
        ability_Ic = neu_ability(pp.θc, pp.α, Ic_vec)
        ability_If = neu_ability(pp.θf, pp.α, If_vec)
        ability_k = pp.η * k_vec[T + 1]
        error = ability_k - (ability_Ir + ability_Ic + ability_If)

        if np.abs(error) < tol:
            df = pd.DataFrame(num_res, columns=['期末资本', '期末消费', 'lamda T+1'])
            df.to_excel('期末状态求解.xlsx', index=False, sheet_name='期末数据')
            print("output was done")
            return y_vec, c_vec, k_vec, Ir_vec, Ic_vec, If_vec, True

        if error > 0:
            λTN1_lower = λTN1
        else:
            λTN1_upper = λTN1
        λTN1 = (λTN1_lower + λTN1_upper) / 2


    return res


