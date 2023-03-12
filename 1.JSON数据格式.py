import json
 
"""1、编写JSON文件"""
#编写json文件
json_path = "./json/json.txt"
data = {"Router": [{"hostname": "R1", "ip":"192.168.1.1", "interface": "eth1"},
                   {"hostname": "R2", "ip":"192.168.1.2", "interface": "eth2"},
                   {"hostname": "R3", "ip":"192.168.1.3", "interface": "eth3"},
                   {"hostname": "R4", "ip":"192.168.1.4", "interface": "eth4"},
                   {"hostname": "R5", "ip":"192.168.1.5", "interface": "eth5"}]}

json_data = json.dumps(data,indent=4) #将字典数据类型转换为json格式数据
# print(json_data)
# print(type(json_data)) #<class 'str'>

#定义一个函数将json数据写入至json.txt
def write_doc(path,doc):
    with open(path,"w") as f:
        f.write(doc)

#函数调用
write_doc(json_path, json_data)


"""2、读取JSON文件"""
with open("./json/my_json.json", "r", encoding="utf-8") as f:
    new_data = json.loads(f.read())
    print(new_data) 
