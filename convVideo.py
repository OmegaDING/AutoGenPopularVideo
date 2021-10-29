import random
import subprocess
import os
from pathlib import Path

#将mp3_dir目录下的mp3文件合成一个
import cv2
import shutil


def merge_mp3(mp3_dir: Path, output_mp3=None):
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")

    with open("./read/read.txt","w") as f:
        file_path = father_path+"\\read\\result0.mp3"
        file_num = 0
        while (os.path.exists(file_path)):
            file_path = father_path+"\\read\\result" + str(file_num) + ".mp3"
            f.write("file " + "'" + file_path +"'\n")
            file_num += 1
    f.close()
    cmd = "ffmpeg -y -f concat -safe 0 -i %s -c copy %s" % (father_path+"\\read\\read.txt", output_mp3)
    print(cmd)
    subprocess.run(cmd)

#将mp4连接
#将mp4_dir目录下的mp4文件合成一个
def merge_mp4(mp4_dir: Path, output_mp4=None):
    # #删除之前的output
    # if (os.path.exists("./video/output.mp4")):
    #     os.remove("./video/output.mp4")
    mp4_list = [str(m) for m in mp4_dir.glob("*.mp4")]
    if output_mp4 is None:
        output_mp4 = mp4_dir / ("%s.mp4" % mp4_dir.stem)

    txt = ("file \'{}\'\n"*len(mp4_list)).format(*mp4_list)
    txt_file = mp4_dir / "video.txt"
    txt_file.write_text(txt)
    cmd = "ffmpeg -y -an  -f concat -safe 0 -i %s -c copy %s" % (txt_file, output_mp4)
    print("merge_mp4 : "+cmd)
    subprocess.run(cmd)

#将tts合成保存在/read/下的文件连接
def connect_read():
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    read_path = father_path + "\\read"

    print("连接合成mp3目录"+read_path)
    mp3_dir = Path(read_path)
    #删除之前的output
    if (os.path.exists("./read/output.mp3")):
        os.remove("./read/output.mp3")
    merge_mp3(mp3_dir,output_mp3=read_path+"\\output.mp3")

def add_read_to_video():
    cmd = f'ffmpeg  -i ./read/output.mp3 -i ./video/123.mp4  -codec copy ./srt/123.mp4 -y'
    os.system(cmd)

def convImgToVideo():
    print("将图片转为视频")
    for i in os.listdir(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) ) +os.path.sep +"img" ):
        cmd = "ffmpeg -y -r 30 -f image2 -loop 1 -i ./img/%s  -s 1920x1080 -pix_fmt yuvj420p -t 1.5 -vcodec libx264 ./video/img/%s.mp4"%(i,i.split('.')[0])
        print(cmd)
        os.system(cmd)

#将content中的video连接,保存到video/final #抛弃声音
def connect_video():
    print("正在将content中的video连接保存到final")
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    imgVideo_path = father_path + "\\video\\content"
    mp4_dir = Path(imgVideo_path)
    merge_mp4(mp4_dir, output_mp4=father_path + "\\video\\final\\output.mp4")

def crop_video(inpath : str , outpath :str):
    cmd = "ffmpeg -y -i %s -vf crop=iw/2:ih/2 %s"%(inpath,outpath)
    print(cmd)
    os.system(cmd)


def crop_cutted_video():
    print("开始剪彩视频图像大小-center")
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    bilibiliVideo_path = father_path + "\\video\\cutted"
    bilibili_dir = Path(bilibiliVideo_path)

    bilibili_list = [str(m) for m in bilibili_dir.glob("*.mp4")]
    bilibili_list.extend([str(m) for m in bilibili_dir.glob("*.flv")])
    txt = ("\'{}\'\n" * len(bilibili_list)).format(*bilibili_list)

    num=0
    for i in bilibili_list:
        print("裁剪视频图像-center："+i)
        name = i.split(".")[-1]
        crop_video(inpath=i, outpath="./video/croped/"+str(num) + "."+name)
        num += 1


def resize_croped_video():
    print("开始resize视频")
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    cropVideo_path = father_path + "\\video\\croped\\"
    crop_dir = Path(cropVideo_path)

    crop_list = [str(m) for m in crop_dir.glob("*.mp4")]
    crop_list.extend([str(m) for m in crop_dir.glob("*.flv")])
    txt = ("\'{}\'\n" * len(crop_list)).format(*crop_list)

    num=0
    for i in crop_list:
        print("resize视频："+i)
        name = i.split(".")[0]
        cmd="ffmpeg -y -i "+ i +" -vf scale=1920:1080 ./video/resized/"+str(num)+".mp4 -hide_banner"
        print(cmd)
        os.system(cmd)
        num += 1


def get_video_duration(filename):
  cap = cv2.VideoCapture(filename)
  if cap.isOpened():
    rate = cap.get(5)
    frame_num =cap.get(7)
    duration = frame_num/rate
    return duration
  return -1


def cut_bilibili_video(part = 5, each_len = 10):
    print("开始剪裁视频片段")
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    bilibiliVideo_path = father_path + "\\video\\bilibili"
    bilibili_dir = Path(bilibiliVideo_path)

    bilibili_list = [str(m) for m in bilibili_dir.glob("*.mp4")]
    bilibili_list.extend([str(m) for m in bilibili_dir.glob("*.flv")])

    for list in bilibili_list:
        video_len = get_video_duration(list)
        print("开始剪裁："+list +" 总长度：" + str(video_len))
        video_len -= each_len;

        start_point={}
        for x in range(part):#每个视频抽几段
            start_point[x] = video_len / part  * (x+1)

        print(start_point)
        for j in range(part):
            cut_path = father_path + "\\video\\cutted\\0.mp4"
            file_num = 0
            while (os.path.exists(cut_path)):
                file_num += 1
                cut_path = father_path + "\\video\\cutted\\" + str(file_num) + ".mp4"
            cmd="ffmpeg -y -i %s -ss %d -t %d %s"%(list,int(start_point[j]),each_len,cut_path)
            print(cmd)
            os.system(cmd)

def final_material():
    print("正在将素材打乱保存到content")
    if(os.path.exists("./video/content")):
        shutil.rmtree("./video/content")
    os.mkdir("./video/content")

    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")

    resized_dir = Path("./video/resized/")
    material_list = [father_path +"\\"+str(m) for m in resized_dir.glob("*.mp4")]
    material_list.extend([father_path +"\\"+str(m) for m in resized_dir.glob("*.flv")])

    # img_video_dir = Path("./video/img/")
    # material_list.extend([father_path +"\\"+str(m) for m in img_video_dir.glob("*.mp4")])
    # material_list.extend([father_path + "\\" + str(m) for m in img_video_dir.glob("*.flv")])
    random.shuffle(material_list)
    num=0
    for i in material_list:
        shutil.copy(src=i,dst="./video/content/" +str(num)+".mp4")
        num+=1

#获取目录下所有 文件名
def file_name(file_dir):
         for root, dirs, files in os.walk(file_dir):
             print(root) #当前目录路径
             print(dirs) #当前路径下所有子目录
             print(files) #当前路径下所有非目录子文件



def conv_video():
    #连接读好的语音
    connect_read()
    # 将爬到的图转换为视频
    convImgToVideo()
    # 连接爬好的图

    #将连接完的语音加入视频
    add_read_to_video()

    #剪裁片段
    #将视频建材为片段
    cut_bilibili_video()

    #剪裁视频
    #将片段视频裁剪图像中间的部分
    crop_cutted_video()

    #resize 到1920 1080
    resize_croped_video()

    #将视频，保存到content
    final_material()

    #连接content中的视频,打乱,保存至final
    connect_video()
