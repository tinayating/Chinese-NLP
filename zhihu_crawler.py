# coding=utf-8

"""  
Created on 2017-06-13 
@author: YatingTian
功能: 爬取知乎的搜索结果
网址：http://s.weibo.com/
实现：采取selenium测试工具，模拟知乎登录，结合PhantomJS/Firefox，分析DOM节点后，采用Xpath对节点信息进行获取，实现重要信息的抓取
参考：royrao的代码
"""

import time
import datetime
import re            
import os    
import sys  
import codecs  
import shutil
import urllib 
from selenium import webdriver        
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui      
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.common.action_chains import ActionChains
import xlwt
import pandas as pd
import numpy as np
import pdb
#先调用无界面浏览器PhantomJS或Firefox    
#driver = webdriver.PhantomJS()
driver = webdriver.Firefox(executable_path=r'C:\ProgramData\Anaconda3\Lib\site-packages\selenium\webdriver\firefox\geckodriver.exe')

#********************************************************************************
#                            第一步: 登陆zhihu.com/#signin
#                     这是一种很好的登陆方式，有可能有输入验证码
#                          登陆之后即可以登陆方式打开网页
#********************************************************************************
#可以不需要登陆
def LoginWeibo(username, password):
    try:
        #输入用户名/密码登录
        print('准备登陆zhihu.com网站...')
        driver.get("https://www.zhihu.com/#signin")
        elem_user = driver.find_element_by_name("account")
        elem_user.send_keys(username) #用户名
        elem_pwd = driver.find_element_by_name("password")
        elem_pwd.send_keys(password)  #密码
        # elem_sub = driver.find_element_by_xpath("//input[@class='smb_btn']")
        # 2017-06-06 element class changed 
        elem_sub = driver.find_element_by_xpath("//button[@class='sign-button submit']")    
        # elem_sub.click()     

        try:
            #输入验证码
            time.sleep(10)
            elem_sub.click() #点击登陆 因无name属性
        except: 
            #不用输入验证码
            pass

        #获取Coockie 推荐资料：http://www.cnblogs.com/fnng/p/3269450.html
        print( 'Crawl in ' + driver.current_url)
        print('输出Cookie键值对信息:')
        for cookie in driver.get_cookies(): 
            print(cookie)
            for key in cookie:
                print( key )
                print( cookie[key] ) 
        print('登陆成功...')
    except Exception:      
        print( "Error: ")
    finally:    
        print('End LoginWeibo!\n')


 

#********************************************************************************
#                  第二步: 访问http://s.weibo.com/页面搜索结果
#               输入关键词, 得到 搜索人的 ID, 粉丝数
#********************************************************************************    
# PYTHON 2 / 3 对字符 ENCODE 不同
# PYTHON 3 默认已是 UNICODE 编码

def GetSearchContent(key):

    time.sleep(10)
    #输入关键词并点击搜索
    try:
#        item_inp = driver.find_element_by_xpath("//input[@class='zu-top-search-input']")
        item_inp = driver.find_element_by_xpath("//input[@class='Input']") #xpath变了
        item_inp.send_keys(key)
        item_inp.send_keys(Keys.RETURN)    #采用点击回车直接搜索
        driver.implicitly_wait(30)
        return getInfo()
    except:
        print(" exception NO INPUT FORM " )







#********************************************************************************
#                  第三步，考虑页面加载完成后得到页面所需要的内容
#********************************************************************************   

#在页面有内容的前提下，获取内容
def checkNextPage():
    try:
        driver.find_element_by_xpath("//a[@class='zg-btn-white zu-button-more']")
        flag = True
    except:
        flag = False
    return flag


def getInfo():
    # searchUrl = 
    # driver.get(searchUrl)
    #寻找 SEARCH_DIRECTAREA 微博class
    # 关注 粉丝 微博
    result = []
    expand_url = []
    

    while True:
        time.sleep(5)
        try:
            next_button = driver.find_element_by_xpath("//a[@class='zg-btn-white zu-button-more']")
            next_button.click()
            driver.implicitly_wait(30)
        except:
            print('exception in finding next page')
            break
        
    try:
        expand = driver.find_elements_by_xpath("//a[@class='toggle-expand inline']")
        for i in range(len(expand)):
            expand_url.append(expand[i].get_attribute("href"))   
        print("url num: " + str(len(expand_url)))
        for j in range(len(expand_url)):
            time.sleep(10)
            driver.get(expand_url[j])
            content = driver.find_elements_by_xpath("//span[@class='RichText CopyrightRichText-richText']")
            post_time = driver.find_elements_by_xpath("//div[@class='ContentItem-time']/a")
            for k in range(len(content)):
                result.append((content[k].text,(post_time[k].text)[4:]))
                
    except Exception as e:
        print(e)
        print(" exception in GetInfo ==")

    
    return result

# def getContent():
    

#     # df = pd.DataFrame(content)
#     # df.to_csv('C:/Users/tintian2/zhihu.txt', encoding='utf-8', index = False, header = False)
#     # pdb.set_trace()
    
#     return content
#*******************************************************************************
#                                程序入口
#*******************************************************************************

if __name__ == '__main__':

    start = time.clock()
    username ='492611036@qq.com'
    password ='tyt123456'
    LoginWeibo(username, password) 
    
    df_final = []
    df_keys = pd.read_excel('../zhihu/list.xlsx')
#    key = '苏菲卫生巾'
    
    for index, row in df_keys.iterrows():
        key = row[0]
        print(key)
        result = GetSearchContent(key)
        df = pd.DataFrame(result)
        df.to_csv('../output/zhihu/' + key +'.csv', encoding='utf-8', index = False, header = False)

    
#    GetSearchContent(key)
#    info = getInfo()
    
	    
 
    elapsed = (time.clock() - start)
    
    print("Time used:", elapsed)
    
