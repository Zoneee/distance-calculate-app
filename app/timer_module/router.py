# -*- coding: utf-8 -*-
#
# 模块路由文件
# Author: AlphonseLuca
# Email: alphonseluca@163.com
# Created Time: 2024-08-15
# from typing import Dict
from fastapi import APIRouter

# from fastapi import Depends, HTTPException
from schema import MessageResp  # 通用schema
from common.amap import direction_driving as amap_distance_calculate
import schedule
import csv
from .schema import DistanceCalculationReq
import datetime

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/", summary="模块测试API", response_model=MessageResp)
async def test_api():
    """模块测试API"""
    return {"message": "ok"}


@router.post(
    "/create_calculate", summary="创建路径计算任务", response_model=MessageResp
)
async def create_calculate(tasks: list[DistanceCalculationReq]):
    # 每天早上6点到8点每隔10分组计算一次距离
    schedule.every(10).minutes.do(lambda: distance_calculate()).between(
        "06:00", "08:00"
    )
    pass


def distance_calculate_core(tasks: list[DistanceCalculationReq]):
    for task in tasks:
        args = {"origin": task.origin, "destination": task.destination}
        distance_calculate_core(args, task.origin_name, task.destination_name)


def distance_calculate_core(arg, origin, destination):
    result = amap_distance_calculate(arg)
    distance = result["route"]["paths"][0]["distance"]
    fastest_way = result["route"]["paths"][0]["cost"]
    row = {
        "origin": origin,
        "destination": destination,
        "distance": distance,
    } | fastest_way

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(f"{current_date}.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
