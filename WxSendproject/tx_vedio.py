#coding:utf-8
'''
程序名：自动化爬取腾讯视频
程序完成需求：自动化完成腾讯视频的爬取任务
'''
from selenium import webdriver
from lxml import etree
import requests
import cStringIO
from PIL import Image
import random
import time
from mysql_cun.mysql_kk import tx_cun
class TxPc:
    def __init__(self):
        self.url = "https://v.qq.com/x/list/fun"
        self.driver = webdriver.Chrome()
        self.list_base = []
        self.max_vedio_count = 8
        self.max_vediotime = u"00:01:00"
        self.min_vediotime = u"00:00:00"
        self.count = 0
        self.flag = 0
        self.create = tx_cun()
    def txvedio_url(self):

        js = """
        function RandomNum(max, min) {
            var range = max - min;
            var random = Math.random();
            var num =  min + Math.round(range * random);
            return num;
        }

        old = window.scrollY;
        step = RandomNum(10, 30);
        window.scrollBy(0,step);
        news = window.scrollY;
        if(old === news)
            return false;
        else
            return true;

        """
        inter = random.uniform(0.006, 0.03)
        while self.driver.execute_script(js):
            time.sleep(inter)
        page = etree.HTML(self.driver.page_source)
        items = page.xpath("//li[@class='list_item']")
        for item in items:
            if self.check_time_vedio(item) and self.check_samevedio(item):

                self.list_base.append(
                    {
                        u"视频标题": item.xpath("//strong[@class='figure_title figure_title_two_row']//a/text()")[
                            self.count],
                        u"视频链接": item.xpath("//strong[@class='figure_title figure_title_two_row']//a/@href")[
                            self.count],
                        u"图片地址": u"http:" + item.xpath("//li[@class='list_item']//img/@src")[self.count],
                        u"视频时长": item.xpath("//span[@class='figure_info_left']/text()")[self.count],
                        u"视频是否上传": self.flag})
                self.txvedio_img_cun()
                self.count += 1
                if self.count >= self.max_vedio_count:

                    break
        if self.count < self.max_vedio_count:
            self.next_page()
            print "下一页"
            self.txvedio_url()
    def check_time_vedio(self, item):
        time_num = item.xpath("//span[@class='figure_info_left']/text()")[0]
        return self.max_vediotime >= time_num and self.min_vediotime <= time_num
    def check_samevedio(self, item):
        tuples = (item.xpath("//strong[@class='figure_title figure_title_two_row']//a/text()")[0].replace("\"", u"”").replace("\'", u"’").replace(":", u"：").replace("?", u"？"),)
        pagenum = self.create.find_same()
        return tuples not in pagenum
    def next_page(self):
        self.driver.find_elements_by_xpath("//a[@class='page_next']")[0].click()


    def txvedio_img_cun(self):
        for i in self.list_base:
            img_page = requests.session()
            img = img_page.get(i[u"图片地址"]).content
            img_s = cStringIO.StringIO(img)
            img_kk = Image.open(img_s)
            img_kk.resize((800, 600), Image.ANTIALIAS).save(u"E:\WxSendproject\img_cun\{0}.png".format(i[u"视频标题"]))
            img_s.close()
    def Start(self):
        print "开始爬取！"
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.txvedio_url()
        print "爬取结束！"
        self.create.update(self.list_base)
        print "存储完毕！"





if __name__ == "__main__":
    TX_start = TxPc()
    TX_start.Start()