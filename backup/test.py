import datetime
import os
from pathlib import Path

# print(__file__)  # __file__：test.py的绝对路径-->d:/NetDevOps/backup_lab/test.py

ABS_FILE_PATH = Path(__file__).resolve() # test.py的绝对路径-->D:\NetDevOps\backup_lab\test.py
print(ABS_FILE_PATH)

BASE_DIR = Path(__file__).resolve().parent  # test.py的上一级目录-->D:\NetDevOps\backup_lab
print(BASE_DIR)

# 配置备份路径
# 将BASE_DIR、backup_config、str(datetime.date.today()进行拼接 --> D:\NetDevOps\backup_lab\backup_config\2023-02-21
BACKUP_CONFIG_DIR = Path(BASE_DIR, 'backup_config', str(datetime.date.today()))
print(BACKUP_CONFIG_DIR)


# 设备清单devices.xlsx路径
DEVICE_DIR = Path(BASE_DIR, 'devices.xlsx')
print(DEVICE_DIR)

ip_list=['192.168.10.1','192.168.10.2','192.168.10.3']

a = '认证失败IP地址为:\n'
print('认证失败IP地址为:\n'+'\n'.join(ip_list))





"""
获取当前目录
"""
# 使用os.getcwd()函数方法来获取工作目录
# OS = os.getcwd()
# print("os模块获取路径:",OS) #D:\NetDevOps

# 使用使用具体路径Path对象调用cwd()方法来获取工作目录
# Pa = Path().cwd()
# print("pathlib模块获取路径:", Pa)  # D:\NetDevOps


"""
获取上级/上上级目录
"""





