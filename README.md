# Bilibili-Live-Danmaku

收集哔哩哔哩直播间的弹幕。

## 弹幕姬

为了应对B站抽风，昵称只显示第一个字，临时开发的弹幕姬。

- [阿源の弹幕姬](chat/README.md)

## 安装

1. 安装 `Python3` 和 `PostgreSQL`

```sh
apt install python3
apt install python3-dev libpq-dev
apt install postgresql
```

2. 安装 `psycopg` 和 `bilibili-api-python`

```sh
pip3 install --upgrade pip
pip3 install "psycopg[binary]"
pip3 install bilibili-api-python
```

### 创建数据库

```sh
# 执行 initialization.sql
psql -h 127.0.0.1 -U postgres -p 5432 -f initialization.sql
```

### 添加 systemd 服务

```sh
# 修改文件目录为当前目录，然后添加到 systemd 文件目录
sed "s#{{PWD}}#$(echo $PWD)/live.py#g" ./live.service > /etc/systemd/system/live@.service
```

### 启动服务

`@` 后面接直播间ID，可以运行多次，收集多个直播间的弹幕。

```sh
# 开启服务
systemctl start live@3472667.service

# 开机自动启动
systemctl enable live@3472667.service
```

程序一直运行有时候会出问题，必要时可以定时重启一下。  
也可以通过 `check_systemd.py` 检查程序运行是否正常，如果不正常就重启。  
使用 `corntab` 设置为定时执行。

```crontab
# 每小时的0分钟（整点）时执行
0 * * * * /root/check_systemd.py
# 在每天的凌晨4点执行
0 4 * * * systemctl restart live@3472667.service
```

## Docker

程序也支持以 `Docker` 的方式运行。

- [Dockerfile](Dockerfile)

### 使用方法

```bash
# 构建镜像
docker build -t danmaku .

# 运行
docker run -d --restart=always --name live_3472667 --net="host" danmaku 3472667

# 使用登录账号运行程序
# docker run -d --restart=always --name live_90049 --net="host" -v <PATH>/credential:/usr/src/app/credential live_danmaku 90049
```

## 其他

- [常用SQL查询语句](select.sql)