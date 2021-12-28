import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from selenium.common import exceptions as ec

options = Options()
options.add_argument('--headless')
web = Chrome(options=options)
def get_save_goods():
    # 输入要搜索的商品名称
    good_name = input('请输入你要爬取的商品名称:')
    url = f'https://search.jd.com/Search?keyword={good_name}&pvid=e64a90a7e80b47d7b095ff4760c6840d&page=1&s=176&click=1'
    web.get(url)
    # 等待页面加载完毕
    time.sleep(3)
    while True:
        # 获取爬取的页数
        page = web.find_element(By.XPATH, '//*[@id="J_topPage"]/span/b').text
        print(f'开始爬取第{page}页')
        # 获取商品信息的列表
        li_lists = web.find_elements(By.CLASS_NAME, 'gl-item')
        try:
            # 用xpath获取各个商品的信息
            for li_list in li_lists:
                name = li_list.find_element(By.CSS_SELECTOR,'.p-name em').text.replace('\n','')
                join_name = ''.join(name)
                link = 'http:'+li_list.find_element(By.CSS_SELECTOR,'.p-img a').get_attribute('href')
                price = li_list.find_element(By.CSS_SELECTOR,'.p-price i').text
                shop = li_list.find_element(By.CSS_SELECTOR,'.p-shopnum a').text
                comment = li_list.find_element(By.CSS_SELECTOR,'.p-commit a').text
                data = {
                    '商品名称':name,
                    '商品链接':link,
                    '价格':price,
                    '商店名称':shop,
                    '评论': comment
                }
                # 储存到mongodb
                print(data)
                client = MongoClient(host='localhost',port=27017)
                db = client['jd']
                collections = db[good_name]
                collections.insert(data)
        # 捕捉爬取过程的异常,继续爬取
        except:
            continue
        # 爬完100即停止
        if int(page) == 100:
            break
        #     点击下一页
        js = web.find_element(By.XPATH, '//*[@id="J_topPage"]/a[2]')
        web.execute_script("arguments[0].click();", js)
        # 等待加载完毕
        time.sleep(2)
# 调用函数
get_save_goods()