import requests


def twitter_search(num_calls=1):
    url = "https://api.tikhub.io/api/v1/twitter/web/fetch_search_timeline"

    all_data = []
    cursor = None  # 初始化 cursor

    headers = {
        'Authorization': 'Bearer z5cVTn59mFErmXYJ13WGmHtv8CsAiY2HirFZ+x7ouGtC6Q8kY94r9j3yUw==',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    for i in range(num_calls):
        print(f"第 {i + 1} 次调用 Twitter API...")

        params = {
            "keyword": "flood",  # 关键词
            "search_type": "Latest",  # 搜索类型，默认为Top，其他可选值为Latest，Media，People, Lists
            "cursor": cursor or '',  # 游标，默认为None，用于翻页，后续从上一次请求的返回结果中获取
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            all_data.append(data)
            # 更新 cursor
            cursor = data.get("data", {}).get("next_cursor")
            if not cursor:  # 如果没有下一页，提前停止
                print("没有更多数据，停止调用。")
                break
        else:
            print(f"请求失败，状态码: {response.status_code}")
            break

    return all_data