import urllib
import urllib.request
import os
import re
import sys
import time

#http连接有问题时候，自动重连  
def conn_try_again(function):  
    RETRIES = 0  
    #重试的次数  
    count = {"num": RETRIES}  
    def wrapped(*args, **kwargs):  
        try:  
            return function(*args, **kwargs)  
        except Exception as err:  
            if count['num'] < 5:  
                count['num'] += 1  
                return wrapped(*args, **kwargs)                    
            else:
                print("Main Exception Catch")
                raise Exception(err)  
    return wrapped  
 
def schedule(a,b,c):
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)

@conn_try_again 
def getHtml(url):
    try:
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        request = urllib.request.Request(url, data = None, headers = headers)
        page = urllib.request.urlopen(request, timeout = 3)
        html = page.read()
        html = html.decode('utf-8')
        return html
    except Exception as e:
        print('getHtml Eroor:' + e)
        raise e

@conn_try_again 
def downloadImg(html, num, foldername):
    try:
        picpath = 'gwgif'
        if not os.path.exists(picpath):
            os.makedirs(picpath)
        target = picpath+'/%s_%s.gif'% (foldername.replace("-",""), num)
        #如果已存在则跳过下载
        if not os.path.exists(target):
            myItems = re.findall('<p><img src="(.*?)" /></p>',html,re.S)
            #print("myItems_len:" + str(len(myItems)))
            print('Downloading image to location: ' + target)
            if len(myItems) > 0:
                urllib.request.urlretrieve(myItems[0], target, schedule)
                time.sleep(1)
        else:
            print('jump next')
    except Exception as e:
        print('DownLoad Error:' + e)
        raise e
        
def findFirstList(html):
    myItems = re.findall('<a target="_blank" href="http://55po.com/(.*?)" title=".*?">.*?</a>', html, re.S)
    #print(html)
    return myItems
 
def findList(html):
    myItems = re.findall('<a href=".*?"><span>(\d*)</span></a>', html, re.S)
    return myItems
 
def totalDownload(modelUrl, fnum):
    try:
        listHtml = getHtml(modelUrl)
        listContent = findList(listHtml)
        for list in listContent:
            html = getHtml(modelUrl + "/" + str(list))
            #print(html)
            downloadImg(html, str(list), str(fnum))
    except Exception as e:
        print('total Error:' + e)
        raise e
    
if __name__ == '__main__':
    try:
        listHtml = getHtml('http://55po.com/gifchuchu')
        #http://55po.com/dongtaitu
        firstlist = findFirstList(listHtml)
        for list in firstlist:
            modelUrl = 'http://55po.com/' + str(list)
            totalDownload(modelUrl, str(list))
        print("Download has finished.")
        os.system("pause")
    except Exception as e:
        print("Download Exception Catch:" + e)
        os.system("pause")        