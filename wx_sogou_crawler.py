
# coding=utf-8

"""  
Created on 2016-11-06 
@author: royrao
功能: 爬取搜狐微信的搜索结果
网址：http://weixin.sogou.com/
实现：采取selenium测试工具，结合PhantomJS/Firefox，分析DOM节点后，采用Xpath对节点信息进行获取，实现重要信息的抓取
数据：日期，作者，题目，文章
"""

import time

from selenium import webdriver        
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui        
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import numpy as np
import csv
import pdb
#先调用无界面浏览器PhantomJS或Firefox    
#driver = webdriver.PhantomJS(executable_path=r'C:\ProgramData\Anaconda3\Lib\site-packages\selenium\webdriver\firefox\geckodriver.exe')
driver = webdriver.Firefox(executable_path=r'C:\ProgramData\Anaconda3\Lib\site-packages\selenium\webdriver\firefox\geckodriver.exe')

# 手工在浏览器界面点击 登录
# 2017-06-06 NO LOGIN FRAME, ONLY BARCODE LOGIN
def LoginSogou(username, password):
    try:
        #输入用户名/密码登录
        print('准备登陆 sogou 网站...')
        driver.get('http://weixin.sogou.com')

        login_button = driver.find_element_by_xpath("//a[@id='loginBtn']")
        login_button.click()
        #登录表单在页面的框架中，所以要切换到该框架
        iframe1 = driver.find_element_by_tag_name("iframe")
        driver.switch_to_frame(iframe1)
        iframe2 = driver.find_element_by_tag_name("iframe")
        driver.switch_to_frame(iframe2)
        #通过使用选择器选择到表单元素进行模拟输入和点击按钮提交
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys(username)
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(password)
        driver.find_element_by_id('login_button').click()
        

    except Exception:      
        print( "Error: ")
    finally:    
        print('End LoginSogou!\n')

def GetSearchContent(key):

    SEARCH_URL = "http://weixin.sogou.com/"
    driver.get(SEARCH_URL)

    print( '搜索：'+ key )

    #输入关键词并点击搜索
    # item_inp = driver.find_element_by_xpath("//input[@id='upquery']")
    # 2017-06-06 ID changed
    item_inp = driver.find_element_by_xpath("//input[@id='query']")
    item_inp.send_keys(key)
    item_inp.send_keys(Keys.RETURN)
    
    processPage(key)   #处理当前页面内容  
      
#页面加载完成后，对页面内容进行处理
def processPage(key):

    # EVERY 10 seconds, change as needed
    TIMER = 10
    while True:
        time.sleep(TIMER)
        hasResult = checkContent()
        hasNext = checkNext()
        if hasNext:
            next_page_url = driver.find_element_by_xpath("//a[@id='sogou_next']").get_attribute("href")
        #Get ONE Page Content
        if hasResult:
            getPageContent(key)
        else:
            print( "no Content")
            break
        
        #THEN get NEXT Page
        if hasNext:
            driver.get(next_page_url)
        else:
            print( "no Next")
            break

        

#判断页面加载完成后是否有内容
def checkContent():
    try:
        # driver.find_element_by_xpath("//div[@class='no-sosuo']")
        # 2017-06-06 web page change
        driver.find_element_by_xpath("//div[@id='noresult_part1_container']")
        flag = False
    except:
        flag = True
    
    return flag

#判断是否有下一页按钮
def checkNext():
    try:
        driver.find_element_by_xpath("//a[@id='sogou_next']")
        driver.implicitly_wait(30)
        flag = True
    except:
        flag = False
    print("CHECKnext RESULT ==%s" %flag)

    return flag

#在页面有内容的前提下，获取内容
def getPageContent(key):

    RESULT_FILE_NAME = '../wx_sogou/'+ key + '.csv'
    article_urls = []

    article_date = 0
#    article_readNum = 0
#    article_likeNum = 0
    article_author = 0
    article_title = 0

    try:
        
        article_nodes = driver.find_elements_by_xpath("//div[@class='txt-box']/h3/a")
        for i in range(len(article_nodes)):
            try:
                #2017-01-09 ONLY scrape articles when Title Match
#                if article_nodes[i].get_attribute("text").find(key) != -1:
                article_urls.append(article_nodes[i].get_attribute("href"))
            except:
                print("exception in %d" %i)

        #Loop through EACH link to get the details

        for j in range(len(article_urls)):
            try:
#                time.sleep(10)
                article_url = article_urls[j]            
                driver.get(article_url)
                    
                article_date = driver.find_element_by_xpath("//em[@id='post-date']").text
                
                # article_readNum = driver.find_element_by_xpath("//span[@id='sg_readNum3']").text
                
                # article_likeNum = driver.find_element_by_xpath("//span[@id='sg_likeNum3']").text
                
                article_author = driver.find_element_by_xpath("//a[@id='post-user']").text
                
                article_title = driver.find_element_by_xpath("//h2[@id='activity-name']").text

                article_content = driver.find_element_by_xpath("//div[@id='js_content']").text
                driver.implicitly_wait(30)
                
#                writer = pd.ExcelWriter('../wx_sogou/'+ key +'.xlsx',engine='openpyxl')
#                result.append((str(article_date), str(article_author), str(article_title), article_content))
#                df = pd.DataFrame(result,columns=('date','author','title','text'))
#                df.to_excel(writer, sheet_name = 'Sheet1')
                result_out = open(RESULT_FILE_NAME, 'a',  encoding='utf-8')
                mywriter = csv.writer(result_out)
                mywriter.writerow((str(article_date), str(article_author), str(article_title), article_content))
                result_out.close()
                
#
#                   
            except:
                print(" EXCEPTION IN URL ==" + article_url )
                
          
    except:
        print(" EXCEPTION IN PAGE Processing") 
       
    
#*******************************************************************************
#                                程序入口
#*******************************************************************************
if __name__ == '__main__':

    #定义变量
    username = '151XXXXXXX'             #输入你的用户名
    password = 'XXXXXX'               #输入你的密码

    #操作函数
    # LoginSogou(username, password)       #登陆

    #READ IN ALL DRAMAS

    key_FILE = '../wx_sogou/list.xlsx'
    df_dramas = pd.read_excel(key_FILE, sheetname=0);

    #每次定义少量数据来抓取
    
    for index, row in df_dramas.iterrows():
        key = str(row[0])
        print(key)
        d1 = GetSearchContent(key)
  
#        dres = pd.DataFrame(d1, columns = ('date','author','title','content'))
#
#        writer = pd.ExcelWriter('../wx_sogou/'+ key +'.xlsx')
#        dres.to_excel(writer,'Sheet1')
