FROM python:3.12-alpine

LABEL user="AlphonseLuca"
LABEL email="alphonseluca@163.com"
LABEL version="1.0"
LABEL description="基于python3.12-alpine的FastAPI镜像"
ENV DEBIAN_FRONTEND noninteractive

# RUN apt-get update -y \
#     && apt-get install -y --no-install-recommends \
#     git \
#     && apt-get clean \
#     && rm -r /var/lib/apt/lists/*

#  国内源
# RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
# RUN pip3 config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
# RUN pip3 config set global.index-url http://pypi.douban.com/simple/
# RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# install fastapi
COPY ./requirements.txt /
RUN pip3 --no-cache-dir install -r /requirements.txt \
    && rm -f /requirements.txt

# 终端设置
# 默认值是dumb，这时在终端操作时可能会出现：terminal is not fully functional
ENV LANG C.UTF-8
ENV TERM xterm
ENV PYTHONIOENCODING utf-8

# 解决时区问题
ENV TZ "Asia/Shanghai"


WORKDIR /app
COPY . /app
# Check if settings.py exists and throw an error if it does
RUN !(test -f /app/settings.py) || (echo "settings.py file not found!" && exit 1)
# # Check if settings.py exists and throw an error if it does
# RUN if test -f /app/settings.py; then \
#         echo "settings.py file should not exist!" && exit 1; \
#     else \
#         echo "settings.py file does not exist, continuing..."; \
#     fi

EXPOSE 8000
ENTRYPOINT [ "uvicorn", "main:app", "--host", "8000" ]