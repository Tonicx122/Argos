import os
import pandas as pd
import json

def save_data_to_file(data, folder_name, filename):
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

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


def save_text_to_csv(data, folder_name, current_time):
    filename = f"tweet_text_{current_time}.csv"

    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    folder_path = os.path.join(project_dir, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, filename)

    # 检查 data 是否为列表
    if not isinstance(data, list):
        data = [data]  # 如果不是列表，转换为单元素列表

    # 提取 "timeline" 中的推文数据
    all_tweets = []
    for page_data in data:  # 遍历每次调用返回的数据
        tweets = page_data.get("data", {}).get("timeline", [])
        for tweet in tweets:
            if tweet.get("type") == "tweet":
                tweet_id = tweet.get("tweet_id", "")
                keyword = page_data.get("params", {}).get("keyword", "")  # 从 "params" 中提取 keyword
                location = tweet.get("user_info", {}).get("location", "")  # 从 "user_info" 中提取 location
                text = tweet.get("text", "")  # 提取 text
                all_tweets.append({"id": tweet_id, "keyword": keyword, "location": location, "text": text})

    # 创建 DataFrame
    df = pd.DataFrame(all_tweets)

    # 保存到 CSV 文件
    df.to_csv(file_path, index=False, encoding='utf-8')

    print(f"提取完成，共提取 {len(all_tweets)} 条推文，已保存到 {file_path}")