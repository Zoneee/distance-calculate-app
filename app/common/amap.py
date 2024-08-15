from .http import get
from settings import AMAP_KEY


def direction_driving(arg):
    url = f"https://restapi.amap.com/v5/direction/driving?origin={arg['origin']}&destination={arg['destination']}&key={AMAP_KEY}&show_fields=cost,tmcs"
    resp = get({"url": url})
    result = resp.json()
    if result["status"] == 1:
        return result
    else:
        return None
