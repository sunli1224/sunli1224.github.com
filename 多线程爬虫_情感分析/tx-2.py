#coding:utf-8
import requests
from lxml import etree
import json
import re
from mysql_cun import mysql_link
import thread
import threading
'''
多线程爬取腾讯视频评论
并对评论进行情感分析
制作图表以图的形式展示数据
'''


class tx(threading.Thread):
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.cun = mysql_link.mysqlConnect()
        self.commentBase = []
        self.url = url
        self.header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36"}

    def getpage(self):
        page = requests.get(url=self.url, headers=self.header).text
        data = re.findall(r'{.*}', page)[0]
        # print data
        datas = json.loads(data)
        # print datas.get(u"data")
        print str(datas.get(u"data").get(u"commentid"))
        for item in datas.get(u"data").get(u"commentid"):
            self.commentBase.append(item.get(u"abstract").replace("<P>","").replace("<\p>",""))
    def comment_cun(self):
        for item in self.commentBase:
            self.cun.search_data(u"insert into tx_comment(comments)values('%s')"%(item))

    def run(self):
        try:
            print "开始爬取..."
            self.getpage()
            self.comment_cun()
            print "结束..."
        except:
            print "error"


if __name__ == "__main__":
    url_base = ["https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6509319156547678669&_=1553082559192",
                "https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6510897559942385706&_=1553082559191",
                "https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6511802939296578984&_=1553082559190",
                "https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6512218566893268489&_=1553082559189",
                "https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6513401721594285435&_=1553082559188",
                "https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6508965439440026422&_=1553082559187",
                "https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6509069697820127292&_=1553082559186",
                "https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6506545843563160798&_=1553082559185",
                "https://video.coral.qq.com/filmreviewr/c/upcomment/wu1e7mrffzvibjy?callback=_filmreviewrcupcommentwu1e7mrffzvibjy&reqnum=3&source=132&commentid=6506760706205152161&_=1553082559184"
                ]

    for item in url_base:
        tx(item).start()
