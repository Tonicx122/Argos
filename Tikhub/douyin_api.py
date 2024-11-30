import requests


def douyin_fetch_data():
    # 获取指定关键词的综合搜索结果

    url = "https://api.tikhub.io/api/v1/douyin/web/fetch_general_search_result"

    params = {
        "keyword": "洪水",  # 关键词
        "offset": 0,  # 偏移量（第一页请求为0）
        "count": 2,  # 数量
        "sort_type": 2,  # 0:综合排序 1:最多点赞 2:最新发布
        "publish_time": 1,  # 0:不限 1:最近一天 7:最近一周 180:最近半年
        "filter_duration": 0,  # 0:不限 0-1:1分钟以内 1-5:1-5分钟 5-10000:5分钟以上
        "search_id": ''  # 搜索id，第一次请求时为空，第二次翻页时需要提供，需要从上一次请求的返回响应中获取
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
