#微博分月处理
########################################################################################

def cleanTime(date,onlyMonth):
    path='../weibo/save/'+date+'/'
    files = os.listdir(path)
    for file in files:
        df_weibo = pd.read_csv(path+file,header=None,names=['author','time','content'],encoding='utf8',engine='python')

        post_time=[x for x in df_weibo['time']]
        
        for index,item in enumerate(post_time):
            post_time[index]=re.sub('今天',date,item)  #把‘今天’替换成日期
            if re.search('分钟前',item) != None:  #把含有’分钟前‘的项替换为日期
                post_time[index]=date 
            if onlyMonth == True:
                month,rest = re.split('月',item)
                post_time[index]=item[month] #只取月份数字

        df_weibo.drop('time',axis=1,inplace=True)
        df_time = pd.DataFrame(post_time,columns=['month']) #添加上处理后的日期列
        
        df_weibo = pd.concat([df_time,df_weibo],axis=1)
        df_weibo.to_csv('../output/weibo/'+file.strip('.csv')+'.csv',index=None,encoding='utf8')
    
    
    
#提取出某个月份的微博内容
def extractMonth(month):
    path='../output/weibo/'
    files = os.listdir(path)
    for file in files:
        df_weibo = pd.read_csv(path+file,encoding='utf8',engine='python')
        df_weibo = df_weibo.loc[df_weibo['month']==month]
        df_weibo.to_csv('../output/weibo_by_month/'+'weibo'+file.strip('.csv')+month+'月'+'.csv',encoding='utf8')
