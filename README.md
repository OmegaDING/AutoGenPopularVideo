=======
### AutoGenPopularVideo
Automatically generate popular videos



## preface

After watching bilibili and YouTube for a long time, I found that there are many videos that can be automatically generated by computers.
I spent some time writing an automated video project.
It can automatically capture the current hot spots, and collect the corresponding pictures, entries, articles, videos and other information, and integrate them into a manuscript for the computer to read automatically, and the collected video images and other information processing into a video.
Video effects can be seen in my Bilibili:

## Directions：

Make sure you have chrome Driver configured and Requirements installed before using it

Obtain apiKEY and Secret KEY from Baidu open AI platform and fill in tts.py

In main.py, you can change the hotword value. If you want to specify the hotword value, you can change the hotword value 

The read word in the read folder can be edited as head.txt and end.txt

The head and end videos and background music in the folder are randomly selected to add to the video, and to increase selection, simply add the file to the appropriate folder.

Finally, run Python main.py





## The principle：

1. the program will first get the hotword on bilibili and save to bilibilihotword.csv

2. it will crawl the baidu-zhidao and bilibili video as the text and  video material. 

3. it will converage the text to read audio and cut crop the video 

4. it will combine the cutted video and connected audio 

5. it will add the srt to the video and add the head and end selected from the relatived folder

   

##  There are still many problems:

Ffmpeg often has problems connecting videos
Unusable video clips may be captured during random video clips
Crawl Baidu entry may not have the corresponding appropriate entry, need to manually modify



## 前言：
博客地址：http://www.dkyblog.top/index.php/archives/146 （还没写完，会慢慢补充，欢迎各位提出issue）
​		在经过长期的bilibili以及YouTube观看之后发现很多视频完全可以让计算机自动生成。有感而发花了一些时间写了一个自动制作视频的项目。它可以自动抓取当下的热点，并且搜集相应的图片、词条、文章、视频等资料，并将它们整合成一篇文稿让计算机自动朗读，并且将收集到的视频图像等资料加工合成视频。视频效果可以参阅我的bilibili：



## 使用说明

使用前首先确保你已经配置了相应版本的chrome-driver，并且安装了requirements

在百度开放ai平台获取apiKEY 和secret KEY并填入tts.py

在main.py中可以调整hotword是否为自动爬取值，若想指定hotword值可以在注释锄修改

read文件夹中的read word可以被编辑为head.txt和end.txt

文件夹中的头视频和结束视频以及背景音乐将随机抽选添加到视频中，如若想增加选择，只需将文件加入相应文件夹。

最终运行 python main.py即可



## 原理：

1. 该程序将首先获取bilibili上的热词，然后保存到bilibilihotword.csv

2. 它将抓取百度知道和哔哩哔哩视频作为文本和视频素材。

3. 它将聚合文本来阅读音频和剪切剪辑视频

4. 它将把剪切的视频和连接的音频结合起来

5. 它会将SRT添加到视频中，并添加从相关文件夹中选择的头部和尾部

   

## 当前依然有很多问题：

   ffmpeg在连接视频时经常出现各种问题
   在随机截取视频片段时可能截取到不能用的片段
   抓取百度词条时可能没有相应合适的词条，需要手动修改

