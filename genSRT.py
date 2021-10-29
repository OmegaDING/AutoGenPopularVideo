import math

import tts
import time
from datetime import datetime, date, timedelta
import eyed3

def genSRT(text):
    with open(text, "r",encoding="UTF-8") as f:
        data = f.read()
        data = data.replace("，","。")#将，替换为。都作为分句标识
        strlist = data.split('。')
        f.close()

    total_num= len(strlist) -1 #总句子数
    print("生成字幕时：共%d句话"%(total_num))
    num = 0 #当前句子数

    with open("./srt/123.srt", "w", encoding="UTF-8") as f:  # 打开文件
        startTime = '00:00:00:000000'
        startTime = datetime.strptime(startTime, '%H:%M:%S:%f')
        audio_len={}
        for i in range(total_num):
            f.write(str(num)+"\n")
            #合成语音
            print("合成第%d段语音："%(i) +strlist[i])
            try:
                audio_len[i] = tts.tts(strlist[i])
            except:
                time.sleep(10)
                try:
                    audio_len[i] = tts.tts(strlist[i])
                except:
                    time.sleep(10)
                    audio_len[i] = tts.tts(strlist[i])
            time.sleep(6)  #最大并发较低，等待服务器
            print("合成第%d段字幕："%(i) + strlist[i])
            endtime = startTime  + timedelta(seconds =  int(audio_len[i]),milliseconds=1000*math.modf(audio_len[i])[0],microseconds= 1000*math.modf(1000*math.modf(audio_len[i])[0])[0])  #见隔时间长度
            f.write(startTime.strftime("%H:%M:%S,000")   +  " --> "+  endtime.strftime("%H:%M:%S,000") +"\n")
            startTime = endtime
            f.write(strlist[i]+"\n")
            f.write("\n")
            num+=1

    #计算共用了多久
    total_len = 0
    for i in range(total_num):
        total_len += audio_len[i]
    print("the part total duration:" + str(total_len))
    return  audio_len
