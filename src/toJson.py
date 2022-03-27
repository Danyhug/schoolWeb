# 将信息更改为json格式
import json

data = []
with open('SchoolWeb.txt', 'r') as f:
    # 读取所有数据
    r = f.readlines()

    for v in r:
        # 1&password
        unameTemp = v.split('=')[1].split('&')[0]
        # 2\n
        passTemp = v.split('=')[2].split('\n')[0]
        data.append({
            'uname': unameTemp,
            'passwd': passTemp
        })

# 解析成JSON数据
jsonData = json.dumps(data)
with open('data.json', 'w+') as f:
    f.write(jsonData)
    print('over')