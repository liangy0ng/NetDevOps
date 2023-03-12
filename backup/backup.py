from pathlib import Path
from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
import pandas as pd
import datetime
import os
import threading
from pprint import pprint


class BackupConfig(threading.Thread):
    # 获取当前backup.py文件绝对路径
    ABS_FILE_PATH = Path(__file__).resolve()

    # 获取backup.py的上一级目录
    BASE_DIR = Path(__file__).resolve().parent

    # 配置备份路径：将BASE_DIR、backup_config、str(datetime.date.today()进行拼接得到备份路径
    BACKUP_CONFIG_DIR = Path(BASE_DIR, 'backup_config', str(datetime.date.today()))

    # 设备清单路径：将将BASE_DIR、'devices.xlsx'拼接得到设备清单devices.xlsx路径
    DEVICE_DIR = Path(BASE_DIR, 'devices.xlsx')

    # 定义存放认证失败、认证超时IP列表
    auth_faild = []
    auth_timeout = []

    def __init__(self, device):
        self.device = device
        super().__init__()

    @classmethod
    def create_backup_dir(cls):
        """
        构建类方法create_backup_dir:创建备份目录，不存在就新建，存在就利旧使用
        """
        if not os.path.exists(cls.BACKUP_CONFIG_DIR):
            os.makedirs(cls.BACKUP_CONFIG_DIR)
            print("备份目录创建成功")
        else:
            print("备份目录已经存在")

    @classmethod
    def get_device_info(cls):
        """
        构建类方法get_device_info:通过pandas从devices.xlsx表中获取设备登录信息,to_dict转成字典形式
        """
        return pd.read_excel(cls.DEVICE_DIR, sheet_name='devices').to_dict(orient='records')

    def run(self):
        """
        重写run方法:备份配置文件
        """
        device_info = {
            'device_type': self.device["platform"],
            'host': self.device["device_name"],
            'ip': self.device["device_ip"],
            'username': self.device["username"],
            'password': self.device["password"],
            'port': self.device["port"],
            'timeout': 300,
            'conn_timeout': 120
        }
        try:
            with ConnectHandler(**device_info) as connect, open(
                    f'{self.BACKUP_CONFIG_DIR}/{self.device["site_name"]}_{self.device["device_name"]}({self.device["device_ip"]}).txt',
                    'w', encoding='utf-8') as backup_config_file:
                print(self.device["device_ip"] + '登录成功')
                output = connect.send_command("dis cur", delay_factor=2)
                backup_config_file.write(output)
                print(self.device["device_ip"] + "备份成功")
        except AuthenticationException:
            self.auth_faild.append(self.device["device_ip"])
        except NetMikoTimeoutException:
            self.auth_timeout.append(self.device["device_ip"])

    @classmethod
    def exception(cls):
        """
        构建类方法exception:将认证失败、认证超时的IP列表信息转字符串写入至auth_faild_log.txt、auth_timeout_log.txt便于查看
        """
        with open(f'{cls.BACKUP_CONFIG_DIR}/auth_faild_log.txt', 'w', encoding='utf-8') as auth_faild_log, open(
                f'{cls.BACKUP_CONFIG_DIR}/auth_timeout_log.txt', 'w', encoding='utf-8') as auth_timeout_log:
            auth_faild_log.write('认证失败IP地址为:\n' + '\n'.join(cls.auth_faild))
            auth_timeout_log.write('认证超时IP地址为:\n' + '\n'.join(cls.auth_timeout))

            print("认证失败IP地址为:\n", cls.auth_faild)
            print("认证超时IP地址为:\n", cls.auth_timeout)


if __name__ == "__main__":
    # # 路径测试
    # # 使用__file__获取backup.py的绝对路径-->C:/Users/Administrator.DESKTOP-HKMFMDS/PycharmProjects/python_practise2/backup/backup.py
    # print(__file__)
    #
    # # 获取backup.py的绝对路径-->C:\Users\Administrator.DESKTOP-HKMFMDS\PycharmProjects\python_practise2\backup\backup.py
    # print(BackupConfig.ABS_FILE_PATH)
    #
    # # 获取backup.py的上一级目录路径-->C:\Users\Administrator.DESKTOP-HKMFMDS\PycharmProjects\python_practise2\backup
    # print(BackupConfig.BASE_DIR)
    #
    # # 获取配置备份路径,将BASE_DIR、backup_config、str(datetime.date.today()进行拼接 --> C:\Users\Administrator.DESKTOP-HKMFMDS\PycharmProjects\python_practise2\backup\backup_config\2023-02-22
    # print(BackupConfig.BACKUP_CONFIG_DIR)
    #
    # # 获取设备清单路径：将BASE_DIR、'devices.xlsx'拼接得到设备清单devices.xlsx路径 --> C:\Users\Administrator.DESKTOP-HKMFMDS\PycharmProjects\python_practise2\backup\devices.xlsx
    # print(BackupConfig.DEVICE_DIR)

    # 二、正式执脚本采集配置信息
    # 1.创建备份目录
    BackupConfig.create_backup_dir()

    # 2.获取设备登录信息
    devices = BackupConfig.get_device_info()
    # pprint(devices)

    # 3.登录设备采集配置信息
    threads = []
    for device in devices:
        backup = BackupConfig(device)
        backup.start()
        threads.append(backup)
    for t in threads:
        t.join()

    # 4.打印认证失败、认证超时IP信息
    BackupConfig.exception()
