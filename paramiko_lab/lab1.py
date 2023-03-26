import paramiko
import time

# 定义backup_config函数
def backup_config(ip,user,pwd):
    # 1.创建一个ssh_client对象用于建立SSH连接
    ssh_client = paramiko.SSHClient()

    # 2.设置连接到没有已知主机秘钥的服务器时使用的策略：AutoAddPolicy表示自动添加主机名及主机秘钥到本地Hostkey对象，
    # 不依赖load_system_host_key的配置。即新建ssh连接时不需要再输入yes或no进行确认
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 3.调用connect()方法传入参数建立SSH连接，本次实验设备采用的是口令认证故：look_for_key=False
    ssh_client.connect(hostname=ip, username=user, password=pwd, look_for_keys=False)
    print(ip + '登录成功')

    # 4.启用交互式shell会话,采集设备配置信息
    command = ssh_client.invoke_shell()
    command.send("screen-length disable\n")
    command.send("dis cur\n")
    time.sleep(3)
    output = command.recv(99999).decode('ascii').replace('\r', '')  # 截取的信息为byte类型，用"ascii"来解码
    # print(output)
    with open(f'./paramiko_lab/{ip}.txt','w',encoding='ascii') as backup:
        backup.write(output)
        print(ip + '配置备份成功')

    # 5.关闭ssh连接
    ssh_client.close()

if __name__ == '__main__':
    ip_list= ['192.168.1.1','192.168.1.2','192.168.1.3','192.168.1.4','192.168.1.5']
    user = 'python'
    pwd = 'h3c@123'
    
     # for循环遍历ip_list列表元素，依次调用backup_config函数实现ssh连接交换机,备份配置文件
    for ip in ip_list:
        backup_config(ip, user, pwd)
    
    