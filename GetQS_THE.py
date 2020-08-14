# -*- coding: utf-8 -*-
import time
import requests
#引用beautifulsoup解析得到的网页
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

#引用selenium操控浏览器
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #引入键盘事件
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#region MongoDB配置
conn = MongoClient('localhost',27017)
db =conn['QSTHERanking'] #建立数据库
my_set_QS = db['QSRanking2020'] #集合相当于表
#endregion
#region Selenium浏览器启动配置
options = webdriver.ChromeOptions()
options.add_argument('no-sandbox')
options.add_argument('user-agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"')
driver = webdriver.Chrome(executable_path = 'chromedriver.exe', options=options)
url = 'https://www.qschina.cn/university-rankings/world-university-rankings/2020'
#endregion


# get直接返回，不再等待界面加载完成
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
# 不能以包的文件名学前端
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
# }
def get_data():  #爬取网页、解析
    driver.get(url)  # 打开浏览器 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="popup-buttons"]/button[2]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div[2]/main/section/div/section/div/div/article/div/div[2]/div/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[1]/label/span[2]/span[2]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div[2]/main/section/div/section/div/div/article/div/div[2]/div/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[1]/label/span[2]/div/div/span/span/ul/li[5]/span').click()
    time.sleep(10)
        # html = requests.get(url=url,headers=headers)#获得请求页
        # print(html)
        # m = driver.find_element_by_id("ShippingMethod")  处理下拉框
        # m.find_element_by_xpath("//option[@value='10.69']").click()
    soup_all = bs(driver.page_source, 'html.parser')
    soup_boxes = soup_all.find_all("tr",class_ = ['odd','even'])
    # print(soup_boxes)
    for box in soup_boxes[0: 150]:
        print('*'*100)
        rank = box.find('td', class_='rank').text
        name = box.find('a', class_='uni-link').text
        location = box.find('div', class_='location').text
        grade_overall = box.find('td', class_='overall sorting_1').text
        citationPstuff = box.find('td', class_='ind-0').text
        IntStudent = box.find('td', class_='ind-1').text
        IntStuff = box.find('td', class_=None).find('div', class_='td-wrap').text
        print(rank, name, location, grade_overall, citationPstuff, IntStudent, IntStuff)
    #         star = 0
        try:
    #             star = int((box.find('span',class_='rating').attrs['class'][0].split("star")[1]))//10
    #         except Exception as e:
    #             print(e)
    #             star = 0
    #         print(star)
            my_set_QS.insert_one({'rank': rank, 'name': name,'location':location,
                                  'citationPstuff':citationPstuff,'IntStudent':IntStudent,
                                  'IntStuff':IntStuff})
    #         time.sleep(1)
    #         print('插入数据成功！')
    # for i in range(1,11):
    #     print(get_url('30299515',i))
        except:
            return

if __name__ == '__main__':
    get_data()