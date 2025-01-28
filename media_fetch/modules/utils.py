import os
import pandas as pd
import json
import requests
import csv
from datetime import datetime
from uuid import uuid4


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
        return file_path
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


def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response:
                    f.write(chunk)
            return True
        else:
            print(f"下载失败: {url}, 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"下载错误: {url}, 错误信息: {e}")
        return False


def extract_tweets_and_images(json_data, image_folder, csv_file):
    # 创建图像保存文件夹
    os.makedirs(image_folder, exist_ok=True)

    # 创建 CSV 文件所在的目录（如果不存在）
    csv_dir = os.path.dirname(csv_file)
    if csv_dir:  # 如果 csv_file 包含目录路径
        os.makedirs(csv_dir, exist_ok=True)

    # 打开 CSV 文件准备写入
    with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["tweet_id", "image_id", "tweet_text", "image"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for element in json_data:
            timeline = element.get("data", {}).get("timeline", [])
            if not timeline:
                print("未找到推文数据！")
                return
            # 遍历每条推文
            for tweet in timeline:
                # 生成唯一的 tweet_id
                tweet_id = tweet.get("tweet_id")
                text = tweet.get("text", "").strip()
                # 替换所有换行符（\n 和 \r）为单个空格
                text = text.replace("\n", " ").replace("\r", " ")

                media = tweet.get("entities", {}).get("media", [])
                for medium in media:
                    image_url = medium.get("media_url_https", "")
                    if image_url:
                        # 生成图像 ID 和保存路径
                        image_id = f"{tweet_id}_0"  # 图像 ID 规则：tweet_id + 序号
                        image_name = f"{image_id}.jpg"
                        image_path = f"{image_folder}/{image_name}"

                        # 下载并保存图像
                        if download_image(image_url, image_path):
                            # 写入 CSV 文件
                            writer.writerow({
                                "tweet_id": tweet_id,
                                "image_id": f"{image_folder}/{image_id}",
                                "tweet_text": text,
                                "image": image_path
                            })
                            print(f"已保存: {image_path}")
                        else:
                            print(f"跳过: {image_url}")
