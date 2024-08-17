from .http import get
from settings import AMAP_KEY
from .logger import logger


def direction_driving(arg):
    url = "https://restapi.amap.com/v5/direction/driving"
    params = {
        "origin": arg["origin"],
        "destination": arg["destination"],
        "key": AMAP_KEY,
        "show_fields": "cost,tmcs",
    }
    resp = get(url, params=params)
    if resp.status_code != 200:
        logger.error(f"请求高德地图API失败: {resp.text}")
        return None

    result = resp.json()
    if result["status"] == "1":
        logger.info(f"请求高德地图API成功: {result}")
        return result
    else:
        logger.error(f"请求高德地图API失败: {result}")
        return None
