from bs4 import BeautifulSoup
import time
from lxml import etree
from urllib.request import urlopen
resp = open("C:\\Users\\kwind\\Downloads\\flomo\index.html",'r', encoding='utf-8')
cont=resp.read()
print(cont)
import sqlite3
tree=etree.HTML(cont)
title_spans = tree.xpath('//div[@class="memo"]')

soup=BeautifulSoup(cont,features="lxml")
totalresult=soup.find_all(name='div',attrs={"class":"memo"})
imgresult=soup.find_all(name='img')


# ÐèÒª½« soupÄæÐò


memoid=len(totalresult)
resourceid=len(imgresult)

conn = sqlite3.connect('memos_prod.db')
cursor = conn.cursor()
creatorid=1



formatStr = "%Y-%m-%d %H:%M:%S"


for i in totalresult:
    
    a=i.find_all(name='div',attrs={"class":"time"})
    b=i.find_all(name='div',attrs={"class":"content"})
    c=i.find_all(name='div',attrs={"class":"files"})
    d=i.find_all(name='img')
    startTimeStr = a[0].text
    tmObject = time.strptime(startTimeStr, formatStr)
    ts = time.mktime(tmObject)




    cursor.execute('insert into memo (id,creator_id,created_ts,updated_ts,row_status ,content,visibility) values (?,1,?,?,"NORMAL",?,"PRIVATE")',(memoid,ts,ts,b[0].text))
    
    if c[0].contents!=[]:
        
        for j in c[0].contents:
        
            filepath="/var/opt/memos/assets/"+j.attrs["src"] 
     
        

            cursor.execute('insert into resource (id,creator_id,created_ts,updated_ts,filename,internal_path,type,memo_id) values (?,1,?,?,"NORMAL.png",?,"image/png",?)',(resourceid,ts,ts,filepath,memoid))
            conn.commit()

            resourceid=resourceid-1

    
    conn.commit()
    memoid=memoid-1
    x=2;


#cursor.execute('insert into user12 (id, name) values (\'2\', \'Michael\')')    



conn.commit()
cursor.close()


    
a=1