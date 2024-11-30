from Tikhub.douyin_api import douyin_fetch_data
from Tikhub.xiaohongshu_api import xhs_search_notes
import json
import os
import datetime


def save_data_to_file(data, folder_name, filename):
    project_dir = os.path.dirname(os.path.abspath(__file__))

    folder_path = os.path.join(project_dir, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # 保存为 JSON 文件
        print(f"数据已成功保存到 {file_path}")
    except Exception as e:
        print(f"保存数据时出错: {e}")


def main():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # API选择
    search_data = xhs_search_notes()
    # 保存文件名
    filename = f"xhs_data_{current_time}.json"

    save_data_to_file(search_data, 'data', filename)


if __name__ == '__main__':
    main()
