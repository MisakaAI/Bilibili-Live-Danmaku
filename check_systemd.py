#!/usr/bin/env python3
import time
import subprocess
# from send_mail import send_mail

# 要监测的服务名
service_list = ["live@3472667.service","live@90049.service"]

def check_systemd(service_name):
    try:
        # 执行 systemctl status 命令，获取服务状态
        output = subprocess.check_output(["systemctl", "status", service_name], stderr=subprocess.STDOUT).decode()
        service_type = True
    except subprocess.CalledProcessError as e:
        service_type = False
        # 如果状态不为0，则服务状态异常，进行重启。
        try:
            # 执行 systemctl restart 命令，重启服务。
            restart_output = subprocess.check_output(["systemctl", "restart", service_name]).decode()
            # 重启成功状态为T
            service_restart_type = True
        except subprocess.CalledProcessError as e:
            # 重启失败则状态为F
            service_restart_type = False

    # 等待5秒
    time.sleep(5)

    # 进行最后的检查
    if not service_type:
        try:
            status_output = subprocess.check_output(["systemctl", "status", service_name], stderr=subprocess.STDOUT).decode()
        except subprocess.CalledProcessError as e:
            status_output = e.output.decode()

        room_id = service_name.split('.')[0].split('@')[1]
        if "Active: active (running)" in status_output:
            print('[info] 弹幕姬已经重启。({})','{} 服务运行异常，已经成功重启。\n\n{}'.format(room_id,service_name,status_output))
            # send_mail('[info] 弹幕姬已经重启。({})','{} 服务运行异常，已经成功重启。\n\n{}'.format(room_id,service_name,status_output))
        else:
            print('[warning] 弹幕姬异常！({})','{} 服务重启失败。请手动检查。\n\n{}'.format(room_id,service_name,status_output))
            # send_mail('[warning] 弹幕姬异常！({})','{} 服务重启失败。请手动检查。\n\n{}'.format(room_id,service_name,status_output))

if __name__ == '__main__':
    for i in service_list:
        check_systemd(i)
