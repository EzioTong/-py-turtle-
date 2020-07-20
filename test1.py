# -*- conding:utf-8 -*-
#pandas-1.0.5-cp37-cp37m-win_amd64.whl
#https://jwxt.ncepu.edu.cn/jsxsd/framework/xsMain.jsp

import ssl
import requests
import re
import execjs
from bs4 import BeautifulSoup
import pandas as pd
import csv
from datetime import datetime

class School:
    """
        :login_in(user,psw)   # 登录到教务系统，必须先进行这这步
        ：get_xskb_lis()      # 返回登录者本人的课表 返回的是元组数据，s[0] 去掉
        :day_init()           # 每天更新教室情况  使用定时更新
        ：get_msg_by_csv（）  # 返回教室情况  每一节大课 一个\n 字符串型
        :get_cj()             #  返回登录者的成绩 ，得到后使用’\n'分割然后分块输出 字符串型
    """
    def __init__(self):
        self.ses = requests.session()
    def get_js(self, msg):  # python 调用JS加密 返回 加密后的结果
        with open('conwork.js', encoding='utf-8') as f:
            js = execjs.compile(f.read())
            return js.call('encodeInp', msg)
    def get_login_cookies(self):
        header = {
            "Content-Type": "text/html;charset=GBK",
            "Vary": "Accept-Encoding"
        }
        url = "https://jwxt.ncepu.edu.cn/"
        self.ses.get(url=url, headers=header, timeout=1000)
        cookies = self.ses.cookies.get_dict()  # 获得临时的cookies
        cookies = str(cookies).replace("{", '').replace("'", '').replace(":", '=').replace('}', '').replace(",", ";")
        cookies = cookies.replace(" ", '')
        return cookies
    def login(self, cookies, jsmsg):
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Content-Length": "47",
            "Content-Type": "application/x-www-form-urlencoded",  # 接收类型
            "Cookie": cookies,
            "Host": "jwgl.hnuc.edu.cn",
            "Origin": "http://jwgl.hnuc.edu.cn",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://jwgl.hnuc.edu.cn/jsxsd/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
        }
        PostData = {
            'encoded': jsmsg  # 账号密码加密后的东西
        }
        url = 'https://jwxt.ncepu.edu.cn/'
        msg = self.ses.post(url, headers=header, data=PostData, timeout=1000).text  # 这个跳转
        # print("cookies验证:"+str(msg))
    def login_in(self, account, psw):  # 输入账号密码，让cookies 生效
        jsmsg = str(self.get_js(account)) + "%%%" + str(self.get_js(psw)) + "="  # 获得加密后的东西
        self.get_login_cookies()  # cookies 初始化
        self.login(account, jsmsg)  #
    def get_now_week(self):
        now = "2019-09-02 00:03:00"  # 第一周
        now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')  # 第一周
        end = datetime.now()
        week = int((end - now).days / 7) + 1  #
        return week
    def get_all_room(self, where, what):  # 获得教室信息
        week = self.get_now_week()
        beg = week
        end = week
        url = "http://jwgl.hnuc.edu.cn/jsxsd/kbcx/kbxx_classroom_ifr"
        data = {
            "xnxqh": "2019-2020-1",  # 时间不变
            "skyx": "",
            "xqid": where,  # 哪个校区
            "jzwid": what,  # 哪个教学楼
            "classroomID": "",
            "jx0601id": "",
            "jx0601mc": "",
            "zc1": beg,
            "zc2": end,
            "jc1": "",
            "jc2": "",
        }
        msg = self.ses.post(url, data=data).text
        msg = pd.read_html(msg, encoding="UTF-8", header=1)[0]  # 第几个表格
        pd.set_option('display.width', None)
        pd.set_option('display.unicode.east_asian_width', True)  # 宽度对齐
        msg.to_csv(r'' + str(where) + str(what) + '.csv', mode='w+', encoding='utf_8_sig', header=1, index=0)
        print(str(where) + str(what) + "csv文件保存成功！\n")
    def get_msg_by_csv_pre(self, today, classs, where, what):
        filname = str(where) + str(what) + ".csv"
        ans = ""
        with open(file=filname, encoding="UTF-8") as f:
            f_csv = csv.reader(f)
            temp = 1
            for i in f_csv:  # 遍历每一行
                if temp == 1:  # 第一行自动跳过
                    temp += 1
                    continue
                # print(i[6*(today-1)+classs])
                if i[6 * (today - 1) + classs] in (None, ""):  # 是空
                    ans += i[0] + " "
        return ans + "\n"  # 返回所有的，这天这节课没有课的教室
    def exchange(self, where, what):
        temp = []
        if where == 1:
            temp.append("00001")  # 南院
            if int(what) in range(1, 4):  # 左开右闭
                temp.append("0000" + str(what))
                return temp
            else:
                return None
        elif where == 2:
            temp.append("00002")  # 北院
            temp.append("332328065C2440CBAC97F4A714E8937F")
            return temp
        return None
    def get_msg_by_csv(self, where, what):
        temp = self.exchange(where, what)
        if temp in (None, ""):
            return None
        where = temp[0]
        what = temp[1]
        d = datetime.today()  # 获取当前日期时间
        today = d.isoweekday()  # 获得当前的星期
        week = str(self.get_now_week())
        ans = "本学期第" + week + "周星期" + str(today) + ""
        if where == "00001":
            ans += "（南校区，"
            if what == '00001':
                ans += "一教)"
            elif what == '00002':
                ans += "二教)"
            else:
                ans += "三教)"
        else:
            ans += "(北校区，教学楼)"
        ans += "空闲教室如下：\n"
        for i in range(1, 5):
            ans += "第" + str(i * 2 - 1) + "-" + str(i * 2) + "节课:"
            ans += self.get_msg_by_csv_pre(today, i, where, what)
        return ans
    def day_init(self):  # 每天  自动初始化
        try:
            try:
                self.get_all_room("00001", "00001")  # 南院一教
            except:
                pass
            try:
                self.get_all_room("00001", "00002")  # 南院二教
            except:
                pass
            try:
                self.get_all_room("00001", "00003")  # 南院三教
            except:
                pass
            try:
                self.get_all_room("00002", "332328065C2440CBAC97F4A714E8937F")  # 北院教学楼
            except:
                pass
            return True
        except:
            return False
if __name__ == '__main__':
    a = School()
    a.login_in("学号", "密码")
    msg = a.get_msg_by_csv(1, 1)
    print(msg)