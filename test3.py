# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import csv


class score_spider():
    def __init__(self, target_url, header):
        self.target_url = target_url
        self.header = header
        self.s = requests.Session()

    def login_data(self):  # 输入登录所需信息
        username = input('请输入学号：')
        password = input('请输入登录密码：')
        global payload
        payload = {'username': username, 'password': password}
        return payload

    def login(self):  # 登录
        url_login = self.s.post(self.target_url, headers=header, data=payload)
        print('登录状态为：', url_login.status_code)

    def get_score_text(self, score_url):  # 获取成绩页面源代码
        global score_text
        score_text = self.s.get(score_url).text
        # print(score_text)
        return score_text

    def score_text_cleanning(self, score_text):  # 数据清洗
        score_soup = BeautifulSoup(score_text, 'html.parser')
        my_score_detail = score_soup.find_all('tbody')[1]
        my_score_detail = list(my_score_detail.find_all('td'))
        global my_score_list
        my_score_list = [i.string for i in my_score_detail]
        print(my_score_list)
        return my_score_list

    def output_csv(self, filename):  # 写入csv文件
        f = open(filename, 'w', newline='')
        csv_write = csv.writer(f)
        csv_write.writerow(['序号', '课程代码', '课程名称', '类别', '情况', '教师', '学分', '总评', '绩点'])

        for i in range(0, 140, 10):
            course_list = []
            global my_score_list
            for a in range(i, i + 9):
                course_list.append(my_score_list[a])
            csv_write.writerow(course_list)
        f.close()


if __name__ == "__main__":
    target_url = 'https://jwxt.ncepu.edu.cn/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/64.0'}
    jw_crawler = score_spider(target_url, header)
    jw_crawler.login_data()
    jw_crawler.login()
    score_url = 'https://jwxt.ncepu.edu.cn/webapp/std/edu/grade/course.action'
    score_text = jw_crawler.get_score_text(score_url)
    jw_crawler.score_text_cleanning(score_text)
    jw_crawler.output_csv('my_score_update.csv')
