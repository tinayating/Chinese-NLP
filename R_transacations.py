# transform text into transaction records


def deleteWordList():
    delete=[]
    with codecs.open("../test/deleteWordList.csv",'r','utf8') as f:
        for line in f.readlines():
            line = line.strip('\r\n')
            delete.append(line)
   return delete

def pyToTransactions(deleteWords):
    jieba.load_userdict("dict.txt")
    df = pd.read_csv("../output/text/All.csv")
    lineNames = []

    for row in df['content']:
        poss = pseg.cut(row)
        lineNames.append(set()) #remove duplicate
        for w in poss:
            if w.flag not in ['n','nr','ns','nt','a','ad','an'] or len(w.word)<2: 
                continue
            if w.word not in deleteWords:
                lineNames[-1].add(w.word)

    with codecs.open("../output/output_n.csv","w","utf8") as f:
        for wordSet in lineNames:
            for word in wordSet:
                f.write(word+'h,')
            f.write('\r\n')

