# !usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import re
import shutil
import time
from urllib.parse import quote,unquote

def getCoding(strInput):
    '''
    获取编码格式
    '''
    try:
        strInput.decode("utf8")
        return 'utf8'
    except:
        pass
    try:
        strInput.decode("gbk")
        return 'gbk'
    except:
        pass
     

paths=os.listdir("./txts")

shutil.rmtree('posts')
os.mkdir('posts')
for path in paths:
    finb=open('./txts/'+path,'rb')
    coding=getCoding(finb.read())
    finb.close()
    fin=open('./txts/'+path,'r',encoding=coding,errors='ignore')
    print(path)
    # os.system('cd blog && ..\hugo.exe new '+("post/"+path[:-3]+"md").replace(' ','_'))
    os.mkdir("./posts/"+quote(path[:-4]))
    fout=open(("./posts/"+quote(path[:-4])+'/index.html'),'w',encoding='utf8')
    lines=fin.readlines()
    fin.close()
    fout.writelines(
    '''
    <html><head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, minimal-ui">
    <link rel="stylesheet" href="https://typo.sofi.sh/typo.css">
    <title>%s</title>
    <style>'''%path[:-4])

    with open('style.css','r',encoding='utf8') as f:
        fout.write(f.read())

    fout.writelines('''</style></head>
    <body>
    <div id="wrapper" class="typo typo-selection">
    <h1>%s</h1>'''%path[:-4])

    for line in lines:
        fout.write('<p>'+line.strip()+'</p>\n')

    fout.writelines('''</div>
    <!-- #wrapper -->
    </body></html>
    ''')

    fout.close()
    
    os.system('.\\go-ipfs\\ipfs.exe add -r posts\\'+quote(path[:-4]))

# os.system('.\\go-ipfs\\ipfs.exe init')

print('开始部署网站：')
res=os.popen('.\\go-ipfs\\ipfs.exe add -r .\\posts')
tempstream = res._stream
text=tempstream.buffer.read().decode(encoding='utf-8',errors='ignore')

finb=open('title.txt','rb')
coding=getCoding(finb.read())
finb.close()
fin=open('title.txt','r',encoding=coding)
lines=fin.readlines()
title=lines[0]
des=lines[1:]

os.mkdir('./posts/index')
fout=open('./posts/index/index.html','w',encoding='utf8')
fout.writelines(
    '''
    <html><head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, minimal-ui">
    <link rel="stylesheet" href="https://typo.sofi.sh/typo.css">
    <title>%s</title>
    <style>'''%title)

with open('style.css','r',encoding='utf8') as f:
    fout.write(f.read())

fout.writelines('''</style></head>
<body>
<div id="wrapper" class="typo typo-selection">
<h1>%s</h1>\n'''%title)
for line in des:
    fout.write('<p>%s</p>\n'%line)
print()
site_hashes=text.split('\n')
for item in site_hashes[:-2]:
    page_hash=item.strip()[6:].split(' ')[0]
    page_name=unquote(item.strip()[6:].split(' ')[1][6:])
    if page_name[-5:]=='.html':
        continue
    print(page_name)
    fout.write('<p><a href=\"%s/">'%('/ipfs/'+page_hash)+page_name+'</a></p>\n')

fout.writelines('''</div>
    <!-- #wrapper -->
    </body></html>
    ''')

fout.close()
res2=os.popen('.\\go-ipfs\\ipfs.exe add -r posts\\index')
tempstream2 = res2._stream
text2=tempstream2.buffer.read().decode(encoding='utf-8',errors='ignore')
site_hash=text2.split('\n')[-2].strip()[6:].split(' ')[0]
print()

# print(site_hashes)
# print(site_hash)
# os.system('.\go-ipfs\ipfs.exe name publish '+site_hash)

gateways=['ipfs.eternum.io',
'gateway.pinata.cloud',
'permaweb.io',
'ipfs.2read.net',
'ipfs.jeroendeneef.com',
'ipfs.privacytools.io',
'ipfs.best-practice.se',
'hardbin.com',
'ipfs.stibarc.com',
'10.via0.com'
,]

print('你的网站的链接如下：（选中右键复制，都试试，挑几个能用的）')
for gateway in gateways:
    print('https://'+gateway+'/ipfs/'+site_hash)
os.system('pause')

print('请耐心等待10分钟以同步网站数据：')
for i in range(600):
    time.sleep(1)
    print("\r[%d/%d]"%(i,600),end='')

os.chdir('tmp')
for gateway in gateways:
    os.popen('..\wget.exe -r -p -np -k '+gateway+'/ipfs/'+site_hash)
