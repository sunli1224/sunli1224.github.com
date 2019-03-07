#coding:utf-8
from selenium import webdriver
def find_btn(driver, tagname, strtag, intertime=1, count = 80):
    num = 0
    while num < count:
        try:
            result = driver.find_element_by_xpath(strtag)
            print "该控件已经找到！" + tagname
            return result
        except:
            num +=1
            print "未找到" + tagname + str(num)
    print "规定次数内未找到该控件" + tagname