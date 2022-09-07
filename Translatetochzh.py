import requests
import pygoogletranslation
"""
POST /v2/translate?auth_key=[yourAuthKey]> HTTP/1.0
Host: api-free.deepl.com
User-Agent: YourApp
Accept: */*
Content-Length: [length]
Content-Type: application/x-www-form-urlencoded

auth_key=[yourAuthKey]&text=Hello, world&target_lang=DE
"""

def deepl(path,name,file_type):
    with open(path+'\\'+name+'.'+file_type)as file:
        text=file.readlines()
    authkey='a'
    lang='Ch-ZH'
    url="http://api-free.deepl.com/v2/translate?auth_key={}&text={}&target_lang={}".format(authkey,text,lang)
    #payload={'text':text,'target_lang':'DE'}
    r=requests.get(url)
    with open(path+'\\'+name+'_t.md','w') as reveived:
        reveived.write(r.content)

def google(path):
    path1=path
    translator=pygoogletranslation.Translator()
    r=translator.bulktranslate(path1,dest='zh-CN')
    return r
