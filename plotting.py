# carbon_neutrality_model/plotting.py

from matplotlib.patches import Patch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D

import config
from .config import PLOT_ALL_V


# 一次性设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def plot_3d_scenarios(results_data, variable_info, scenarios_list, start_year):
    """
    绘制一个变量在多个情景下的三维演化路径图。
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    vec_name = variable_info['vec_name']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    legend_handles = []
    ribbon_width = 0.3

    for i, sc in enumerate(scenarios_list):
        label = sc["label"]
        data_vec = results_data[label][vec_name]
        years = np.arange(start_year, start_year + len(data_vec))
        values = data_vec

        y_bottom = i - ribbon_width / 2
        y_top = i + ribbon_width / 2
        X = np.array([years, years])
        Z = np.array([values, values])
        Y = np.array([[y_bottom] * len(years), [y_top] * len(years)])

        color = colors[i % len(colors)]
        ax.plot_surface(X, Y, Z, color=color, alpha=0.85, edgecolor='k', linewidth=0.3)
        legend_handles.append(Patch(color=color, label=label))

    ax.set_xlabel('年份 (Year)', fontsize=12)
    ax.set_zlabel(variable_info['z_label'], fontsize=12, labelpad=15)
    ax.set_title(variable_info['title'], fontsize=16, weight='bold')
    ax.set_yticks(range(len(scenarios_list)))
    ax.set_yticklabels([sc['label'] for sc in scenarios_list], rotation=15, ha='right', fontsize=9)
    ax.zaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.view_init(elev=25, azim=-135)
    ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(0.9, 1))
    plt.subplots_adjust(right=0.8)


def plot_2d_scenarios(start_year, scenarios, results):
    """
    绘制多个变量在多个情景下的2D对比图。
    """
    fig, axs = plt.subplots(2, 3, figsize=(16, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for i, sc in enumerate(scenarios):
        label = sc["label"]
        res = results[label]
        years_c = np.arange(start_year, start_year + len(res['c_vec']))
        years_k = np.arange(start_year, start_year + len(res['k_vec']))

        axs[0, 0].plot(years_c, res['y_vec'], label=label, color=colors[i])
        axs[0, 1].plot(years_c, res['I_vec'], label=label, color=colors[i])
        axs[0, 2].plot(years_c, res['c_vec'], label=label, color=colors[i])
        # axs[0, 2].plot(years_k, res['k_vec'], label=label, color=colors[i])
        axs[1, 0].plot(years_k, res['Ir_vec'], label=f'Ir {label}', color=colors[i])
        axs[1, 1].plot(years_k, res['Ic_vec'], label=f'Ic {label}', color=colors[i])
        axs[1, 2].plot(years_k, res['If_vec'], label=f'If {label}', color=colors[i])

    """
    在格式化坐标轴和标题。
    """
    axs[0, 0].set(title='产出（GDP、Y）')
    axs[0, 1].set(title='生产性投资(I)')
    axs[0, 2].set(title='消费 (C)')
    axs[1, 0].set(title='Reduction Investment (Ir)')
    axs[1, 1].set(title='CCS Investment (Ic)')
    axs[1, 2].set(title='Forest Investment (If)')

    formatter = ticker.StrMethodFormatter('{x:,.0f}')
    for ax in axs.flat:
        ax.legend()
        ax.set_xlabel('Year')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.yaxis.set_major_formatter(formatter)

    # CCS的值太小了，需要单独格式化一下
    axs[1, 1].set_ylim(-5, 100)

    fig.suptitle('2D Scenario Comparison', fontsize=16, weight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.96])


def plot_2d_scenarios_inv(start_year, scenarios, results):
    """
    绘制多个变量在多个情景下的2D对比图。
    """
    fig, axs = plt.subplots(2, 3, figsize=(14, 6))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for i, sc in enumerate(scenarios):
        label = sc["label"]
        res = results[label]
        years_c = np.arange(start_year, start_year + len(res['c_vec']))
        years_k = np.arange(start_year, start_year + len(res['k_vec']))

        axs[0, i].plot(years_c, res['y_vec'], label=label, color=colors[i])
        axs[0, i].plot(years_c, res['I_vec'], label=label, color=colors[i])
        axs[0, i].plot(years_c, res['c_vec'], label=label, color=colors[i])
        axs[1, i].plot(years_k, res['Ir_vec'], label=f'Ir {label}', color=colors[i])
        axs[1, i].plot(years_k, res['Ic_vec'], label=f'Ic {label}', color=colors[i])
        axs[1, i].plot(years_k, res['If_vec'], label=f'If {label}', color=colors[i])

    """
    在格式化坐标轴和标题。
    """
    axs[0, 0].set(title='情景1')
    axs[0, 1].set(title='情景2')
    axs[0, 2].set(title='情景3')
    axs[1, 0].set(title='情景1')
    axs[1, 1].set(title='情景2')
    axs[1, 2].set(title='情景3')

    formatter = ticker.StrMethodFormatter('{x:,.0f}')
    for ax in axs.flat:
        ax.legend()
        ax.set_xlabel('Year')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.yaxis.set_major_formatter(formatter)

    # CCS的值太小了，需要单独格式化一下
    axs[1, 1].set_ylim(-10, 5000)

    fig.suptitle('2D Scenario Comparison', fontsize=16, weight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.96])


def plot_3d_k0_ribbons(results_for_k0, scenarios_for_k0, start_year, plot_info):
    """
    绘制因初始资本(k0)变化而导致的变量路径变化的3D带状图。
    此函数只负责绘图，接收已经模拟好的数据。
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    vec_name_to_plot = plot_info['vec_name']
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(scenarios_for_k0)))
    legend_handles = []
    ribbon_width = 0.7

    for i, sc in enumerate(scenarios_for_k0):
        label = sc["label"]
        if label not in results_for_k0: continue

        data_vec = results_for_k0[label][vec_name_to_plot]
        years = np.arange(start_year, start_year + len(data_vec))
        values = data_vec

        y_bottom = i - ribbon_width / 2
        y_top = i + ribbon_width / 2

        X = np.array([years, years])
        Z = np.array([values, values])
        Y = np.array([[y_bottom] * len(years), [y_top] * len(years)])

        color = colors[i]
        ax.plot_surface(X, Y, Z, color=color, alpha=0.9, edgecolor='k', linewidth=0.3)
        legend_handles.append(Patch(color=color, label=label))

        ax.set_xlabel('年份 Year', fontsize=12, labelpad=10)
        ax.set_ylabel('初始资本 k0', fontsize=12, labelpad=5)
        ax.set_zlabel(plot_info['z_label'], fontsize=12, labelpad=15)
        ax.set_title(plot_info['title'], fontsize=16, weight='bold')
        ax.set_yticks(range(len(scenarios_for_k0)))
        #  ax.set_yticklabels([sc['label'] for sc in scenarios_for_k0], rotation=-45, ha='left', va='top', fontsize=9)
        ax.set_yticklabels([])
        ax.zaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        ax.tick_params(axis='z', which='major', pad=10)
        ax.view_init(elev=10, azim=-135)
        ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(0.06, 0.85),  fontsize=12)
        fig.tight_layout()


def plot_2d_sensitivity_paths(start_year, results_data, plot_info):
    """
    绘制一个通用的2D图，展示敏感性分析中某个变量的演化路径。

    Args:
        start_year (int): 模拟的起始年份。
        results_data (dict): 存储不同情景模拟结果的字典。
        plot_info (dict): 包含绘图所需元信息的字典，例如:
            {
                'vec_key': 'If_vec',          # 要绘制的数据向量的键
                'title': '敏感性分析标题',  # 图表标题
                'y_label': 'Y轴标签'          # Y轴标签
            }
    """
    # 从 plot_info 字典中解包绘图信息
    vec_key = plot_info.get('vec_key', 'c_vec') # 默认绘制消费
    plot_title = plot_info.get('title', '演化路径分析')
    y_label = plot_info.get('y_label', '数值')

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots(figsize=(5, 5))

    colors = plt.cm.viridis(np.linspace(0, 0.8, len(results_data)))

    for i, (label, data) in enumerate(results_data.items()):
        if vec_key in data:
            print(label)
            data_vec = data[vec_key]
            years = np.arange(start_year, start_year + len(data_vec))
            ax.plot(years, data_vec, label=label, color=colors[i], linewidth=2.5)

    ax.set_title(plot_title, fontsize=14, weight='bold')
    ax.set_xlabel('年份 Year', fontsize=14)
    ax.set_ylabel(y_label, fontsize=14)
    ax.legend(fontsize=18)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    formatter = ticker.StrMethodFormatter('{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)

    fig.tight_layout()


def plot_2d_1_scenario(start_year, scenarios, results):
    """
    绘制多个变量在1个情景下的2D对比图。
    """
    fig, axs = plt.subplots(1, 3, figsize=(16, 5))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    label = scenarios[2]["label"]
    res = results[label]
    years_c = np.arange(start_year, start_year + len(res['c_vec']))
    years_k = np.arange(start_year, start_year + len(res['k_vec']))

    """
    在axs[0]单独绘制多个变量在情景3下的2D对比图。
    """
    axs[0].plot(years_c, res['y_vec'], label=config.PLOT_ALL_V['y_label'], color=colors[0])
    axs[0].plot(years_c, res['c_vec'], label=config.PLOT_ALL_V['c_label'], color=colors[1])
    axs[0].plot(years_c, res['I_vec'], label=config.PLOT_ALL_V['I_label'], color=colors[2])
    axs[0].set(title='碳中和约束下各变量路径图')

    """
    在axs[1]单独绘制多个变量在情景3下的2D对比图。
    """
    label = scenarios[2]["label"]
    res = results[label]
    axs[1].plot(years_k, res['Ir_vec'], label=config.PLOT_ALL_V['Ir_label'], color=colors[0])
    axs[1].plot(years_k, res['Ic_vec'], label=config.PLOT_ALL_V['Ic_label'], color=colors[1])
    axs[1].plot(years_k, res['If_vec'], label=config.PLOT_ALL_V['If_label'], color=colors[2])
    axs[1].set(title='碳中和约束下各碳中和技术投资路径图')

    """
    在axs[2]单独绘制多个变量在情景3下的2D对比图。
    """
    label = scenarios[2]["label"]
    res = results[label]
    axs[2].plot(years_k, res['k_vec'], label=config.PLOT_ALL_V['k_label'], color=colors[0])
    axs[2].set(title='碳中和约束下资本路径图')

    """
    在格式化坐标轴和标题。
    """
    formatter = ticker.StrMethodFormatter('{x:,.0f}')
    for ax in axs.flat:
        ax.legend(fontsize=14)
        ax.set_xlabel('Year')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.yaxis.set_major_formatter(formatter)

    fig.suptitle('2D Scenario Comparison', fontsize=16, weight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.96])


def plot_3d_theta_surface(theta1_vals, theta2_vals, z_grid, theta_info_1, theta_info_2, z_info):
    """
    绘制两个 Theta 参数敏感性分析的 3D 曲面图。
    """
    # 1. 创建网格坐标
    X, Y = np.meshgrid(theta1_vals, theta2_vals)

    # 2. 创建 3D 图形
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # 3. 绘制曲面图
    # z_grid 的维度 (i, j) 对应 (theta1, theta2)。
    # meshgrid 创建的 X, Y 维度对应 (theta2, theta1)。
    # 因此，需要对 z_grid 进行转置 (.T) 以匹配 X 和 Y 的坐标。
    surf = ax.plot_surface(X, Y, z_grid.T, cmap='viridis', edgecolor='none', antialiased=True)

    # 4. 设置坐标轴标签和标题
    ax.set_xlabel(f"{theta_info_1['param_name']} ", fontsize=16, labelpad=15)
    ax.set_ylabel(f"{theta_info_2['param_name']} ", fontsize=16, labelpad=15)
    ax.set_zlabel(f" {z_info['label']}", fontsize=16, labelpad=20)
    # zmin = np.nanmin(z_grid)
    # zmax = np.nanmax(z_grid)
    # ax.set_zlim(zmin * 0.98, zmax * 1.02)

    title_str = (f"最后一期 {z_info['title_name']} 对 "
                 f"{theta_info_1['param_name']} 和 {theta_info_2['param_name']} 的敏感性")
    ax.set_title(title_str, fontsize=16, weight='bold', pad=20)

    # 5. 添加颜色条
    fig.colorbar(surf, shrink=0.6, aspect=10, label=f"值")

    # 6. 格式化坐标轴
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.4f'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.4f'))
    ax.zaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)
    ax.zaxis.set_tick_params(labelsize=14)
    ax.set_xticks(np.linspace(X.min(), X.max(), 5))
    ax.set_yticks(np.linspace(Y.min(), Y.max(), 5))
    ax.zaxis.set_tick_params(labelsize=14, pad=10)

    # 7. 调整视角和布局
    ax.view_init(elev=15, azim=20)
    plt.tight_layout()


