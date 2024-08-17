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
import threading
import time
from common.logger import logger
import os


task_enabled = False
disable_calculate_list = []

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/", summary="模块测试API", response_model=MessageResp)
async def test_api():
    """模块测试API"""
    return {"message": "ok"}


@router.post(
    "/enable_calculate", summary="启动路径计算任务", response_model=MessageResp
)
async def enable_calculate(tasks: list[DistanceCalculationReq]):
    # 每天早上6点到8点每隔10分组计算一次距离
    global task_enabled, disable_calculate_list
    disable_calculate_list = tasks
    task_enabled = True
    logger.info(f"启动路径计算任务. info: {tasks}. enable: {task_enabled}")

    return {"message": "ok"}


@router.post(
    "/disable_calculate", summary="停止路径计算任务", response_model=MessageResp
)
async def disable_calculate():
    global task_enabled, disable_calculate_list
    disable_calculate_list = []
    task_enabled = False
    logger.info(
        f"关闭路径计算任务. info: {disable_calculate_list}. enable: {task_enabled}"
    )
    return {"message": "ok"}


def distance_calculate_core():
    global task_enabled, disable_calculate_list
    morning_time_range = range(7, 9)
    afternoon_time_range = range(17, 19)
    now_hour = datetime.datetime.now().hour
    if task_enabled and (
        now_hour in morning_time_range or now_hour in afternoon_time_range
    ):
        for task in disable_calculate_list:
            args = {"origin": task.origin, "destination": task.destination}

            result = amap_distance_calculate(args)
            distance = result["route"]["paths"][0]["distance"]
            fastest_way = result["route"]["paths"][0]["cost"]
            row = (
                {
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "origin": task.origin_name,
                    "destination": task.destination_name,
                    "distance": distance,
                }
                | fastest_way
                | {"distance_unit": "m", "time_unit": "s"}
            )

            # 创建csv目录
            if not os.path.exists("./csv"):
                os.makedirs("./csv")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            with open(
                f"./csv/{current_date}.csv", "a", newline="", encoding="utf8"
            ) as f:
                writer = csv.DictWriter(f, fieldnames=row.keys())
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow(row)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)


# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

schedule.every(10).minutes.do(lambda: distance_calculate_core())
