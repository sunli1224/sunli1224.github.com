#coding:utf-8
'''
程序名：自动化完成微信公众号平台视频发布
程序完成需求： 自动化完成公众号视频的发布
'''
from selenium import webdriver
from find_btn import btn_find
from mysql_cun.mysql_kk import tx_cun
import time
from selenium.webdriver.common.keys import Keys
import  cStringIO
import requests
from win_control.control import solvedexplore
import random
from tx_vedio import TxPc
class WxLogin:
    def __init__(self):
        self.txpc = TxPc()
        self.wxweb_url = "https://mp.weixin.qq.com/"
        self.webdriver = webdriver.Chrome()
        self.sucesslogin = True
        self.txcun  = tx_cun()
        self.viewcount = 8
        self.slogan1 = u'点击--pi虾虾--笑料--玩梗  '
        self.slogan2 = u'  关注公众号，免费看更多搞笑视频。'
        self.path = u"E:\\WxSendproject\\img_cun\\"
        self.author = u"皮虾虾"

    def loginwx(self):
        self.webdriver.get(self.wxweb_url)
        self.webdriver.maximize_window()
        name_btn = self.webdriver.find_element_by_xpath("//input[@placeholder='邮箱/微信号/QQ号']")
        pass_btn = self.webdriver.find_element_by_xpath("//input[@placeholder='密码']")
        login_btn = self.webdriver.find_element_by_xpath("//a[@class='btn_login']")
        name_btn.send_keys("youdianxiaoshuai24@126.com")
        pass_btn.send_keys("s19961224l")

        while self.sucesslogin:
            try:
                self.webdriver.find_element_by_xpath("//div[@class='js_wording']")
                self.sucesslogin = False
            except:
                login_btn.click()
                time.sleep(2)
        print "扫码成功进入公众号"
    def sctj(self):
        btn_find.find_btn(self.webdriver, "素材管理", '//span[text()="素材管理"]', 1, 3600).click()

    def xjscwd(self):
        btn_find.find_btn(self.webdriver, "新建图文素材", '//button[text()="新建图文素材"]', 1, 30).click()

    def czbt(self):
        all_hands = self.webdriver.window_handles
        for hand in all_hands:
            self.webdriver.switch_to.window(hand)
            if btn_find.find_btn(self.webdriver, "请在这里输入标题", '//input[@placeholder="请在这里输入标题"]', 1, 1): break

    def bjwd(self):
        viewdata = self.txcun.find_all_data(self.viewcount)
        return (True, viewdata) if len(viewdata) == self.viewcount else (False,)

    def bjwz(self, viewdata):
        for count , data in enumerate(viewdata):
            viewtitle = data[1]
            viewvediourl = viewdata[count][2]
            # viewimg = data[3]
            # # viewflag = data[4]

            btn_find.find_btn(self.webdriver, "请在这里输入标题", '//input[@id="title"]').send_keys(viewtitle)

            btn_find.find_btn(self.webdriver, "作者", '//input[@id="author"]').send_keys(self.author)

            self.__windowtoframe(self.slogan1)

            self.webdriver.switch_to.default_content()

            btn_find.find_btn(self.webdriver, "视频", '//li[@id="js_editor_insertvideo"]').click()

            btn_find.find_btn(self.webdriver, "视频链接", '//a[text()="        视频链接      "]').click()

            btn_find.find_btn(self.webdriver, "输入视频链接", '//input[@name="videoLink"]').clear()

            time.sleep(3)

            btn_find.find_btn(self.webdriver, "输入视频链接", '//input[@name="videoLink"]').click()

            btn_find.find_btn(self.webdriver, "输入视频链接", '//input[@name="videoLink"]').send_keys(viewvediourl)

            time.sleep(2)

            btn_find.find_btn(self.webdriver, "点击确定视频",'//button[@class="weui-desktop-btn weui-desktop-btn_primary"][text()="确定"]').click()
            time.sleep(1)

            self.webdriver.switch_to.default_content()


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
            inter = random.uniform(0.003, 0.1)
            while self.webdriver.execute_script(js):
                time.sleep(inter)
            # time.sleep(2)
            btn_find.find_btn(self.webdriver, "选择封面", '//span[text()="选择封面"]')



            # btn_img = btn_find.find_btn(self.webdriver, "从图片库选择", '//a[@id="js_imagedialog"]',0, 1)

            btn_img = self.webdriver.find_element_by_xpath("//a[@id='js_imagedialog']")

            self.webdriver.execute_script("$(arguments[0]).click()",btn_img)

            # btn_img.click()
            # btn_find.find_btn(self.webdriver, "今日图片", '//strong[text()="今日图片"]').click()


            # while btn_find.find_btn(self.webdriver, "判断今日图片选中",  '//strong[text()="今日图片"]/../..', 1, 1).get_attribute("class") != "inner_menu_item js_groupitem selected":pass
            btn_find.find_btn(self.webdriver, "本地上传",  '//span[@class="upload_area webuploader-container"]').click()

            solvedexplore(self.path + viewtitle + u".png")

            time.sleep(3)

            btn_find.find_btn(self.webdriver, "图片下一步", '//button[text()="下一步"]').click()

            time.sleep(2)

            btn_find.find_btn(self.webdriver, "图片完成", '//button[text()="完成"]').click()

            time.sleep(3)

            self.webdriver.switch_to.default_content()

            self.__judgecontents(count, viewdata)

    def __judgecontents(self, count, viewdata):
        #有时候完成按钮消失后，回到主页面可能会延迟
        while btn_find.find_btn(self.webdriver, "完成按钮消失", '//button[text()="完成"]/', 1, 3): pass  # 完成按钮消失，点击才可以保存
        if count < self.viewcount - 1:
            self.safeclick(btn_find.find_btn(self.webdriver, "保存", '//button[text()="保存"]'))
            self.__newcontent()
        else:
            self.safeclick(btn_find.find_btn(self.webdriver, "保存并群发", '//button[text()="保存并群发"]', 1, 1))
            #ajax页面等页面出现在下拉滚动条
            btn_find.find_btn(self.webdriver, "群发", '//label[text()="群发"]')
            # pullscrool(self.webdriver, 0.003, 0.1)
            btn_find.find_btn(self.webdriver, "群发", '//label[text()="群发"]').click()
            time.sleep(3)
            btn_find.find_btn(self.webdriver, "继续群发", '//a[text()="继续群发"]').click()
            self.iscomplete(viewdata)#改变数据库的内容

    def iscomplete(self, viewdata):
        if btn_find.find_btn(self.webdriver, "是否发布", "//a[text()='新建群发']",1, 6000):
            self.txcun.changeview(viewdata)
            print "完成今日推送！"
    def __newcontent(self):
        time.sleep(3)


        self.imagedocount = "other"
        btn_find.find_btn(self.webdriver, "点击+号", '//i[@id="js_add_appmsg"]')

        time.sleep(2)

        add_btn = btn_find.find_btn(self.webdriver, "点击+号", '//i[@id="js_add_appmsg"]')

        add_btn.click()
        btn_find.find_btn(self.webdriver, "增加一条图文消息", '//i[@class="icon-svg-editor-appmsg"]').click()
        # self.safeclick(btn_find.find_btn(self.webdriver, "增加一条图文消息", '//i[@class="icon-svg-editor-appmsg"]'))
    def safeclick(self, tag):#自动化点击保存和鼠标点击有冲突
        while True:
            try:
                tag.click()
                break
            except:pass
    def __windowtoframe(self, content):
        iframe = btn_find.find_btn(self.webdriver, "编辑文档", '//iframe[@id="ueditor_0"]')
        self.webdriver.switch_to.frame(iframe)
        sceditcontent = btn_find.find_btn(self.webdriver, "iframe的body", '//body[@class="view"]')
        #sceditcontent.send_keys(Keys.LEFT)
        sceditcontent.send_keys(Keys.LEFT)
        sceditcontent.send_keys(Keys.BACK_SPACE)#退格
        sceditcontent.send_keys(Keys.RIGHT)
        sceditcontent.send_keys(content)
    def main(self):
        self.loginwx()
        self.sctj()
        self.xjscwd()
        print "开始编辑文档！"
        self.czbt()
        viewtuples = self.bjwd()
        if viewtuples[0] == True:
            self.bjwz(viewtuples[1])
        else:
            print "数据库的内容不够，请重新爬取！"
            self.txpc.Start()
            self.main()



if __name__ == "__main__":
    wxlogin = WxLogin()
    wxlogin.main()