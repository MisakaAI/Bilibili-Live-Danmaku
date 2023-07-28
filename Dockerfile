FROM python:latest
WORKDIR /usr/src/app
ENV TZ=Asia/Shanghai PYTHONUNBUFFERED=1
COPY live.py ./
RUN pip install -i https://mirrors.tencent.com/pypi/simple/ --no-cache-dir bilibili-api-python \
    && pip install -i https://mirrors.tencent.com/pypi/simple/ --no-cache-dir "psycopg[binary]"
ENTRYPOINT ["python", "live.py"]
