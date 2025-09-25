# carbon_neutrality_model/analysis.py

import numpy as np
from .model import PlanningProblem_alpha
from .solver_2phase import solve_model
import copy


def run_scenarios(pp: PlanningProblem_alpha, scenarios, solver_params):
    """
    运行定义好的一系列情景。
    此函数处理从 solver.py 返回的 (vectors..., success_flag) 格式的数据。
    """
    results = {}

    # 从 initial_conditions 获取 c0 和 k0 的基础值
    # 注意：某些分析（如k0敏感性）可能会覆盖这些值
    base_c0 = solver_params.get('c0', 600000.0)
    base_k0 = solver_params.get('k0', 4500000.0)
    T = solver_params['T']

    print("正在运行情景模拟...")
    for sc in scenarios:
        label = sc['label']
        print(f"  --> 正在运行: {label}")

        # 设置模型的技术参数
        pp.α, pp.θr, pp.θc, pp.θf, pp.η = sc["α"], sc["θr"], sc["θc"], sc["θf"], sc["η"]

        # 允许情景定义覆盖初始条件，这对于敏感性分析至关重要
        current_k0 = sc.get('k0', base_k0)
        current_c0 = sc.get('c0', base_c0)

        # 从 solver 获取结果，包含一个成功标志
        *res_vecs, success = solve_model(
            pp=pp,
            c0_guess=current_c0,
            k0=current_k0,
            λTN1_guess=solver_params['λTN10_guess'],
            T=T,
            tol=solver_params['tol'],
            max_iter=solver_params['max_iter']
        )

        if success:
            results[label] = {
                'y_vec': res_vecs[0], 'c_vec': res_vecs[1], 'I_vec': res_vecs[2], 'k_vec': res_vecs[3],
                'Ir_vec': res_vecs[4], 'Ic_vec': res_vecs[5], 'If_vec': res_vecs[6]
            }
        else:
            print(f"  警告: 情景 '{label}' 模拟失败，已跳过。")

    print("情景模拟完成！")
    return results


def run_theta_sensitivity(pp: PlanningProblem_alpha, base_scenario, solver_params, theta_config, theta_type='f', multipliers=None):
    """
    运行对某个theta参数的敏感性分析。
    构造好情景集以后，通过调用run_scenarios实现
    """
    print(f"\n开始运行技术参数 {theta_type.upper()} 敏感性分析...")
    if multipliers is None:
        multipliers = [0.5, 1.0, 2.0, 4.0]

    config = theta_config[theta_type]
    param_key = config['param_key']
    multipliers = config['multipliers']
    base_theta_value = base_scenario[param_key]

    scenarios_to_run = []
    for m in multipliers:
        new_theta_value = base_theta_value * m
        # 创建一个新的情景字典，继承基础情景的参数，并更新目标参数
        new_scenario = {
            **base_scenario,  # 继承基础情景的所有设置
            "label": f"{config['label_prefix']}={new_theta_value:.6f} (x{m})",
            param_key: new_theta_value
        }
        scenarios_to_run.append(new_scenario)

    # 直接调用 run_scenarios 函数来执行这一系列构造好的情景
    return run_scenarios(pp, scenarios_to_run, solver_params)


def run_k0_sensitivity(pp: PlanningProblem_alpha, base_scenario, solver_params, k0_values, c0_ratio, base_k0_for_scaling):
    """
    运行对初始资本(k0)的敏感性分析。
    通过构造一系列情景，并调用 run_scenarios 来实现。
    """
    print(f"\n开始运行初始资本 K0 敏感性分析...")

    scenarios_to_run = []

    for k0_val in k0_values:
        # 1. 为每个 k0 值计算相应的情景参数
        c0_val = pp.f(k0_val) * c0_ratio
        label = f"k0 = {k0_val:,.0f}"

        # 2. 创建一个新的情景字典，继承基础情景的参数
        #    并用当前循环的值覆盖 k0, c0, 和 k_ter。
        new_scenario = {
            **base_scenario,  # 继承基础情景的所有设置
            "label": label,
            "k0": k0_val,            # 覆盖初始资本
            "c0": c0_val            # 覆盖初始消费猜测值
        }
        scenarios_to_run.append(new_scenario)

    return run_scenarios(pp, scenarios_to_run, solver_params)


def run_alpha_sensitivity(pp: PlanningProblem_alpha, base_scenario, solver_params, alpha_config):
    """
    运行对alpha参数的敏感性分析。
    构造好情景集以后，通过调用run_scenarios实现
    """
    print(f"\n开始运行技术参数alpha敏感性分析...")

    config = alpha_config
    param_key = config['param_key']
    multipliers = config['multipliers']
    base_alpha_value = base_scenario[param_key]

    scenarios_to_run = []
    for m in multipliers:
        new_alpha_value = base_alpha_value * m
        # 创建一个新的情景字典，继承基础情景的参数，并更新目标参数
        new_scenario = {
            **base_scenario,  # 继承基础情景的所有设置
            "label": f"{config['label_prefix']}={new_alpha_value:.6f} (x{m})",
            param_key: new_alpha_value
        }
        scenarios_to_run.append(new_scenario)

    # 直接调用 run_scenarios 函数来执行这一系列构造好的情景
    return run_scenarios(pp, scenarios_to_run, solver_params)


def run_theta_2d_sensitivity(pp, base_scenario, solver_params, theta_config, theta_type_1, theta_type_2, z_variable_name, grid_size=5):
    """
    对两个 Theta 参数进行二维敏感性分析，生成一个结果网格。
    此函数直接调用求解器，而不是通过 run_scenarios。
    """
    # 1. 从配置中获取两个theta参数的详细信息
    config1 = theta_config[theta_type_1]
    config2 = theta_config[theta_type_2]
    param_key1 = config1['param_key']  # e.g., 'θc'
    param_key2 = config2['param_key']  # e.g., 'θf'

    # 2. 创建参数扫描的范围
    # 使用配置中定义的 min 和 max (如果存在)，否则基于 base_scenario 的值创建范围
    min_val_1 = config1.get('min', base_scenario[param_key1] * 0.4)
    max_val_1 = config1.get('max', base_scenario[param_key1] * 1.5)
    min_val_2 = config2.get('min', base_scenario[param_key2] * 0.4)
    max_val_2 = config2.get('max', base_scenario[param_key2] * 1.5)

    theta1_vals = np.linspace(min_val_1, max_val_1, grid_size)
    theta2_vals = np.linspace(min_val_2, max_val_2, grid_size)

    # 3. 初始化用于存储结果的Z轴网格
    z_grid = np.full((grid_size, grid_size), np.nan)  # Initialize with NaN

    # 4. 创建变量名到求解器返回向量索引的映射
    # 顺序必须与 solve_model 的返回顺序一致
    vec_to_idx = {
        'y_vec': 0, 'c_vec': 1, 'I_vec': 2, 'k_vec': 3,
        'Ir_vec': 4, 'Ic_vec': 5, 'If_vec': 6
    }
    if z_variable_name not in vec_to_idx:
        print(f"错误: Z轴变量 '{z_variable_name}' 无效。")
        return theta1_vals, theta2_vals, z_grid
    z_idx = vec_to_idx[z_variable_name]

    print(f"\n开始进行 {grid_size}x{grid_size} 网格敏感性分析 ({param_key1} vs {param_key2})...")
    total_sims = grid_size * grid_size

    # 5. 遍历网格，运行模拟
    for i, val1 in enumerate(theta1_vals):
        for j, val2 in enumerate(theta2_vals):
            print(f"  --> 正在运行模拟 {i * grid_size + j + 1} / {total_sims}...")

            # 创建当前模拟的参数副本
            current_scenario = copy.deepcopy(base_scenario)
            current_scenario[param_key1] = val1
            current_scenario[param_key2] = val2

            # 设置模型的技术参数
            pp.α, pp.θr, pp.θc, pp.θf, pp.η = (
                current_scenario["α"], current_scenario["θr"],
                current_scenario["θc"], current_scenario["θf"], current_scenario["η"]
            )

            # 运行模型求解 (与 run_scenarios 中的调用方式保持一致)
            *res_vecs, success = solve_model(
                pp=pp,
                c0_guess=solver_params['c0'],
                k0=solver_params['k0'],
                λTN1_guess=solver_params['λTN10_guess'],
                T=solver_params['T'],
                tol=solver_params['tol'],
                max_iter=solver_params['max_iter']
            )

            if success:
                # 提取所需变量向量的最后一个值
                result_vector = res_vecs[z_idx]
                z_grid[i, j] = result_vector[-1]
            else:
                # 求解失败，该点值保持为 NaN
                print(f"  警告: 模拟失败于 {param_key1}={val1:.4f}, {param_key2}={val2:.4f}")

    print("网格敏感性分析完成。")
    return theta1_vals, theta2_vals, z_grid
