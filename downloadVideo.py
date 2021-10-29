from you_get import common

url = "https://www.bilibili.com/video/BV16b4y1S7J5"

common.any_download(url=url,stream_id='mp4',info_only=False,output_dir=r'./',merge=True)
