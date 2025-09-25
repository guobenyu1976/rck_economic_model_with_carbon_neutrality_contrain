# carbon_neutrality_model/utils.py

import pandas as pd
import re


def export_results_to_csvs(results_data, file_prefix, start_year):
    """
    将模拟结果字典导出为多个独立的 CSV 文件，每个情景一个文件。

    Args:
        results_data (dict): 结果数据。键是情景名称(str)，值是包含各向量的字典。
        file_prefix (str): 输出的 CSV 文件的前缀，如 'main_scenario_results'。
        start_year (int): 模拟的起始年份，用于生成索引。
    """
    print(f"准备将结果导出为多个 CSV 文件 (前缀: '{file_prefix}')...")

    try:
        # 遍历结果字典，每个键值对是一个情景/案例
        for scenario_name, scenario_data in results_data.items():

            # 检查该情景是否有有效数据
            if scenario_data and isinstance(scenario_data, dict) and scenario_data.values():

                # ------------------- 修改开始 -------------------
                # 关键修复：直接从字典创建 DataFrame，让 pandas 自动处理不同长度的列
                # 它会用 NaN 填充较短列的末尾
                df = pd.DataFrame.from_dict(scenario_data, orient='index').transpose()

                # 根据 DataFrame 的最终行数（即最长向量的长度）来创建年份索引
                num_rows = len(df)
                years = range(start_year, start_year + num_rows)
                df.index = years
                df.index.name = 'Year'
                # ------------------- 修改结束 -------------------

                # --- 创建安全的文件名 ---
                sanitized_scenario_name = re.sub(r'[\\/*?:"<>|]', "", scenario_name).replace(' ', '_')
                filename = f"{file_prefix}_{sanitized_scenario_name}.csv"

                # --- 导出到 CSV ---
                df.to_csv(filename, encoding='utf-8-sig')
                print(f"  - 结果已成功导出到文件: '{filename}'")

            else:
                print(f"  - 警告：情景 '{scenario_name}' 没有有效数据，已跳过。")

        print("--- 所有情景已成功导出为 CSV 文件 ---")

    except Exception as e:
        print(f"导出到 CSV 时发生错误: {e}")
        print("\n--- 原始结果数据 ---")
        print(results_data)
        print("--------------------")


def export_results_to_excel(results_data, filename, start_year):
    """
    将模拟结果字典导出到指定的 Excel 文件，每个情景一个工作表。
    此版本已修复因数据向量长度不匹配而导致文件损坏的问题。

    Args:
        results_data (dict): 结果数据。键是情景名称(str)，值是包含各向量的字典。
        filename (str): 输出的 Excel 文件名 (例如 'my_results.xlsx')。
        start_year (int): 模拟的起始年份，用于生成索引。
    """
    print(f"准备将结果写入 Excel 文件: '{filename}'...")

    try:
        # 使用 ExcelWriter 来将多个 DataFrame 写入不同的 sheet
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:

            # 遍历结果字典，每个键值对是一个情景/案例
            for scenario_name, scenario_data in results_data.items():

                # 检查该情景是否有有效数据
                if scenario_data and isinstance(scenario_data, dict) and scenario_data.values():

                    # --- 关键修复 ---
                    # 1. 直接从字典创建 DataFrame，让 pandas 自动处理不同长度的列
                    #    它会用 NaN (空值) 填充较短列的末尾，从而避免错误。
                    df = pd.DataFrame.from_dict(scenario_data, orient='index').transpose()

                    # 2. 根据 DataFrame 的最终行数（即最长向量的长度）来创建年份索引
                    num_rows = len(df)
                    years = range(start_year, start_year + num_rows)
                    df.index = years
                    df.index.name = 'Year'  # 给索引列命名

                    # 3. 将格式正确的 DataFrame 写入到 Excel 的一个 sheet 中
                    print(scenario_name)
                    safe_sheet_name = re.sub(r'[\\/*?:\[\]：？＊＼／]', '', scenario_name)[:31]
                    print(safe_sheet_name)
                    df.to_excel(writer, sheet_name=safe_sheet_name)
                    print(f"  - 已将情景 '{scenario_name}' 的数据写入工作表。")
                else:
                    print(f"  - 警告：情景 '{scenario_name}' 没有有效数据，已跳过。")

        print(f"--- 结果已成功导出到 Excel 文件: '{filename}' ---")

    except Exception as e:
        print(f"导出到 Excel 时发生错误: {e}")
        # 如果导出失败，仍然打印原始数据以供调试
        print("\n--- 原始结果数据 ---")
        print(results_data)
        print("--------------------")
