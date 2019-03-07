#coding:utf-8
import MySQLdb
class tx_cun:
    def __init__(self):
        self.mysql_connect = MySQLdb.connect(user='root', db='txvedio', passwd='s19961224l', host='localhost',
                             charset='utf8')

    def update(self, list_base):
        for item in range(0,len(list_base)):
            sql = u'insert txvediotable(  txvediotitle, txvediourl , txvedioimg, txvediotime, txvedioflag)values( "%s", "%s", "%s", "%s", "%s")'%( list_base[item][u"视频标题"], list_base[item][u"视频链接"], list_base[item][u"图片地址"], list_base[item][u"视频时长"], list_base[item][u"视频是否上传"])
            cur = self.mysql_connect.cursor()
            cur.execute(sql)
            self.mysql_connect.commit()
            cur.close()

    def find_same(self):
        cur = self.mysql_connect.cursor()
        sql = "select txvediotitle from txvediotable "
        cur.execute(sql)
        self.mysql_connect.commit()
        viewtuple = cur.fetchall()
        cur.close()
        return  viewtuple

    def find_all_data(self, viewcount):
        cur = self.mysql_connect.cursor()
        sql = "select * from txvediotable where txvedioflag=0 limit %d"%viewcount
        cur.execute(sql)
        viewtuples =cur.fetchall()
        cur.close()
        return viewtuples
    def changeview(self, viewdatas):
        viewnameindex = 1
        for data in viewdatas:
            sql = "UPDATE txvediotable SET txvedioflag = 1 WHERE txvediotitle = '%s'" % (data[viewnameindex])
            try:
                cursor = self.mysql_connect.cursor()
                cursor.execute(sql)
                # 提交到数据库执行
                self.mysql_connect.commit()
            except:
                # 发生错误时回滚
                self.mysql_connect.rollback()
        print "数据库已经修改"

