
# coding=utf-8

"""  
Created on 2016-10-15 
@author: royrao
功能: 爬取新浪微博的搜索结果
网址：http://s.weibo.com/
实现：采取selenium测试工具，模拟微博登录，结合PhantomJS/Firefox，分析DOM节点后，采用Xpath对节点信息进行获取，实现重要信息的抓取
数据：作者，时间，博文，部分评论
"""

import time
from selenium import webdriver    
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By    
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui        
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import numpy as np

#先调用无界面浏览器PhantomJS或Firefox    
#driver = webdriver.PhantomJS()

driver = webdriver.Firefox(executable_path=r'C:\ProgramData\Anaconda3\Lib\site-packages\selenium\webdriver\firefox\geckodriver.exe')
driver.implicitly_wait(10)
#********************************************************************************
#                            第一步: 登陆login.sina.com
#                     这是一种很好的登陆方式，有可能有输入验证码
#                          登陆之后即可以登陆方式打开网页
#********************************************************************************

def LoginWeibo(username, password):
    try:
        #输入用户名/密码登录
        print('准备登陆Weibo.cn网站...')
        driver.get("http://login.sina.com.cn/")
        elem_user = driver.find_element_by_name("username")
        elem_user.send_keys(username) #用户名
        elem_pwd = driver.find_element_by_name("password")
        elem_pwd.send_keys(password)  #密码
        # elem_sub = driver.find_element_by_xpath("//input[@class='smb_btn']")
        # 2017-06-06 element class changed 
        elem_sub = driver.find_element_by_xpath("//input[@class='W_btn_a btn_34px']")        
        elem_sub.click()              #点击登陆 因无name属性

        try:
            #输入验证码
            time.sleep(10)
            elem_sub.click() 
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

    driver.get("http://s.weibo.com/")
   
    #输入关键词并点击搜索
    
    try:
        item_inp = driver.find_element_by_xpath("//input[@class='searchInp_form']")
        item_inp.send_keys(key)
        item_inp.send_keys(Keys.RETURN)    #采用点击回车直接搜索
    except:
        print(" exception NO INPUT FORM " )

    
    if checkContent():
        try:
            return getStarInfo(key)
        except:
            print(" exception in getSearchContent ==" + key)

#********************************************************************************
#                  辅助函数，考虑页面加载完成后得到页面所需要的内容
#********************************************************************************   

#判断页面加载完成后是否有内容
def checkContent():
    #有内容的前提是有“导航条”？错！只有一页内容的也没有导航条
    #但没有内容的前提是有“pl_noresult”
    try:
        driver.find_element_by_xpath("//div[@class='pl_noresult']")
        flag = False
    except:
        flag = True
    return flag

#判断有没有下一页按钮
def checkNextPage():
    try:
        driver.implicitly_wait(30)
        driver.find_element_by_xpath("//div[@class='W_pages']")
        driver.implicitly_wait(30)
        flag = True
    except:
        flag = False
    return flag


#在页面有内容的前提下，获取内容
def getStarInfo(key):

    result = []
    
    count = 0
    while True: #循环爬取每一页的内容      
        try:            

            post = driver.find_elements_by_xpath("//p[@class='comment_txt']") #微博文字
            nick_name = driver.find_elements_by_xpath("//div/a[@class='W_texta W_fb']") #用户名
            postTime = driver.find_elements_by_xpath("//div/a[@class='W_textb']")
            forward = driver.find_elements_by_xpath("//a[@action-type='feed_list_forward']/span")
            comment = driver.find_elements_by_xpath("//a[@action-type='feed_list_comment']/span")
            like = driver.find_elements_by_xpath("//ul[@class='feed_action_info feed_action_row4']/li/a[@title='赞']/span/em")
            driver.implicitly_wait(30)
            
            for i in range(len(post)):
                result.append((nick_name[i].text, postTime[i].text, post[i].text, (forward[i].text)[2:],(comment[i].text)[2:],like[i].text))
     
            if checkNextPage():
                count = count+1
                print(count)
                page_url = driver.find_elements_by_xpath("//a[@class='page next S_txt1 S_line1']")
                url = page_url[0].get_attribute("href")
                driver.get(url)
                driver.implicitly_wait(30)
                
                # star_weibo_id = current_url.split('/')[3].split('?')[0]            
                # star_fans_num = nodes[1].find_element_by_xpath('.//a').text.split('\n')[0]
                # star_fans_num = nodes[1].find_element_by_xpath('.//a').text
            else:
                print('No next page')
                break 
        except Exception as e:
            print(e)
            print("exception in GetStarInfo ==" + key)
            break
        
    return result


#*******************************************************************************
#                                程序入口
#*******************************************************************************
if __name__ == '__main__':
    
    start = time.clock()
#    定义变量
    username = ''             #输入你的用户名
    password = ''               #输入你的密码

    #操作函数
    LoginWeibo(username, password)       #登陆微博
   #搜索微博
    df_keys = pd.read_excel('C:/Users/tintian2/Documents/Publicis/NLP/weibo/ratingToolEntities.xlsx');
  
    for index, row in df_keys.iterrows():
        key = row[0]
        print(key)

        result = GetSearchContent(key)
        df = pd.DataFrame(result)
        df.to_csv('../weibo/'+key+'.csv',encoding='utf8',header = False, index = False)


    
    elapsed = (time.clock() - start)
    
    print("Time used:", elapsed)
