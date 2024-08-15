# -*- coding: utf-8 -*-
#
# 模块路由配置文件
# Author: AlphonseLuca
# Email: alphonseluca@163.com
# Created Time: 2024-08-15
# from pydantic import BaseModel, Field

from pydantic import BaseModel, Field


class DistanceCalculationReq(BaseModel):
    origin: str = Field(..., title="起点", description="起点")
    origin_name: str = Field(..., title="起点", description="起点")
    destination: str = Field(..., title="终点", description="终点")
    destination_name: str = Field(..., title="终点", description="终点")
