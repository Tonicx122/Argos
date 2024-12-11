from media_fetch.Tikhub.twitter_api import twitter_search
from media_fetch.modules.utils import save_data_to_file
from media_fetch.modules.utils import save_text_to_csv
from media_fetch.modules.classification import classify
import datetime


def media_fetch():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # API选择
    search_data = twitter_search(num_calls=2)

    # 保存文件名
    filename = f"twitter_data_{current_time}.json"

    save_data_to_file(search_data, 'data', filename)

    save_text_to_csv(search_data, 'data', current_time)

    classify()


def main():
    media_fetch()


if __name__ == '__main__':
    main()
