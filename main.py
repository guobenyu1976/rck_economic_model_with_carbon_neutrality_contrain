# carbon_neutrality_model/main.py

import matplotlib.pyplot as plt
import numpy as np
from . import config
from .config import MODEL_DEFAULT
from .model import PlanningProblem_alpha
from . import analysis
from . import plotting
from . import utils


# ----------------------------------------------------------------------------
# 任务1: 主要情景分析
# ----------------------------------------------------------------------------
def task_1_main_scenarios(pp, solver_params):
    """运行主要情景分析并绘图"""
    print("--- 正在执行任务1: 主要情景分析 ---")

    # 模拟
    main_results = analysis.run_scenarios(pp, config.SCENARIOS, solver_params)

    # print(main_results)
    utils.export_results_to_excel(
        results_data=main_results,
        filename='main_scenarios_results.xlsx',
        start_year=config.START_YEAR
    )

    # 绘图
    plotting.plot_2d_scenarios(config.START_YEAR, config.SCENARIOS, main_results)
    plotting.plot_2d_scenarios_inv(config.START_YEAR, config.SCENARIOS, main_results)
    plotting.plot_3d_scenarios(
        results_data=main_results,
        variable_info={'vec_name': 'c_vec', 'title': '各情景下消费的演化路径', 'z_label': '消费 (C)'},
        scenarios_list=config.SCENARIOS,
        start_year=config.START_YEAR
    )
    plotting.plot_3d_scenarios(
        results_data=main_results,
        variable_info={'vec_name': 'If_vec', 'title': '各情景下森林碳汇的演化路径', 'z_label': '森林碳汇 (If)'},
        scenarios_list=config.SCENARIOS,
        start_year=config.START_YEAR
    )
    print("--- 任务1 完成 ---\n")


# ----------------------------------------------------------------------------
# 任务2: k0 (初始资本) 敏感性分析
# ----------------------------------------------------------------------------
def task_2_k0_sensitivity(pp,  solver_params):
    """运行并绘制 k0 敏感性分析"""
    print("--- 正在执行任务2: 初始资本 (k0) 敏感性分析 ---")

    k_config = config.RIB_CONFIG['If']
    print(k_config)
    # 定义参数
    k0_values = np.linspace(solver_params['k0'] * 0.8, solver_params['k0'] * 1.2, num=6)
    base_scenario_for_k0 = config.SCENARIOS[2]
    initial_c_to_y_ratio = solver_params['c0'] / (pp.A * solver_params['k0'])

    # 模拟
    k0_results = analysis.run_k0_sensitivity(
        pp=pp, base_scenario=base_scenario_for_k0,
        solver_params=solver_params,
        k0_values=k0_values, c0_ratio=initial_c_to_y_ratio,
        base_k0_for_scaling=solver_params['k0']
    )

    # 绘图
    if k0_results:
        k0_scenarios = [{'label': label} for label in k0_results.keys()]
        plot_variable_info = {
            'vec_name': k_config['vec_key'], 'title': '初始资本 (k0) 变化的影响', 'z_label': k_config['inv_name']
        }
        plotting.plot_3d_k0_ribbons(
            results_for_k0=k0_results, scenarios_for_k0=k0_scenarios,
            start_year=config.START_YEAR, plot_info=plot_variable_info
        )
    else:
        print("k0 敏感性分析没有成功的模拟结果可供绘图。")
    print("--- 任务2 完成 ---\n")


# ----------------------------------------------------------------------------
# 任务3: Theta 敏感性分析
# ----------------------------------------------------------------------------
def task_theta_sensitivity(pp, solver_params, theta_type):
    """运行并绘制 Theta 敏感性分析"""
    theta_name_map = {'r': '碳减排技术', 'c': 'CCS技术', 'f': '森林碳汇技术'}
    print(f"--- 正在执行任务:  {theta_name_map[theta_type]} (Theta_{theta_type}) 敏感性分析 ---")

    # 模拟
    theta_results = analysis.run_theta_sensitivity(
        pp=pp, base_scenario=config.SCENARIOS[2],
        solver_params=solver_params,
        theta_config=config.THETA_CONFIG, theta_type=theta_type
    )

    # 绘图
    if theta_results:
        theta_config = config.THETA_CONFIG[theta_type]
        plot_info = {
            'vec_key': theta_config['vec_key'],
            'title': f"不同{theta_config['param_name']}对{theta_config['inv_name']}路径的影响",
            'y_label': theta_config['inv_name']
        }
        plotting.plot_2d_sensitivity_paths(
            start_year=config.START_YEAR, results_data=theta_results, plot_info=plot_info
        )

        plot_info = {
            'vec_key': 'y_vec',
            'title': f"不同{theta_config['param_name']}对总产出路径的影响",
            'y_label': '总产出'
        }
        plotting.plot_2d_sensitivity_paths(
            start_year=config.START_YEAR, results_data=theta_results, plot_info=plot_info
        )
    else:
        print("Theta 敏感性分析没有成功的模拟结果可供绘图。")

    utils.export_results_to_excel(
        results_data=theta_results,
        filename='theta_results.xlsx',
        start_year=config.START_YEAR
    )

    print(f"--- 任务 Theta_{theta_type} 完成 ---\n")


# ----------------------------------------------------------------------------
# 任务6: 2D 主要情景分析
# ----------------------------------------------------------------------------
def task_6_main_scenarios(pp, solver_params):
    """运行主要情景分析并绘图"""
    print("--- 正在执行任务1: 主要情景分析 ---")

    # 模拟
    main_results = analysis.run_scenarios(pp, config.SCENARIOS, solver_params)

    # print(main_results)
    utils.export_results_to_excel(
        results_data=main_results,
        filename='main_scenarios_results.xlsx',
        start_year=config.START_YEAR
    )

    # 绘图
    plotting.plot_2d_1_scenario(config.START_YEAR, config.SCENARIOS, main_results)
    print("--- 任务6 完成 ---\n")


# ----------------------------------------------------------------------------
# 任务7: alpha 敏感性分析
# ----------------------------------------------------------------------------
def task_alpha_sensitivity(pp, solver_params):
    """运行并绘制 alpha 敏感性分析"""
    print(f"--- 正在执行任务:  alpha 敏感性分析 ---")

    # 模拟
    alpha_results = analysis.run_alpha_sensitivity(
        pp=pp, base_scenario=config.SCENARIOS[2],
        solver_params=solver_params,
        alpha_config=config.ALPHA_CONFIG
    )

    # 绘图
    if alpha_results:
        alpha_config = config.ALPHA_CONFIG
        plot_info = {
            'vec_key': alpha_config['vec_key'],
            'title': f"不同alpha对{alpha_config['inv_name']}路径的影响",
            'y_label': alpha_config['inv_name']
        }
        plotting.plot_2d_sensitivity_paths(
            start_year=config.START_YEAR, results_data=alpha_results, plot_info=plot_info
        )
    else:
        print("alpha 敏感性分析没有成功的模拟结果可供绘图。")

    utils.export_results_to_excel(
        results_data=alpha_results,
        filename='alpha_results.xlsx',
        start_year=config.START_YEAR
    )

    print(f"--- 任务 alpha 完成 ---\n")


# ----------------------------------------------------------------------------
# 任务8: 双 Theta 参数二维曲面敏感性分析
# ----------------------------------------------------------------------------
def task_8_theta_2d_surface_sensitivity(pp, solver_params):
    """对两个 Theta 参数进行二维敏感性分析并绘制 3D 曲面图"""
    print("--- 正在执行任务8: 双 Theta 参数二维曲面敏感性分析 ---")

    # ----- 在这里配置你的分析 -----
    theta_type_1 = 'c'  # X轴参数, 可选 'r', 'c', 'f'
    theta_type_2 = 'f'  # Y轴参数, 可选 'r', 'c', 'f'
    grid_size = 10       # 网格密度 (5x5, 10x10, etc.)

    # Z轴变量配置, 你可以取消注释来选择不同的变量
    # z_variable_info = {
    #     'vec_name': 'Ic_vec',        # 模型中变量向量的名称
    #     'title_name': 'CCS投资',     # 在图表标题中显示的名称
    #     'label': 'Ic'                # 在Z轴上显示的标签
    # }
    z_variable_info = {
        'vec_name': 'If_vec',
        'title_name': '森林碳汇投资',
        'label': 'If'
    }

    # 1. 运行模拟
    theta1_vals, theta2_vals, z_grid = analysis.run_theta_2d_sensitivity(
        pp=pp,
        base_scenario=config.SCENARIOS[2],  # 使用第三个情景作为基础
        solver_params=solver_params,
        theta_config=config.THETA_CONFIG,
        theta_type_1=theta_type_1,
        theta_type_2=theta_type_2,
        z_variable_name=z_variable_info['vec_name'],
        grid_size=grid_size
    )

    # 2. 准备绘图信息并绘图
    # 检查是否有任何有效的(非NaN)模拟结果
    if np.any(np.isfinite(z_grid)):
        theta_info_1 = config.THETA_CONFIG[theta_type_1]
        theta_info_2 = config.THETA_CONFIG[theta_type_2]

        plotting.plot_3d_theta_surface(
            theta1_vals=theta1_vals,
            theta2_vals=theta2_vals,
            z_grid=z_grid,
            theta_info_1=theta_info_1,
            theta_info_2=theta_info_2,
            z_info=z_variable_info
        )
    else:
        print("二维 Theta 敏感性分析没有成功的模拟结果可供绘图。")

    print(f"--- 任务8 完成 ---\n")


def main(task_id):
    """
    主执行函数，根据 task_id 执行特定任务。
    """
    # 1. 初始化模型实例和加载参数 (所有任务共享)
    print("初始化模型并加载配置...")
    ini_model_param = MODEL_DEFAULT
    pp = PlanningProblem_alpha(ini_model_param)
    solver_params = {**config.SOLVER_PARAMS, 'T': config.T}

    tasks_executed = False

    # 2. 任务调度
    if task_id == 1:
        task_1_main_scenarios(pp, solver_params)
        tasks_executed = True
    elif task_id == 2:
        task_2_k0_sensitivity(pp, solver_params)
        tasks_executed = True
    elif task_id == 3:
        task_theta_sensitivity(pp, solver_params, 'r')
        tasks_executed = True
    elif task_id == 4:
        task_theta_sensitivity(pp, solver_params, 'c')
        tasks_executed = True
    elif task_id == 5:
        task_theta_sensitivity(pp, solver_params, 'f')
        tasks_executed = True
    elif task_id == 6:
        task_6_main_scenarios(pp, solver_params)
        tasks_executed = True
    elif task_id == 7:
        task_alpha_sensitivity(pp, solver_params)
        tasks_executed = True
    elif task_id == 8:
        task_8_theta_2d_surface_sensitivity(pp, solver_params)
        tasks_executed = True
    else:
        print(f"错误: 无效的任务编号 '{task_id}'。请输入 1-5 之间的数字来运行任务。")

    # 3. 显示所有生成的图像
    if tasks_executed:
        print("所有选定任务的绘图已生成，正在显示...")
        plt.show()

    print('程序结束')


if __name__ == "__main__":
    # ========================================================================
    # ==                                                                    ==
    # ==              在此处修改数字以选择要运行的模拟与绘图任务                    ==
    # ==                                                                    ==
    # ==    1: 主要情景分析 (3个情景，1个2D对比图，2个3D跨情景对比图)                 ==
    # ==    2: 初始资本 k0 敏感性分析 3D (1个图)                                 ==
    # ==    3: 碳减排技术 Theta_r 敏感性分析 2D (1个图)                           ==
    # ==    4: CCS技术 Theta_c 敏感性分析 2D (1个图)                           ==
    # ==    5: 森林碳汇技术 Theta_f 敏感性分析 2D (1个图)                         ==
    # ==    6: 单个情景，多个变量 2D (1个图)                                    ==
    # ==    7: 碳中和技术 alpha 敏感性分析 2D (1个图)                           ==
    # ==    8: 双Theta参数 (c vs f) 二维曲面敏感性分析 3D (1个图)               ==
    # ==                                                                    ==
    # ========================================================================

    main(8)
