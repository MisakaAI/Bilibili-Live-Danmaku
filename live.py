import sys
import asyncio
import json
import time
import psycopg
from bilibili_api import live

# 使用登录账号爬取弹幕
# 需要使用 `login.py` 登录

# import pickle
# from pathlib import Path
# from bilibili_api import Credential, sync, Danmaku

# file_path = Path.cwd() / "credential"
# credential = Credential()
# if file_path.exists():
#     with open('credential','rb') as f:
#         credential_data = pickle.load(f)
#     credential = Credential(sessdata=credential_data.sessdata,bili_jct=credential_data.bili_jct,buvid3=credential_data.buvid3,dedeuserid=credential_data.dedeuserid,ac_time_value=credential_data.ac_time_value)
#     # 检查 Credential 是否需要刷新
#     if sync(credential.chcek_refresh()):
#         # 刷新 Credential
#         sync(credential.refresh())
# credential =  Credential(sessdata="3b12a453%2C1703936013%2Cd2f1c%2A72l9AzxDNmpFePgRJF7ZaAJ0UpcyNnpt5goqblVbG2LnQj5CzblWpjuTrrUEN41Dw0EYjPCQAANAA",bili_jct="196215dbc03904544c9f55054fdba35b")
# room = live.LiveDanmaku(room_id,credential=credential)

# 发送弹幕 - 用于测试登录状态
# sender = live.LiveRoom(room_id, credential=credential)
# await sender.send_danmaku(Danmaku("弹幕发送成功"))

room_id = sys.argv[1]
room = live.LiveDanmaku(room_id)

hostaddr = "127.0.0.1"
port = "5432"
dbname = "bilibili_live"
user = "postgres"
password = "<YOU PASSWORD>"
connect_timeout = "10"

# 连接数据库
conn = psycopg.connect("hostaddr={} port={} dbname={} user={} password={} connect_timeout={}".format(
    hostaddr, port, dbname, user, password, connect_timeout), autocommit=True)

# 执行SQL语句
async def exec_sql(sql):
    with conn.cursor() as cur:
        cur.execute(sql)

# 收到弹幕
@room.on('DANMU_MSG')
async def on_danmaku(event):
    print('[DANMU_MSG] {}: {}'.format(event['data']
          ['info'][2][1], event['data']['info'][1]))
    try:
        sql = "INSERT INTO danmaku (room_id,uname,uid,msg,create_time,raw_data) VALUES ({room_id},'{uname}','{uid}','{msg}','{create_time}','{raw_data}')".format(
            room_id=event['room_display_id'],
            uname=event['data']['info'][2][1],
            uid=event['data']['info'][2][0],
            msg=event['data']['info'][1],
            create_time=time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(event['data']['info'][9]['ts'])),
            raw_data=json.dumps(event, ensure_ascii=False))
        await exec_sql(sql)
    except:
        sql = "INSERT INTO other (room_id,type,raw_data) VALUES ({room_id},'{_type_}','{raw_data}')".format(
            room_id=room_id,
            _type_='ERROR',
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)

# 收到礼物
@room.on('SEND_GIFT')
async def on_gift(event):
    print('[SEND_GIFT] {} {} {} x {}'.format(event['data']['data']['uname'], event['data']
          ['data']['action'], event['data']['data']['giftName'], event['data']['data']['num']))
    try:
        if event['data']['data']['coin_type'] == 'gold':
            paid = True
        elif event['data']['data']['coin_type'] == 'silver':
            paid = False
        sql = "INSERT INTO gift (room_id,uname,uid,gift_name,gift_num,paid,price,create_time,raw_data) VALUES ({room_id},'{uname}','{uid}','{gift_name}',{gift_num},{paid},{price},'{create_time}','{raw_data}')".format(
            room_id=event['room_display_id'],
            uname=event['data']['data']['uname'],
            uid=event['data']['data']['uid'],
            gift_name=event['data']['data']['giftName'],
            gift_num=event['data']['data']['num'],
            paid=paid,
            price=event['data']['data']['price'],
            create_time=time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(event['data']['data']['timestamp'])),
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)
    except:
        sql = "INSERT INTO other (room_id,type,raw_data) VALUES ({room_id},'{_type_}','{raw_data}')".format(
            room_id=room_id,
            _type_='ERROR',
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)

# 醒目留言
@room.on('SUPER_CHAT_MESSAGE')
async def on_super_chat(event):
    print('[SUPER_CHAT] {}: {}'.format(event['data']['data']
          ['user_info']['uname'], event['data']['data']['message']))
    try:
        sql = "INSERT INTO super_chat (room_id,uname,uid,message,price,start_time,end_time,create_time,raw_data) VALUES ({room_id},'{uname}',{uid},'{message}',{price},'{start_time}','{end_time}','{create_time}','{raw_data}')".format(
            room_id=event['room_display_id'],
            uname=event['data']['data']['user_info']['uname'],
            uid=event['data']['data']['uid'],
            message=event['data']['data']['message'],
            price=event['data']['data']['price'],
            start_time=time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(event['data']['data']['start_time'])),
            end_time=time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(event['data']['data']['end_time'])),
            create_time=time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(event['data']['data']['ts'])),
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)
    except:
        sql = "INSERT INTO other (room_id,type,raw_data) VALUES ({room_id},'{_type_}','{raw_data}')".format(
            room_id=room_id,
            _type_='ERROR',
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)

# 续费大航海
@room.on('GUARD_BUY')
async def on_guard(event):
    print('[GUARD_BUY] {} 开通了 {}'.format(event['data']['data']['username'],event['data']['data']['gift_name']))
    try:
        sql = "INSERT INTO guard (room_id,uname,uid,guard_level,guard_num,gift_name,price,start_time,end_time,raw_data) VALUES ({room_id},'{uname}','{uid}',{guard_level},{guard_num},'{gift_name}',{price},'{start_time}','{end_time}','{raw_data}')".format(
            room_id=event['room_display_id'],
            uname=event['data']['data']['username'],
            uid=event['data']['data']['uid'],
            guard_level=event['data']['data']['guard_level'],
            guard_num=event['data']['data']['num'],
            gift_name=event['data']['data']['gift_name'],
            price=event['data']['data']['price'],
            start_time=time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(event['data']['data']['start_time'])),
            end_time=time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(event['data']['data']['end_time'])),
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)
    except:
        sql = "INSERT INTO other (room_id,type,raw_data) VALUES ({room_id},'{_type_}','{raw_data}')".format(
            room_id=room_id,
            _type_='ERROR',
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)

# 直播开始
@room.on('LIVE')
async def LIVE_START(event):
    try:
        if 'live_time' in event['data']:
            r = live.LiveRoom(room_id)
            room_info = await r.get_room_info()
            print('[LIVE] {} - {}'.format(room_info['room_info']['title'], time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(room_info['room_info']['live_start_time']))))
            sql = "INSERT INTO live_time (room_id,title,area_name,parent_area_name,start_time,raw_data) VALUES ({room_id},'{title}','{area_name}','{parent_area_name}','{start_time}','{raw_data}')".format(
                room_id=room_info['room_info']['room_id'],
                title=room_info['room_info']['title'],
                area_name=room_info['room_info']['area_name'],
                parent_area_name=room_info['room_info']['parent_area_name'],
                start_time=time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(room_info['room_info']['live_start_time'])),
                raw_data=json.dumps(room_info, ensure_ascii=False)
            )
            await exec_sql(sql)
    except:
        sql = "INSERT INTO other (room_id,type,raw_data) VALUES ({room_id},'{_type_}','{raw_data}')".format(
            room_id=room_id,
            _type_='ERROR',
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)

# 直播准备中 aka.live_stop
@room.on('PREPARING')
async def LIVE_STOP(event):
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('[STOP] {}'.format(end_time))
    try:
        sql = "update live_time set end_time = '{end_time}' where id in (select id from live_time where room_id = {room_id} order by start_time desc limit 1)".format(
            end_time=end_time,
            room_id=event['room_display_id']
        )
        await exec_sql(sql)
    except:
        sql = "INSERT INTO other (room_id,type,raw_data) VALUES ({room_id},'{_type_}','{raw_data}')".format(
            room_id=room_id,
            _type_='ERROR',
            raw_data=json.dumps(event, ensure_ascii=False)
        )
        await exec_sql(sql)

# 断开连接
@room.on('DISCONNECT')
async def disconnect(event):
    if 'type' in event:
        t = event['type']
    else:
        t = 'NULL'
    sql = "INSERT INTO other (room_id,type,raw_data) VALUES ({room_id},'{_type_}','{raw_data}')".format(
        room_id=room_id,
        _type_=t,
        raw_data=json.dumps(event, ensure_ascii=False)
    )
    await exec_sql(sql)

# # 系统通知
# @room.on('NOTICE_MSG')
# async def notice_msg(event):
#     if 'type' in event:
#         t = event['type']
#     else:
#         t = 'NULL'
#     sql = "INSERT INTO other (room_id,type,raw_data) VALUES ({room_id},'{_type_}','{raw_data}')".format(
#         room_id=room_id,
#         _type_=t,
#         raw_data=json.dumps(event, ensure_ascii=False)
#     )
#     await exec_sql(sql)


async def main():
    await room.connect()

if __name__ == '__main__':
    asyncio.run(main())
