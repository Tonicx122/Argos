import json

from media_fetch.Tikhub.twitter_api import twitter_search
from media_fetch.modules.utils import save_data_to_file
from media_fetch.modules.utils import save_text_to_csv
from media_fetch.modules.classification import classify
from media_fetch.modules.utils import extract_tweets_and_images
import datetime


def media_fetch():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # API选择
    search_data = twitter_search(num_calls=2)

    if search_data is not None:
        # 保存文件名
        filename = f"twitter_data_{current_time}.json"

        file_path = save_data_to_file(search_data, 'data', filename)
        save_text_to_csv(search_data, 'data', current_time)
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        # 调用函数
        extract_tweets_and_images(json_data, image_folder=f"images/{current_time}",
                                  csv_file=f"media_fetch/data/tweets_images_{current_time}.csv")

    else:
        print("未获取到有效数据")

#    classify()


def main():
    media_fetch()

    # current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # with open(r"C:\Users\Tonicx\PycharmProjects\RedianProject\media_fetch\data\twitter_data_2025-01-27_16-42-46.json", "r", encoding="utf-8") as f:
    #     json_data = json.load(f)
    # # 调用函数
    # extract_tweets_and_images(json_data, image_folder=f"images/{current_time}", csv_file=f"media_fetch/data/tweets_images_{current_time}.csv")

if __name__ == '__main__':
    main()
