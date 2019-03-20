#coding:utf-8
from snownlp import SnowNLP
from mysql_cun import mysql_link
from pylab import mpl
import matplotlib.pyplot as plt

class aysis_txcomment:
    def __init__(self):
        self.cun = mysql_link.mysqlConnect()
        self.base = []
        self.positive_base = []
        self.main_base = {u"好评":0, u"差评":0, u"中等":0}
        self.list_base = []
        self.ptternone = mpl.rcParams["font.sans-serif"] = ['Microsoft YaHei']
        self.patterntwo = mpl.rcParams['axes.unicode_minus'] = False


    def all_comment(self):
        print "开始获取数据。。。"
        sql = u"SELECT comments FROM tx_comment"
        all_data = self.cun.search_data(sql)
        for i in all_data:
            self.base.append(i[0])
        print "获取数据结束。。。"



    def all_comment_ay(self):
        print "开始情感分析。。。"
        for item in self.base:
            s = SnowNLP(item)
            # print s.sentiments
            if(s.sentiments <= 0.5):
                self.main_base[u"差评"] +=1
            if (s.sentiments >= 0.6):
                self.main_base[u"好评"] +=1
            if (s.sentiments >= 0.5 and s.sentiments <= 0.6):
                self.main_base[u"中等"] +=1

        # print self.main_base[u"差评"]
        # print self.main_base[u"好评"]
        # print self.main_base[u"中等"]
        print "情感分析结束。。。"



    def make_pc(self):
        print "开始制作图标。。。"
        self.list_base.append(self.main_base[u"好评"])
        self.list_base.append(self.main_base[u"中等"])
        self.list_base.append(self.main_base[u"差评"])
        plt.bar([u"好",u"中等",u"差"],[self.list_base[0],self.list_base[1],self.list_base[2]])
        plt.xlabel(u"评价")
        plt.ylabel(u"参与人数")
        plt.legend()
        plt.title(u"电视剧都挺好评价表")
        plt.show()
        print "图表制作结束。。。"




    def main(self):
        self.all_comment()
        self.all_comment_ay()
        self.make_pc()




if __name__ == "__main__":
    ll =aysis_txcomment()
    ll.main()