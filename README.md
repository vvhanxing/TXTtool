# TXTtool
https://mp.weixin.qq.com/s?__biz=MzAxMjMwODMyMQ==&mid=2456389073&idx=4&sn=851a92db1ce7ad1069da7eaa0c3bfcb4&chksm=8c2effdfbb5976c9d328ab83db6e7ca87590f096ad5a2e728490246a175fe4a3646477f7ede3&mpshare=1&scene=24&srcid=0728cmZaSda3PaVSmmYSUvTM&sharer_sharetime=1658983960007&sharer_shareid=79b7418d9903049653381037970ea1f7&ascene=14&devicetype=android-30&version=280019c9&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&exportkey=A%2B1y9wn64S1hlC5ECiO%2FuMs%3D&pass_ticket=PY1ix229pzDbvYduMpyBm1bRwOJsQf9sIL4Y85z5pm7ZbdDVANYUYCR%2FGDNBYyRm&wx_header=3

def LCS(x,y):
    import numpy as np
    c=np.zeros((len(x)+1,len(y)+1))
    b=np.zeros((len(x)+1,len(y)+1))
    for i in range(1,len(x)+1):
        for j in range(1,len(y)+1):
            if x[i-1]==y[j-1]:
                c[i,j]=c[i-1,j-1]+1
                b[i,j]=2
            else:
                if c[i-1,j]>=c[i,j-1]:
                    c[i,j]=c[i-1,j]
                    b[i,j]=1
                else:
                    c[i,j]=c[i,j-1]
                    b[i,j]=3
    return c,b

def getLCS(x,y):
    c,b=LCS(x,y)
    i=len(x)
    j=len(y)
    lcs=''
    while i>0 and j>0:
        if b[i][j]==2:
            lcs=x[i-1]+lcs
            i-=1
            j-=1
        if b[i][j]==1:
            i-=1
        if b[i][j]==3:
            j-=1
        if b[i][j]==0:
            break
    return lcs


print(getLCS("Hello World"   ,   "Hello-World!"))

def LCSsimilarity(entity,matchList,case_sensitive=False):
    result_list = []
    for match_entity in matchList:
        if case_sensitive:
            LCSchars = getLCS(entity,match_entity)
        else:
            LCSchars = getLCS(lower(entity),lower(match_entity))
        score = len(LCSchars)/ (len(entity)+ (len(match_entity)- len(LCSchars)) )
        result_list.append([entity,match_entity,LCSchars, round( score   ,3) ])
    result_list = sorted(result_list, key=lambda x:-x[-1])
    return result_list
