# carbon_neutrality_model/model.py

import numpy as np


class PlanningProblem_alpha:
    """
    定义了碳中和经济模型的核心动态方程和效用/生产函数。
    """
    def __init__(self, model_param):
        """
        使用一个包含所有模型参数的字典来初始化模型。
        """
        self.β = model_param.get('β')
        self.δ = model_param.get('δ')
        self.α = model_param.get('α')
        self.A = model_param.get('A')
        # 技术参数先缺省设置，运行时从外部情景进行设置
        self.θr = model_param.get('θr')
        self.θc = model_param.get('θc')
        self.θf = model_param.get('θf')
        self.η = model_param.get('η')

    def u(self, c):
        return np.log(c)

    def u_prime(self, c):
        return c ** (-1)

    def f(self, k):
        return self.A * k

    def f_prime(self, k):
        return self.A

    def c_to_Ir_Ic_If(self, c, λTN1):
        α = self.α
        θr, θc, θf = self.θr, self.θc, self.θf
        Ir = (λTN1 * θr * c) ** (1 / α)
        Ic = (λTN1 * θc * c) ** (1 / α)
        If = (λTN1 * θf * c) ** (1 / α)
        return Ir, Ic, If

    def next_y_c_I_Ir_Ic_If_k(self, c, k, λTN1):
        A, β, δ = self.A, self.β, self.δ
        c_next = c * β * (A + 1 - δ)
        Ir_next, Ic_next, If_next = self.c_to_Ir_Ic_If(c_next, λTN1)
        k_next = k * (A + 1 - δ) - (c_next + Ir_next + Ic_next + If_next)
        I_next = k_next - k * (1 - δ)
        y_next = self.f(k_next)
        return y_next, c_next, I_next, Ir_next, Ic_next, If_next, k_next


def neu_ability(θ, α, I_rcf_vec):
    """
    计算给定投资路径下的碳中和能力。
    """
    powered_I_rcf_vec = (I_rcf_vec ** (1 - α)) / (1 - α)
    sum_of_powers = np.sum(powered_I_rcf_vec)
    ability_I_rcf = θ * sum_of_powers
    return ability_I_rcf
