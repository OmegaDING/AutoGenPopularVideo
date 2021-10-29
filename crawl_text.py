
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests
import urllib.request
import urllib.parse
from lxml import etree

def query(content):
    # 请求地址
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    # 请求头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 发送请求，获得响应
    response = urllib.request.urlopen(req)
    # 读取响应，获得文本
    text = response.read().decode('utf-8')
    # 构造 _Element 对象
    html = etree.HTML(text)
    # 使用 xpath 匹配数据，得到匹配字符串列表
    sen_list = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()')
    # 过滤数据，去掉空白
    sen_list_after_filter = [item.strip('\n') for item in sen_list]
    # 将字符串列表连成字符串并返回
    return ''.join(sen_list_after_filter)



result="默认词条搜索结果"

def getTEXT(keyword = ""):
    print("正在获取文章")
    b = webdriver.Chrome()
    #搜索界面
    b.get('http://baike.baidu.com/')
    search_box = b.find_element_by_id('query')
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)

    try:
        ele = b.find_element_by_xpath("/html/body/div[3]/div[3]/div/div[1]/div/h2")
    except:
        ele = b.find_element_by_xpath("/html/body/div[2]/div[1]/dl/dd/a")
        print("未找到相关词条，关键词条已经更换为：" + ele.get_attribute("textContent"))
        ActionChains(b).move_to_element(ele).perform()
        ele.click()
        b.close()
        b.switch_to.window(b.window_handles[0])
        ele2= b.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/dl[1]/dd/h1")
        keyword = ele2.get_attribute("textContent")  # 更改搜索关键词

    result = query(keyword)
    b.close()
    print("抓取到文章："+result)
    if len(result)<2000:
        result= result
    return result



if __name__ == '__main__':
    print(getTEXT(keyword="原神"))

