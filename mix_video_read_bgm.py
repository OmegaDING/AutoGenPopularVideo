import os
import random
from moviepy.editor import *
import eyed3
import librosa
from pathlib import Path

def add_read_to_final_output():
    print("混合output和生成的语音")
    cmd = "ffmpeg -i ./read/output.mp3 -i video/final/output.mp4 -y ./output/output.mp4"
    print(cmd)
    os.system(cmd)


def cut_video_len_read():
    print("将video剪裁到和read时长一致")
    # 获取时长
    duration = librosa.get_duration(filename="./read/output.mp3")
    print(duration)
    cmd = "ffmpeg -i ./output/output.mp4 -t %d -y ./output/output_cutted.mp4"%(duration)
    print(cmd)
    os.system(cmd)


def add_srt():
    print("插入srt字幕到视频中")
    cmd = "ffmpeg -i ./output/output_cutted.mp4 -vf subtitles=./srt/123.srt -y ./output/output_title.mp4"
    print(cmd)
    os.system(cmd)

#计算txt文件有多少个，和。
def sentence_num(path):
    with open(path, "r",encoding="UTF-8") as f:
        data = f.read()
        data = data.replace("，","。")#将，替换为。都作为分句标识
        strlist = data.split('。')
        f.close()
    total_num= len(strlist) -1 #总句子数
    return total_num

#获取read文件夹中指定序号范围的语音长度
def read_len(start,length):
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    num=start
    duration=0
    file = "./read/result"+str(num)+".mp3"
    while (os.path.exists(file) and num<length):
        duration += librosa.get_duration(filename=file)
        file = father_path + "\\read\\result" + str(num) + ".mp3"
        #print(file)
        num += 1
    return duration


def mix_bgm():
    print("开始制作bgm")
    #获取文章各个部分的长度
    #开头
    total_num_head= sentence_num("./text/head.txt") #总句子数
    head_len = read_len(0,total_num_head)
    #正文
    total_num_content= sentence_num("./text/content.txt") #总句子数
    content_len = read_len(total_num_head,total_num_head+total_num_content)
    #结尾
    total_num_end= sentence_num("./text/end.txt") #总句子数
    end_len = read_len(total_num_head + total_num_content,total_num_head + total_num_content + total_num_end)

    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    #随机抽取bgm
    head_bgm_dir = Path("./bgm/head/")
    content_bgm_dir = Path("./bgm/content/")
    end_bgm_dir = Path("./bgm/end/")
    head_bgm_list = [father_path + "\\" + str(m) for m in head_bgm_dir.glob("*.mp3")]
    content_bgm_list = [father_path + "\\" + str(m) for m in content_bgm_dir.glob("*.mp3")]
    end_bgm_list = [father_path + "\\" + str(m) for m in end_bgm_dir.glob("*.mp3")]

    #根据长度剪裁
    print("根据各段长短剪裁bgm")
    #head bgm
    cmd = "ffmpeg  -y -i %s -t %f  ./bgm/cutted/head.mp3"%(random.choice(head_bgm_list),head_len)
    print(cmd)
    os.system(cmd)
    #content bgm
    cmd = "ffmpeg  -y -i %s -t %f  ./bgm/cutted/content.mp3"%(random.choice(content_bgm_list),content_len)
    print(cmd)
    os.system(cmd)
    #end bgm
    cmd = "ffmpeg  -y -i %s -t %f  ./bgm/cutted/end.mp3"%(random.choice(end_bgm_list),end_len)
    print(cmd)
    os.system(cmd)

    #合并bgm
    print("合并bgm")
    with open("./bgm/cutted//bgm.txt","w") as f:
        f.write("file '" + father_path + "\\bgm\\cutted\\head.mp3" +"'\n")
        f.write("file '" + father_path + "\\bgm\\cutted\\content.mp3" + "'\n")
        f.write("file '" + father_path + "\\bgm\\cutted\\end.mp3" + "'\n")
        f.close()
    cmd = "ffmpeg -y -f concat -safe 0 -i %s -c copy %s" % (father_path + "\\bgm\\cutted\\bgm.txt",father_path+"\\bgm\\cutted\\bgm.mp3")
    print(cmd)
    os.system(cmd)

    #将合并的bgm混入视频
    print("混合bgm")
    cmd="ffmpeg  -y -i ./output/output_title.mp4  -i ./bgm/cutted/bgm.mp3 -filter_complex amix=inputs=2:duration=first:dropout_transition=2   ./output/content.mp4"
    print(cmd)
    os.system(cmd)
    
def add_head_end():
    print("将开头结尾加入最终视频")
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    # 随机抽取bgm
    head_video_dir = Path("./video/head")
    end_video_dir = Path("./video/end")
    head_bgm_list = [father_path + "\\" + str(m) for m in head_video_dir.glob("*.mp4")]
    end_bgm_list = [father_path + "\\" + str(m) for m in end_video_dir.glob("*.mp4")]
    with open("./output/out.txt","w") as f:
        f.write("file '" + random.choice(head_bgm_list) +"'\n")
        #f.write("file '" + father_path+"\\output\\content.mp4" + "'\n")
        f.write("file '" + random.choice(end_bgm_list) + "'\n")
        f.close()
    #"-loglevel quiet"
    cmd = "ffmpeg -i ./video/head/a.mp4 -i ./output/content.mp4 -i ./video/end/a.mp4 -filter_complex '[0:0] [0:1] [1:0] [1:1] [2:0] [2:1] concat=n=3:v=1:a=1 [v] [a]' -map '[v]' -map'[a]'<1> output.mkv"
    cmd = "ffmpeg -y -f concat -safe 0 -i ./output/out.txt -c copy output.mp4"
    print(cmd)
    os.system(cmd)
