from bilibili_api.login import login_with_password, login_with_sms, send_sms, PhoneNumber, Check
from bilibili_api.user import get_self_info
from bilibili_api import settings
from bilibili_api import Credential, sync
import pickle

mode = int(input("""请选择登录方式：
1. 密码登录
2. 验证码登录
请输入 1/2
"""))

credential = None

# 自动打开 geetest 验证窗口
settings.geetest_auto_open = True

if mode == 1:
    # 密码登录
    username = input("请输入手机号/邮箱：")
    password = input("请输入密码：")

    print("正在登录。")
    c = login_with_password(username, password)
    if isinstance(c, Check):
        # 还需验证
        phone = print("需要进行验证。请考虑使用二维码登录")
        exit(1)
    else:
        credential = c
    print("登录成功")
elif mode == 2:
    # 验证码登录
    phone = input("请输入手机号：")
    print("正在登录。")
    send_sms(PhoneNumber(phone, country="+86")) # 默认设置地区为中国大陆
    code = input("请输入验证码：")
    c = login_with_sms(PhoneNumber(phone, country="+86"), code)
    if isinstance(c, Check):
        # 还需验证
        phone = print("需要进行验证。请考虑使用二维码登录")
        exit(1)
    else:
        credential = c
    print("登录成功")
else:
    print("请输入 1/2 ！")
    exit()

if credential != None:
    name = sync(get_self_info(credential))['name']
    print(f"欢迎，{name}!")
    # print('Credential(sessdata="{}",bili_jct="{}")'.format(credential.sessdata,credential.bili_jct))
    with open('credential','wb') as f:
        pickle.dump(credential,f)
    # 检查 Credential 是否需要刷新
    print(sync(credential.check_refresh()))
