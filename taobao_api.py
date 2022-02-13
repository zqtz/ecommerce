import time
import random
import requests
from lxml import etree
import re

# 获取淘宝苹果手机信息并存到文本文档
def get_taobao_detail_and_save_txt():
    # 构造headers信息
    headers = {
        'authority': 's.taobao.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.jianhua.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6',
        'cookie': 'thw=cn; enc=r11OqZMNkZXUWX0pb9N321P3utxthZdXYnuUBgrXKOXXIKwACd%2B6Conuhe3imE3G738Cr9%2F9x1WWi6rLV9aTAA%3D%3D; t=a9bb6e3f5d90b2a759133dfb216b74c4; cna=ZTdgGq8WGx0CAduHPnvuCyf8; lgc=%5Cu5434%5Cu96E8%5Cu6DA600; tracknick=%5Cu5434%5Cu96E8%5Cu6DA600; mt=ci=-1_0; xlly_s=1; sgcookie=E1003BDtAYISHDsUkMng%2Bd9zPcf9OfxJAyWKHM9ujjCeQbnwhHWQatTMoSJSWk4rFFLgtqbLVuv1e8gmv%2BeEb4Dvm5DePoB%2BjtIck9HLKy2AxK7Y9p6ERoxmIlUzr2QbtPb%2F; uc3=nk2=rXvnNO33LNc%3D&vt3=F8dCvU%2B0HNbEiDBkxcs%3D&id2=UojdSdUmZbiH8w%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; uc4=id4=0%40UOBZk9a5KGeY7fv0Rge6adkzkQ%2FE&nk4=0%40r4q2rRkZSIqBZUQTZtHymaFEvA%3D%3D; _cc_=W5iHLLyFfA%3D%3D; _m_h5_tk=be3382f5ba5a9bc44d4d8e507510ceb4_1644726432336; _m_h5_tk_enc=5f0ccc0b3c9626c1d48c12cd84394fcb; uc1=cookie14=UoewBGChXF1VLQ%3D%3D; _tb_token_=0be165b7818e; JSESSIONID=6329526FBBA15417016002733B19F3B4; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; tfstk=c8wFBNGPI9BUT5k5MvMPNqsD5TldZ00oldoqtW6HJDF5yJlhirT-jiajb0-wrXf..; isg=BNfX-DWCeSYRBf57UFxQbz0-ZkshHKt-aEwFxikFu6YlWPSaMe6bz1s-u_jGtIP2; l=eB_V6iHugBBzIw1UBO5ahurza77trIOf1oVzaNbMiInca6g1tEyyGNCn6kI9Sdtxgt5YCetPHDFQZReHWcUU-xgKqelyRs5mpL9wJe1..',
    }
    for page in range(100):
        # 构造请求参数
        params = (
            ('data-key', 's'),
            ('data-value',str(page*44)),
            ('ajax', 'true'),
            ('_ksTS', '1644717093845_728'),
            ('callback', 'jsonp729'),
            ('initiative_id', 'tbindexz_20170306'),
            ('ie', 'utf8'),
            ('spm', 'a21bo.jianhua.201856-taobao-item.2'),
            ('sourceId', 'tb.index'),
            ('search_type', 'item'),
            ('ssid', 's5-e'),
            ('commend', 'all'),
            ('imgfile', ''),
            ('q', '\u82F9\u679C\u624B\u673A'),
            ('suggest', 'history_1'),
            ('_input_charset', 'utf-8'),
            ('wq', ''),
            ('suggest_query', ''),
            ('source', 'suggest'),
            ('bcoffset', '1'),
            ('ntoffset', '7'),
            ('p4ppushleft', '2,48'),
        )
        # 发送请求
        sc = random.randint(1,2)
        time.sleep(sc)
        response = requests.get('https://s.taobao.com/search', headers=headers, params=params)
        print(response.text)
        # 正则匹配要获取的信息
        pat = re.compile('"raw_title":"(.*?)".*?"view_price":"(.*?)".*?"nick":"(.*?)"',re.S)
        results = re.findall(pat,str(response.text))
        for result in results:
            raw_title = result[0]
            view_price = result[1]
            nick = result[2]
            # 获取信息
            data = {
                'raw_title':raw_title,
                'view_price': view_price,
                'nick': nick
            }
            # 打印信息
            print(data)
            # 存储到文本文档
            with open('pg.txt','a',encoding='utf-8')as f:
                f.write(str(data)+'\n')

# 定义主函数
def main():
    get_taobao_detail_and_save_txt()

# 启动主函数
if __name__ == '__main__':
    main()