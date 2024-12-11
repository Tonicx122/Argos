import requests


def weibo_search():
    # 搜索

    url = "https://api.tikhub.io/api/v1/weibo/web/fetch_search_data"

    params = {
        "keyword": "洪水",  # 关键词
        "page": "1",  # 页数
        "search_type": "61",  # 搜索类型 1: 综合；61: 实时；3: 用户；60: 热门；64: 视频；63: 图片；21: 文章；38: 话题；98: 超话
    }

    headers = {
        'Authorization': 'Bearer z5cVTn59mFErmXYJ13WGmHtv8CsAiY2HirFZ+x7ouGtC6Q8kY94r9j3yUw==',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"请求失败，状态码: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"请求发生错误: {e}"}
