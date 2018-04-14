# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 17:01:12 2018

@author: tdbr
"""

import sqlite3
sql = sqlite3.connect(r'/data/data/com.kanshushenqi.ebook.app/databases/JW_BOOK_3.db')
sqlc=sql.cursor()
sqlc.execute('SELECT name,author,desc_lpcolumn,collectid,booktype,progress,max FROM collectbook')
sqldata=sqlc.fetchall()
sqlc.execute('SELECT name,novelid,oid,rollname,hascontent FROM chapterbean')
sqldata2=sqlc.fetchall()
sqlc.close()
sql.close()
#%%
bookInfo=list(map(lambda i:{'name':i[0],'author':i[1],'desc':i[2],'id':int(i[3]),'count':int(i[5])},sqldata))
chapterInfo=list(map(lambda i:{'name':i[0],'noveid':int(i[1]),'fid':int(i[2]),'rollname':i[3]},sqldata2))
del sqldata
del sqldata2
for chapter in chapterInfo:
    chapter['isroll']=chapter['fid']>pow(10,8)
del chapter
#%%
import os
outdir=r'/sdcard/0000/book'
indir=r'/sdcard/Android/data/com.kanshushenqi.ebook.app/files/books'
try:
    os.chdir(outdir)
except:
    os.mkdir(outdir)
logFile=open('log.txt',mode='w',encoding='utf-8')
process=0
for book in bookInfo:
    process+=1
    os.chdir(outdir)
    chapters=list(filter(lambda i:(i['noveid']==book['id']),chapterInfo))
    rolls=list(filter(lambda i:(i['isroll']==True),chapters))
    chapters=dict(map(lambda i:(i['fid'],i),chapters))
# =============================================================================
#     rolls=dict(map(lambda i:(i['fid'],i['rollname']),rolls))
# =============================================================================
    print(str(process)+'/'+str(len(bookInfo))+':'+book['name'])
    file=open(book['name']+'.txt',mode='w',encoding='utf-8')
    try:
        file.write('书名：'+book['name']+'\n'+
            '作者：'+book['author']+'\n'+
            '简介：'+book['desc']+'\n'
            )
    except:
        logFile.write('in bookInfo : '+book['name']+' miss author or desc!\n')
    indexlist=list(chapters.keys())
    indexlist.sort()
    try:
        os.chdir(indir+os.path.sep+str(book['id'])+os.path.sep+'1')
    except:
        logFile.write(book['name']+' miss dir!\n')
        continue
    count=0
    for i in indexlist:
        chapter=chapters[i]
        if count==book['count'] or chapter['fid']>pow(10,8):
            break
        try:
            content=open(str(chapter['fid'])+'.txt',mode='r',encoding='utf-8').readlines()
            file.write('\n'+chapter['rollname']+' '+chapter['name']+'：\n')
            file.writelines(content)
            file.write('\n')
            count+=1
        except OSError as reason:
            logFile.write('in bookInfo : '+book['name']+' miss file : '+str(reason)+'\n')
    file.close()