import csv

import requests
import time
import json

get_url = "https://s.search.bilibili.com/main/hotword"

def hotWorld():
    #2.发送get请求
    resp = requests.get(get_url)
    content = json.loads(resp.content)
    counter = 1
    t = content["timestamp"]
    #3.打开文件，处理，报告状态
    if content["message"] == "success":
        with open("bilibilihotword.csv","w+")as f:
            for factor in content["list"]:
                f.write(time.ctime(t))
                f.write(",")
                f.write(str(counter))
                f.write(",")
                f.write(factor["keyword"])
                f.write("\n")
                counter += 1
            f.close()
            print("获取当前热榜完毕，当前时间为%s" % str(time.ctime(t)))
        with open("bilibilihotword.csv", "r")as f:
            reader = csv.reader(f)
            head_row = next(reader)
            column = [row[0] for row in reader]

        f.close()
        print("当前热榜top:"+head_row[2])
        return head_row[2]
    else:
        print("本次获取接口出错，当前时间为%s.正在重新尝试" % str(time.ctime(t)))
        time.sleep(5)
        hotWorld()

def get_hot_world():
    return hotWorld()

if __name__ == "__main__":
    print(hotWorld())

