import re
import os

dirs = 'result'
if not os.path.exists(dirs):
    os.makedirs(dirs)


# 上限数量
MAX_WORDS = 100
MAX_WRITING = 2
MAX_READING = 4
MAX_LISTENING = 2
MAX_TRANSLATING = 2

# 修正最小值
MIN_WORDS = 50

# 分数权重
IMP_WORDS = 2
IMP_WRITING = 5
IMP_READING = 2
IMP_LISTENING = 5
IMP_TRANSLATING = 4

print("默认设置规定如下：")
print("%-12s%-12s%-10s" % ("任务内容", "单项积分/分", "积分上限/分"))
print("%-15s%-15d%-15d" % ("单词/50个", IMP_WORDS, MAX_WORDS * IMP_WORDS / 50))
print("%-15s%-15d%-15d" % ("阅读/篇", IMP_READING, MAX_READING * IMP_READING))
print("%-15s%-15d%-15d" % ("听力/套", IMP_LISTENING, MAX_LISTENING * IMP_LISTENING))
print("%-15s%-15d%-15d" % ("作文/篇", IMP_WRITING, MAX_WRITING * IMP_WRITING))
print("%-15s%-15d%-15d" % ("翻译/篇", IMP_TRANSLATING, MAX_TRANSLATING * IMP_TRANSLATING))

"""
name = '王硕+*   &-，2018213641'

user = re.sub("[A-Za-z0-9\+\-\&\*\!\%\ \[\]\,，\。]", "", name)

print(len(user), user)


Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cookie: Hm_lvt_11424cf6b4edd0c3886a337cf8df1ef9=1606100795; vsTY_2132_2132_2132_saltkey=n7QqR7Rq; vsTY_2132_2132_2132_lastvisit=1606098827; vsTY_2132_2132_2132_ulastactivity=1054u9U2mlJRzaVMFaR9IXfPefDIbFlrbbdnym9sHh6ve6k0bj6D; vsTY_2132_2132_2132_auth=740bi3hakJ1s6aV80TfKulq8QnmhToBnu25g07OWRJ%2FX5xi96PM%2BOyKxSN5swh%2FpV0ptg8g2Sio9MFFwtMmAPozhaA; vsTY_2132_2132_2132_lip=59.64.129.247%2C1606102427; vsTY_2132_2132_2132_shou_sort_default_95193=dateline; vsTY_2132_2132_2132_sendmail=1; Hm_lpvt_11424cf6b4edd0c3886a337cf8df1ef9=1606106130; vsTY_2132_2132_2132_sid=Ufa2FR; vsTY_2132_2132_2132_lastact=1606106294%09index.php%09
Host: xzc.cn
Proxy-Connection: keep-alive
Referer: http://xzc.cn/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63
X-Requested-With: XMLHttpRequest


import re
_str = '22 MB'
print(_str[-2])

_str = re.findall("\d+(?:\.\d+)?", _str)
a = 1
a = a + float(_str[0])

print(a)

import datetime
import os
import xlrd
import xlwt
import csv

start_time = datetime.datetime.strptime("2020-12-1 2:0:0", '%Y-%m-%d %H:%M:%S')
end_time = datetime.datetime.strptime("2020-12-3 9:0:0", '%Y-%m-%d %H:%M:%S')

start_date = start_time.date()
end_date = end_time.date()

days = (end_date - start_date).days
csvFile = open("test.csv", 'w', newline='')
try:
    writer = csv.writer(csvFile)
    date_header = ['姓名']
    task_header = ['单词', '阅读', '听力', '写作', '翻译', '分数']
    for i in range(0, days+1):
        now_date = start_date + datetime.timedelta(days=i)
        date_header.append(str(now_date))
        for j in range(0, 5):
            date_header.append('')
    date_header.append('总分')
    writer.writerow(date_header)
    writer.writerow([''] + task_header * (days + 1))

finally:
    csvFile.close()









csvFile = open("test.csv", 'w', newline='')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow((i, i + 2, i * 2))
finally:
    csvFile.close()
"""
