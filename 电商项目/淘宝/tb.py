import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from selenium import webdriver
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import setting
from selenium.common import exceptions as ex



# window.navigator.webdriver如何设置为undefined

# 设置开发者模式
options = webdriver.ChromeOptions()

# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 设置无头浏览器
options.add_argument('--headless')
web = webdriver.Chrome(options=options)


"""Selenium执行cdp命令调用chrome浏览器的开发者工具，给window.navigator对象定义一个webdriver属性，并且设置为undefined,以绕过js的检测"""
web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

def get_and_save_to_mongo():
    good_name = input('请输入你要爬取的商品名称:')
    url = f'https://s.taobao.com/search?q={good_name}'
    web.get(url)
    # 显形等待登录界面的出现
    WebDriverWait(web,5).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="fm-login-id"]')))
    # 模拟登录
    web.find_element(By.XPATH,'//*[@id="fm-login-id"]').send_keys('你的淘宝账号')
    web.find_element(By.XPATH,'//*[@id="fm-login-password"]').send_keys('密码')
    web.find_element(By.XPATH,'//*[@id="login-form"]/div[4]/button').click()
    # 显式等待爬取页面加载完毕
    WebDriverWait(web,30).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="J_relative"]/div[1]/div/div[2]/ul/li[3]/a/span')))
    page = 1
    while True:
        print(f'开始爬取第{page}页')
        # 用正则匹配各种元素
        div_lists = web.find_elements(By.XPATH,'//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
        try:
            for div_list in div_lists:
                name = div_list.find_element_by_xpath('./div[2]/div[2]/a').text.replace('\n','')
                name = ''.join(name)
                link = div_list.find_element_by_xpath('./div[2]/div[2]/a').get_attribute('href')
                price = div_list.find_element(By.XPATH,'./div[2]/div[1]/div[1]/strong').text
                pay_count = div_list.find_element(By.XPATH, './div[2]/div[1]/div[2]').text
                shop_name = div_list.find_element(By.XPATH, './div[2]/div[3]/div[1]/a/span[2]').text
                location = div_list.find_element(By.XPATH, './div[2]/div[3]/div[2]').text
                data = {
                    'name':name,
                    'link': link,
                    'price': price,
                    'pay_count': pay_count,
                    'shop_name': shop_name,
                    'location': location,
                }
                print(data)
                # 保存到mongodb
                client = MongoClient(host=setting.host, port=setting.port)
                db = client[setting.db]
                collections = db[good_name]
                collections.insert(data)
        except ex.StaleElementReferenceException:
            continue
        # 爬取完100页即停止
        if int(page) == 100:
            break
        # 点击下一页
        js = web.find_element(By.XPATH, '//*[@id="J_relative"]/div[1]/div/div[2]/ul/li[3]/a')
        web.execute_script("arguments[0].click();", js)
        time.sleep(1.5)
        page += 1
get_and_save_to_mongo()



