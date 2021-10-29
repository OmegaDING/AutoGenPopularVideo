import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


def getVideoURL(keyword = "",num=1):
    b = webdriver.Chrome()
    #搜索界面
    b.get('http://www.bilibili.com/')
    url={}
    #
    ele = b.find_element_by_xpath("//*[@id=\"i_cecream\"]/div[1]/div[1]")
    ActionChains(b).move_to_element(ele).perform()
    ele.click()
    #
    time.sleep(3)
    search_box = b.find_element_by_xpath("//*[@id=\"nav-searchform\"]/input")
    search_box.send_keys(keyword)
    time.sleep(1)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    for i in range(num):
        try:
            b.switch_to.window(b.window_handles[1])
            #默认第一个视频
            ele = b.find_element_by_xpath("//*[@class=\"video-list clearfix\"]/li[%s]/div[1]/div[1]/a"%(i+1))
            ActionChains(b).move_to_element(ele).perform()
            time.sleep(0.5)
            ele.click()

            time.sleep(0.5)
            b.switch_to.window(b.window_handles[2])
            url[i] = b.current_url
            time.sleep(5)
            b.close()
        except:
            time.sleep(10)
            print("下载b站视频出错")
            # 关闭之前剩余的页面
            pages = b.window_handles
            for handle in pages:
                b.switch_to.window(handle)
                b.close()

    # 关闭之前剩余的页面
    pages = b.window_handles
    for handle in pages:
        b.switch_to.window(handle)
        b.close()
    return url

def crawl_bilibili(keyword : str,num : int):
    print("正在爬取b站视频，keyword：" + keyword +" num: " +str(num))
    url = getVideoURL(keyword,num)
    print(url)
    for i in range(len(url)):
        cmd = "you-get -o ./video/bilibili -O %d -f "%(i) + str(url[i])
        print(cmd)
        try:
            os.system(cmd)
        except:
            os.system(cmd)


if __name__ == '__main__':
    #下载搜索到的视频
    crawl_bilibili("原神",2)