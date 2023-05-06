# Bilibili-Live-Danmaku

收集哔哩哔哩直播间的弹幕。

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

程序一直运行有时候会出问题，可以定时重启一下。  
`check_systemd.py` 可以检查程序运行是否正常，如果不正常就重启。  
可以通过 `corntab` 的方式设置为定时执行。

```crontab
0 * * * * /root/check_systemd.py
0 4 * * * systemctl restart live@3472667.service
```

## 其他

- [常用SQL查询语句](select.sql)