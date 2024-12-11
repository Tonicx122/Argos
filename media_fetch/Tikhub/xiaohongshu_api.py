import requests


def xhs_search_notes():
    # 搜索笔记

    url = "https://api.tikhub.io/api/v1/xiaohongshu/web/search_notes"

    params = {
        "keyword": "洪水",  # 关键词
        "page": 1,  # 页码，默认为1
        "sort": "time_descending",
        # 综合排序（默认参数）: general
        # 最热排序: popularity_descending
        # 最新排序: time_descending
        "noteType": "_0",  # _0:综合笔记（默认参数） _1:视频笔记 _2:图文笔记

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
