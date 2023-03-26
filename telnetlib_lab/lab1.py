# 导入相关模块 
import telnetlib
import time

# 定义backup_config函数, 传入参数ip,user,password
def backup_config(ip,user,password):
    tn = telnetlib.Telnet(ip)
    tn.read_until(b"login: ")
    tn.write(user.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    print(ip +'登录成功')
    tn.write(b'screen-length disable\n') #取消分屏显示
    tn.write(b'dis cur\n')
    time.sleep(1)
    output=tn.read_very_eager().decode('ascii').replace('\r', '')
    # print(output)
    with open(f'./telnetlib_lab/{ip}.txt','w',encoding='ascii') as backup: #创建.txt文件,并将回显output内容写入
        backup.write(output)
        print(ip + '配置备份成功')   
    tn.close() #关闭telnet连接

if __name__ == '__main__':
    ip_list = ['192.168.1.1','192.168.1.2','192.168.1.3','192.168.1.4','192.168.1.5']
    user = 'python'
    password = 'h3c@123' 
    # for循环遍历ip_list列表元素，依次调用backup_config函数实现tenlent交换机
    for ip in ip_list:
        backup_config(ip, user, password)
    
    
    