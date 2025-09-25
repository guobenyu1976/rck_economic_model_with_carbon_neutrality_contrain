# carbon_neutrality_model/config.py

# 模拟基本参数
START_YEAR = 2020
T = 40  # 模拟时长


# 模型缺省参数
MODEL_DEFAULT = {
    'β': 0.95,
    'δ': 0.10,
    'α': 0.30,  # 0.3	0.25~0.35
    'A': 0.25,  # 0.25	0.2~0.3
    'θr': 0.0054,  # 0.0054	0.0018~0.0900
    'θc': 0.0033,  # 0.0033	0.0011~0.0055
    'θf': 0.0167,  # 0.0167	0.0055~0.0278
    'η': 0.000003
}

# 求解器参数
SOLVER_PARAMS = {
    'c0': 600000.0,
    'k0': 4500000.0,  # k0 应该挪到model那里去。k0不属于求解的内容，是模型的设定
    'λTN10_guess': 0.001,
    'tol': 1e-5,
    'max_iter': 50
}

# 主要情景定义 情景的做法就是，先load基础config，然后用情景overwrite这些参数
SCENARIOS = [
    {"label": "情景1 Scenario1", "θr": 100.0, "θc": 100.0, "θf": 100.0, "η": 0.0000001, "α": 0.30},
    {"label": "情景2 Scenario2", "θr": 0.0054, "θc": 0.000001, "θf": 0.000001, "η": 0.000003, "α": 0.30},
    {"label": "情景3 Scenario3", "θr": 0.0054, "θc": 0.0033, "θf": 0.0167, "η": 0.000003, "α": 0.30}
]

# 主要情景定义
PLOT_ALL_V = {
    "y_label": "产出 Output",
    "c_label": "消费 Consumption",
    "I_label": "投资 Investment",
    "k_label": "生产性资本 Productive Capital",
    "Ir_label": "碳减排 Carbon Reduction",
    "Ic_label": "CCS CCS",
    "If_label": "森林碳汇 Forest Carbon Sink",
}

# 技术参数敏感性分析配置
THETA_CONFIG = {
    'r': {'param_key': 'θr', 'multipliers': [0.4, 0.7, 1.0, 2.0], 'vec_key': 'Ir_vec', 'param_name': 'θr', 'inv_name': 'Ir', 'label_prefix': 'θr'},
    'c': {'param_key': 'θc', 'multipliers': [0.4, 0.7, 1.0, 2.0], 'vec_key': 'Ic_vec', 'param_name': 'θc', 'inv_name': 'Ic', 'label_prefix': 'θc'},
    'f': {'param_key': 'θf', 'multipliers': [0.4, 0.7, 1.0, 2.0], 'vec_key': 'If_vec', 'param_name': 'θf', 'inv_name': 'If', 'label_prefix': 'θf'}
}

# 技术参数敏感性分析配置
RIB_CONFIG = {
    'y': {'param_key': 'y', 'vec_key': 'y_vec',  'inv_name': 'y'},
    'c': {'param_key': 'c', 'vec_key': 'c_vec',  'inv_name': 'c'},
    'I': {'param_key': 'I', 'vec_key': 'I_vec',  'inv_name': 'I'},
    'Ir': {'param_key': 'Ir', 'vec_key': 'Ir_vec', 'inv_name': 'Ir'},
    'Ic': {'param_key': 'Ic', 'vec_key': 'Ic_vec', 'inv_name': 'Ic'},
    'If': {'param_key': 'If', 'vec_key': 'If_vec', 'inv_name': 'If'},
}



# 技术替代弹性敏感性分析配置
ALPHA_CONFIG = {
    'param_key': 'α',
    'vec_key': 'y_vec',
    'param_name': 'α',
    'inv_name': 'y',
    'label_prefix': 'α',
    'multipliers': [0.8, 1.0, 1.2]
}