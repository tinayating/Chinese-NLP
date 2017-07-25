#
def cleanTime(date):
    path='../weibo/save/'+date+'/'
    files = os.listdir(path)
    for file in files:
        df_weibo = pd.read_csv(path+file,encoding='utf8',engine='python')

        post_time=[x for x in df_weibo['time']]
        
        for index,item in enumerate(post_time):
            post_time[index]=re.sub('今天',date,item)  #把‘今天’替换成日期
            if re.search('分钟前',item) != None:  #把含有’分钟前‘的项替换为日期
                post_time[index]=date
                
            #将时间转换为标准格式“xxxx-xx-xx”
            post_time[index]=re.sub('月','-',post_time[index])
            post_time[index]=re.sub('日',' ',post_time[index])
            if re.match(r'([1-12]{1,2})(-)([1-31]{1,2})',post_time[index]) == None:
                post_time[index] = '2017-'+post_time[index]
                
        
    
        
        df_weibo.drop('time',axis=1,inplace=True)
        df_time = pd.DataFrame(post_time,columns=['month']) #添加上处理后的日期列
        
        df_weibo = pd.concat([df_time,df_weibo],axis=1)
        df_weibo.to_csv('../output/weibo/'+file.strip('.csv')+date+'.csv',index=None,encoding='utf8')
