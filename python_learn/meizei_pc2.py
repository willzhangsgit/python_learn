import urllib
import urllib.request
import os
import re
import sys
 
def schedule(a,b,c):
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)
 
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('utf-8')
    return html
 
def downloadImg(html, num, foldername):
    picpath = 'gwimg'
    if not os.path.exists(picpath):
        os.makedirs(picpath)
    target = picpath+'/%s_%s.jpg'% (foldername, num)
    #print(html)
    #myItems = re.findall(b'<p><a href="http:\/\/www.mzitu.com/.*?" ><img src="(.*?)" alt=".*?" /></a></p>',html,re.S)
    myItems = re.findall('<a href=".*?" ><img src="(.*?)" alt=".*?" /></a>',html,re.S)
    print('Downloading image to location: ' + target)
    urllib.request.urlretrieve(myItems[0], target, schedule)

def findFirstList(html):
    myItems = re.findall('<span><a href="http://www.mzitu.com/(\d*)" target="_blank">.*?</a></span>', html, re.S)
    #print(html)
    return myItems

def findPage(html):
    myItems = re.findall('<span><a href="http://www.mzitu.com/(\d*)" target="_blank">.*?</a></span>', html, re.S)
    #print(html)
    return myItems.pop()
 
def findList(html):
    #myItems = re.findall(b'<h2><a href="http://www.mzitu.com/(\d*)" title="(.*?)" target="_blank">.*?</a></h2>', html, re.S)
    #print(html)
    myItems = re.findall('<a href=\'.*?\'><span>(\d*)</span></a>', html, re.S)
    return myItems
 
def totalDownload(modelUrl, fnum):
    listHtml5 = getHtml(modelUrl)
    listContent = findList(listHtml5)
    for list in listContent:
        html = getHtml(modelUrl + "/" + str(list))
        #print(html)
        downloadImg(html, str(list), str(fnum))
#         totalNum = findPage(html)
#         for num in range(1, int(totalNum)+1):
#             if num == 1:
#                 url = 'http://www.mzitu.com/xinggan'
#                 html5 = getHtml(url)
#                 downloadImg(html5, str(num), str(list[0]))
#             else:
#                 url = 'http://www.mzitu.com/xinggan/page/' + str(num)
#                 html5 = getHtml(url)
#                 downloadImg(html5, str(num), str(list[1]))
 
if __name__ == '__main__':
    listHtml = getHtml('http://www.mzitu.com/model')    
    firstlist = findFirstList(listHtml)
    for list in firstlist:
        modelUrl = 'http://www.mzitu.com/' + str(list)
        totalDownload(modelUrl, str(list))
    print("Download has finished.")