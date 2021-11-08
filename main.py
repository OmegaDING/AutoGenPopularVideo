import os
import shutil
import time

import crawl_bilibili_video
import hotWorldOnBilibili
import crawl_baidupic
import crawl_text
import genSRT
import convVideo
import mix_video_read_bgm

print("开始自动生成热门视频")
def initialization():
    try:
        #删除之前的视频
        if(os.path.exists("./video/bilibili")):
            shutil.rmtree("./video/bilibili")
            shutil.rmtree("./video/cutted")
            shutil.rmtree("./video/content")
            shutil.rmtree("./video/croped")
            shutil.rmtree("./video/img")
            shutil.rmtree("./video/final")
            shutil.rmtree("./output")
        os.mkdir("./video/bilibili")
        os.mkdir("./video/cutted")
        os.mkdir("./video/content")
        os.mkdir("./video/croped")
        os.mkdir("./video/img")
        os.mkdir("./video/final")
        os.mkdir("./output")

        # 删除之前合成的read声音
        if (os.path.exists("./read")):
            shutil.rmtree("./read")
        os.mkdir("./read")

        # 删除之前的srt字幕
        if (os.path.exists("./srt/123.srt")):
            os.remove("./srt/123.srt")
        open("./srt/123.srt", "w")
    except:
        print("初始化文件及文件夹失败，正在重试")
        initialization()
initialization()

#获取热词
hotword = hotWorldOnBilibili.hotWorld()
# hotword = "九三阅兵"

def pic():
    try:
        #根据热词获取图片
        crawl_baidupic.craw_baidupic(hotword,20)
    except:
        time.sleep(2)
        print("获取热词图片失败正在重试")
        pic()
pic()




#根据热词获取bilibili视频
def video():
    try:
        crawl_bilibili_video.crawl_bilibili(keyword=hotword,num=5) # num 表示要抓取的数量
    except:
        print("爬取视频失败正在重试")
        time.sleep(2)
        video()
video()

#根据热词获取正文
def text():
    try:
        text = crawl_text.getTEXT(hotword)
        #将正文写入content.txt
        with open("./text/content.txt", "w", encoding="UTF-8") as f:  # 打开文件
            f.write(text)#保存到位置
            f.close()
    except:
        print("生成正文失败，正在重试")
        time.sleep(2)
        text()
text()

print("check text")  #检查text是否合格
input() #输入任意值进行下一步


#将开头 正文 结尾合并
with open("./text/head.txt", "r", encoding="UTF-8") as f:  # 打开文件
    head_text = f.read()
    f.close()
with open("./text/content.txt", "r", encoding="UTF-8") as f:  # 打开文件
    content_text = f.read()
    f.close()
with open("./text/end.txt", "r", encoding="UTF-8") as f:  # 打开文件
    end_text = f.read()
    f.close()
with open("./text/finally.txt", "w", encoding="UTF-8") as f:  # 打开文件
    f.write(head_text + content_text + end_text)#保存到位置
    f.close()

#合成配音及字幕
def srt():
    try:
        #合成配音及字幕
        genSRT.genSRT("./text/finally.txt")
    except:
        time.sleep(2)
        print("生成字幕失败，正在重试")
        srt()
srt()

#合成视频
convVideo.conv_video()

def mix():
    try:
        print("正在开始混合视频bgm和修剪")
        #将视频，配音，bgm合并
        mix_video_read_bgm.add_read_to_final_output()
        #将视频剪裁到和读长一致
        mix_video_read_bgm.cut_video_len_read()
        #添加字幕
        mix_video_read_bgm.add_srt()
        #添加bgm
        mix_video_read_bgm.mix_bgm()
    except:
        print("mix 出错,正在重试")
        mix()
mix()
print("合成content完毕")