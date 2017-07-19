
def extractText(fileName,post_time):
    
    WEIBO_FILE_PATH = "../weibo/save/"+fileName+".csv"
    WX_FILE_PATH = "../wx_sogou/save/"+fileName+".csv"
    ZHIHU_FILE_PATH = "../zhihu/save/"+fileName+".txt"
    
    if(os.path.exists(WEIBO_FILE_PATH)):
        df_weibo = pd.read_csv(WEIBO_FILE_PATH,header = None
                               , encoding='utf8',engine='python')
        if(post_time == True):
            df_new = pd.concat([df_weibo[1],df_weibo[2]],axis=1) #时间和博文 time&content
        else:
            df_new=df_weibo[2]
            
    if(os.path.exists(WX_FILE_PATH)):
        df_wx = pd.read_csv(WX_FILE_PATH,header = None, encoding='utf8',engine='python')
        if(post_time == True):
            df_new = pd.concat([df_wx[0],df_wx[3]],axis=1)
        else:
            df_new = df_new.append(df_wx[3])
    if(os.path.exists(ZHIHU_FILE_PATH)):


        df_zhihu = pd.read_csv(ZHIHU_FILE_PATH,header = None, encoding='utf8',engine='python')
        df_new = df_new.append(df_zhihu[0])
    
    df_new.to_csv("../output/text/"+fileName+".csv",header = None, index = None, encoding='utf8')

    #合并所有文件
def combineAll(path):
#    path="../output/text"
    files = os.listdir(path)
    df_combined=pd.DataFrame()
    for file in files:
        print(file)
        df = pd.read_csv(path+file,header = None, encoding='utf8', engine='python')
        df_combined = df_combined.append(df)
    
    df_combined.to_csv(path+file+"output.csv",header=None,index=None,encoding='utf8')
