#!/usr/bin/python
# -*- coding: UTF-8 -*-
# CET Analyser for BUPT SCSS 2020 CET Activity

import os
import urllib.request
from io import BytesIO
import gzip
import csv
import datetime
import re

login_url = "http://xzc.cn/"
# 上限数量
MAX_WORDS = 100
MAX_WRITING = 2
MAX_READING = 4
MAX_LISTENING = 2
MAX_TRANSLATING = 2

# 修正最小值
MIN_WORDS = 50

# 分数权重
IMP_WORDS = 3
IMP_WRITING = 5
IMP_READING = 2
IMP_LISTENING = 5
IMP_TRANSLATING = 4


def get_response_html(u, h):
    request = urllib.request.Request(u, headers=h)
    response = urllib.request.urlopen(request)
    _html = response.read()
    buff = BytesIO(_html)
    f = gzip.GzipFile(fileobj=buff)
    _html = f.read().decode('utf-8')
    return _html


def get_folder_list():
    _folder_list = []
    li_folder_list = []
    li_folder_left = html.find('<li class="post"')
    li_folder_right = html.find('</li>', li_folder_left)
    while li_folder_left != -1:
        li_folder_list.append(html[li_folder_left:li_folder_right])
        li_folder_left = html.find('<li class="post"', li_folder_right)
        li_folder_right = html.find('</li>', li_folder_left)

    for sub_li in li_folder_list:
        # print(sub_li)
        name = get_sub_str(sub_li, 'target="_dzz">', '                <i')
        count = get_sub_str(sub_li, 'data-vote-count="">', '</span>')
        url = get_sub_str(sub_li, '<a href="', '"')
        start_time = get_sub_str(sub_li, 'title="创建时间">', '&nbsp;')
        if len(start_time) > 20:
            start_time = get_sub_str(start_time, '<span  title="', '"')
        end_time = get_sub_str(sub_li, '</i> ', '</span>')

        folder = {
            'name': name,
            'count': count,
            'url': url,
            'start_time': start_time,
            'end_time': end_time
        }
        _folder_list.append(folder)
    return _folder_list


def get_sub_str(_str, left, right):
    str_left = _str.find(left)
    str_right = _str.find(right, str_left + len(left))
    sub_str = _str[str_left + len(left):str_right]
    return sub_str


def get_all_files(folder_index, start, end):
    loop = int(int(folder_list[folder_index]['count']) / 20) + 1
    tr_file_list = []
    for i in range(1, loop + 1):
        sub_page = get_response_html("http://xzc.cn/" + folder_list[folder_index]['url'] + "/" + str(i), headers)
        sub_page = get_sub_str(sub_page, '<table', '</table>')

        li_file_left = sub_page.find('<td width="45">')
        li_file_right = sub_page.find('</tr>', li_file_left)
        while li_file_left != -1:
            tr_file_list.append(sub_page[li_file_left:li_file_right])
            li_file_left = sub_page.find('<td width="45">', li_file_right)
            li_file_right = sub_page.find('</tr>', li_file_left)

    for sub_tr in tr_file_list:
        str_upload_time = get_sub_str(sub_tr, '<span class="hidden-xs" title="', '"') + ":0"
        if len(str_upload_time) > 20:
            str_upload_time = get_sub_str(sub_tr, '<span  title="', '"') + ":0"
        upload_time = datetime.datetime.strptime(str_upload_time, '%Y-%m-%d %H:%M:%S')
        if (upload_time - start).days < 0 or (end - upload_time).days < 0:
            continue
        file = {
            'name': get_sub_str(sub_tr, 'target="_blank">', '</a>'),
            'size': get_sub_str(sub_tr, '<td>', '</td>'),
            'time': str_upload_time,
            'src': get_sub_str(sub_tr, 'share.php?a=view&s=', '"')
        }
        file_list.append(file)


def do_statistics():
    now_time = datetime.datetime.strptime('2020-11-23 0:0:0', '%Y-%m-%d %H:%M:%S')
    now_name = ""
    for _file in file_list:
        u_name = re.sub("[A-Za-z0-9\+\-\&\*\!\%\ \[\]\,，\。]", "", _file['name'][:_file['name'].find('_')])
        file_time = datetime.datetime.strptime(_file['time'], '%Y-%m-%d %H:%M:%S')
        f_date = datetime.datetime.strftime(file_time, '%Y-%m-%d')
        if len(u_name) < 2:
            continue
        if u_name == now_name and file_time == now_time:
            continue
        now_time = file_time
        now_name = u_name
        user = {
            'words': 0,
            'reading': 0,
            'listening': 0,
            'writing': 0,
            'translating': 0,
            'score': 0,
            'everyday': {}
        }
        if u_name not in user_list:
            user_list[u_name] = user
        if f_date not in user_list[u_name]['everyday']:
            user_list[u_name]['everyday'][f_date] = {
                'words': 0,
                'reading': 0,
                'listening': 0,
                'writing': 0,
                'translating': 0,
                'score': 0,
            }
        _tasks = _file['name'][_file['name'].find('_') + 1:_file['name'].rfind('_')]
        if len(_tasks) == 0:
            _tasks = _file['name'][_file['name'].find('_') + 1:_file['name'].rfind('.')]
        if not _tasks[len(_tasks) - 1].isdigit():
            _tasks += '1'
        # print(_tasks) # 单词一百多，阅读×4,  作文一篇.翻译2，听力两套

        base = "单词词汇阅读精读文意匹配写作作文范文听力精听翻译汉译英0123456789一壹两二三叁仨四五六七八九十百"
        tasks = ""
        for i in _tasks:
            if i in base:
                if i == '一' or i == '壹':
                    tasks = tasks + '1'
                elif i == '二' or i == '两':
                    tasks = tasks + '2'
                elif i == '三':
                    tasks = tasks + '3'
                elif i == '四':
                    tasks = tasks + '4'
                elif i == '五':
                    tasks = tasks + '5'
                elif i == '六':
                    tasks = tasks + '6'
                elif i == '七':
                    tasks = tasks + '7'
                elif i == '八':
                    tasks = tasks + '8'
                elif i == '九':
                    tasks = tasks + '9'
                elif i == '十':
                    tasks = tasks + '0'
                elif i == '百':
                    tasks = tasks + '00'
                else:
                    tasks = tasks + i

        # print(tasks) # 单词100阅读4作文2翻译2听力2
        task_list = []
        count_list = []
        index_left = 0
        index_right = 0
        is_num = False
        while index_right < len(tasks):
            if tasks[index_right].isdigit() and (not is_num):
                is_num = True
                task_list.append(tasks[index_left:index_right])
                index_left = index_right
            elif (not tasks[index_right].isdigit()) and is_num:
                is_num = False
                count_list.append(tasks[index_left:index_right])
                index_left = index_right
            else:
                index_right = index_right + 1
        count_list.append(tasks[index_left:index_right])
        # print(task_list)  # ['单词', '阅读', '作文', '翻译', '听力']
        # print(count_list)  # ['100', '4', '1', '2', '2']

        index_task = 0
        for task in task_list:
            added = int(count_list[index_task])
            if task == '单词' or task == '词汇':
                added = MIN_WORDS if added < MIN_WORDS else added
                user_list[u_name]['everyday'][f_date]['words'] += added
            elif task == '阅读' or task == '精读' or task == '文意匹配':
                added = int(count_list[index_task]) if int(count_list[index_task]) < MAX_READING else MAX_READING
                user_list[u_name]['everyday'][f_date]['reading'] += added
            elif task == '听力' or task == '精听':
                added = int(count_list[index_task]) if int(count_list[index_task]) < MAX_LISTENING else MAX_LISTENING
                user_list[u_name]['everyday'][f_date]['listening'] += added
            elif task == '写作' or task == '作文' or task == '范文':
                added = int(count_list[index_task]) if int(count_list[index_task]) < MAX_WRITING else MAX_WRITING
                user_list[u_name]['everyday'][f_date]['writing'] += added
            elif task == '翻译' or task == '汉译英':
                added = int(count_list[index_task]) if int(
                    count_list[index_task]) < MAX_TRANSLATING else MAX_TRANSLATING
                user_list[u_name]['everyday'][f_date]['translating'] += added
            index_task = index_task + 1

    for u_name in user_list:
        for f_date in user_list[u_name]['everyday']:
            n_words = user_list[u_name]['everyday'][f_date]['words']
            n_reading = user_list[u_name]['everyday'][f_date]['reading']
            n_listening = user_list[u_name]['everyday'][f_date]['listening']
            n_writing = user_list[u_name]['everyday'][f_date]['writing']
            n_translating = user_list[u_name]['everyday'][f_date]['translating']

            user_list[u_name]['everyday'][f_date][
                'words'] = MAX_WORDS if n_words > MAX_WORDS else n_words
            user_list[u_name]['everyday'][f_date][
                'reading'] = MAX_READING if n_reading > MAX_READING else n_reading
            user_list[u_name]['everyday'][f_date][
                'listening'] = MAX_LISTENING if n_listening > MAX_LISTENING else n_listening
            user_list[u_name]['everyday'][f_date][
                'writing'] = MAX_WRITING if n_writing > MAX_WRITING else n_writing
            user_list[u_name]['everyday'][f_date][
                'translating'] = MAX_TRANSLATING if n_translating > MAX_TRANSLATING else n_translating

            n_words = user_list[u_name]['everyday'][f_date]['words']
            n_reading = user_list[u_name]['everyday'][f_date]['reading']
            n_listening = user_list[u_name]['everyday'][f_date]['listening']
            n_writing = user_list[u_name]['everyday'][f_date]['writing']
            n_translating = user_list[u_name]['everyday'][f_date]['translating']

            user_list[u_name]['everyday'][f_date]['score'] = int(n_words / 50) * IMP_WORDS + \
                                                             n_listening * IMP_LISTENING + \
                                                             n_reading * IMP_READING + \
                                                             n_writing * IMP_WRITING + \
                                                             n_translating * IMP_TRANSLATING

            user_list[u_name]['words'] += n_words
            user_list[u_name]['reading'] += n_reading
            user_list[u_name]['listening'] += n_listening
            user_list[u_name]['writing'] += n_writing
            user_list[u_name]['translating'] += n_translating
            user_list[u_name]['score'] += user_list[u_name]['everyday'][f_date]['score']


def do_check():
    for _file in file_list:
        u_name = re.sub("[A-Za-z0-9\+\-\&\*\!\%\ \[\]\,，\。]", "", _file['name'][:_file['name'].find('_')])
        file_name = _file['name'][:_file['name'].rfind('_')]
        file_size = _file['size']
        int_size = int(float((re.findall("\d+(?:\.\d+)?", file_size))[0]))
        if file_size[-2] == 'M':
            continue
        elif file_size[-2] == 'K' and int_size > 10:
            continue
        else:
            if u_name not in user_list:
                user_list[u_name] = []
            user_list[u_name].append(_file)


print("=======Welcome to CET Analyser for BUPT SCSS=======")
print("            Update Time : 2020-12-02")
print("            Version     : 1.1")
print(
    "======Program Started at " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d  %H:%M:%S') + "======")

while True:
    print("[cmd]\n[1]查看默认设置\n[2]更改默认设置\n[3]登录系统\n[4]退出系统")
    cmd_init = input("请输入命令(1-4的某个整数): ")
    if cmd_init.isdigit():
        if int(cmd_init) == 1:
            print("默认设置规定如下：")
            print("%-12s%-12s%-10s" % ("任务内容", "单项积分/分", "积分上限/分"))
            print("%-15s%-15d%-15d" % ("单词/50个", IMP_WORDS, MAX_WORDS * IMP_WORDS / 50))
            print("%-15s%-15d%-15d" % ("阅读/篇", IMP_READING, MAX_READING * IMP_READING))
            print("%-15s%-15d%-15d" % ("听力/套", IMP_LISTENING, MAX_LISTENING * IMP_LISTENING))
            print("%-15s%-15d%-15d" % ("作文/篇", IMP_WRITING, MAX_WRITING * IMP_WRITING))
            print("%-15s%-15d%-15d" % ("翻译/篇", IMP_TRANSLATING, MAX_TRANSLATING * IMP_TRANSLATING))
            continue
        elif int(cmd_init) == 2:
            IMP_WORDS = int(input("单词/50个的单项积分："))
            IMP_READING = int(input("阅读的单篇积分："))
            IMP_LISTENING = int(input("听力的单套积分："))
            IMP_WRITING = int(input("写作的单篇积分："))
            IMP_TRANSLATING = int(input("翻译的单篇积分："))
            MAX_WORDS = int(input("单词上限积分：")) * 50 / IMP_WORDS
            MAX_READING = int(input("阅读的上限积分：")) / IMP_READING
            MAX_LISTENING = int(input("听力的上限积分：")) / IMP_LISTENING
            MAX_WRITING = int(input("写作的上限积分：")) / IMP_WRITING
            MAX_TRANSLATING = int(input("翻译的上限积分：")) / IMP_TRANSLATING
            print("修改成功！")
            continue
        elif int(cmd_init) == 4:
            input("\n欢迎下次使用，bye-bye！")
            exit(0)
        elif int(cmd_init) == 3:
            break
    print("[命令错误]请重新输入，请输入1-4的某个整数")

cookie = input("请输入您的cookie值(若不知道去哪儿找请查看帮助文档readme):")
while True:
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": cookie,
        "Host": "xzc.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://xzc.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63",
        "X-Requested-With": "XMLHttpRequest",
    }
    html = get_response_html(login_url, headers)
    if '创建时间' in html:
        print('登录成功！正在获取收件夹信息...')
        break
    else:
        cookie = input("登陆失败，cookie值错误，请重新输入(输入exit退出):")
        if cookie == "exit":
            input("\n欢迎下次使用，bye-bye！")
            exit(0)

html = get_sub_str(html, '<ul class="posts-group">', '</ul>')
# print(html)

folder_list = get_folder_list()

print("您的所有的收件夹的信息如下：")
print("索引 %-20s收件数量\t\t%-12s开始时间\t  结束时间" % ("文件夹名称", "地址"))
index = 1
for folder in folder_list:
    print(str(index) + "\t%-20s" % folder['name'] + folder['count'] + "\t" + folder['url'] + "\t" + folder[
        'start_time'] + "\t" + folder['end_time'])
    index = index + 1

cmd_index = input("请输入对应的索引(一个整数)进入某文件夹: ")
while True:
    if cmd_index.isdigit():
        if 0 < int(cmd_index) <= len(folder_list):
            break
    cmd_index = input("请输入1~" + str(len(folder_list)) + "的整数: ")

while True:
    print("\n您已进入文件夹：" + folder_list[int(cmd_index) - 1]['name'] + "...")
    print("[cmd]\n[1]统计某段时间内分数情况\n[2]判断某一天是否有人出现上传失败/没按要求的情况\n[3]退出程序")
    cmd_mode = input("请输入命令(1-3的某个整数): ")
    if cmd_mode.isdigit() and 1 <= int(cmd_mode) <= 3:
        if int(cmd_mode) == 3:
            input("\n欢迎下次使用，bye-bye！")
            exit(0)
        if int(cmd_mode) == 1:
            str_start_time = input("请输入开始时间(格式例如：2020-12-1 6:30:0): ")
            while True:
                try:
                    start_time = datetime.datetime.strptime(str_start_time, '%Y-%m-%d %H:%M:%S')
                    break
                except:
                    str_start_time = input("[格式错误]请重新输入开始时间(格式例如：2020-12-1 6:30:0): ")
                    continue
            str_end_time = input("请输入截止时间(格式例如：2020-12-13 20:0:0): ")
            while True:
                try:
                    end_time = datetime.datetime.strptime(str_end_time, '%Y-%m-%d %H:%M:%S')
                    if (end_time - start_time).days < 0:
                        str_end_time = input("[时间错误]截止时间要大于开始时间，请重新输入截止时间: ")
                        continue
                    break
                except:
                    str_end_time = input("[格式错误]请重新输入截止时间(格式例如：2020-12-13 20:0:0): ")
                    continue
            # print(start_time, end_time)

            print("正在进行统计，请稍后...")
            file_list = []
            user_list = {}
            # 2019-12-1 23:30:0
            get_all_files(int(cmd_index) - 1, start_time, end_time)
            # for item in file_list:
            #     print(item)
            do_statistics()
            print("统计完毕")

            while True:
                cmd_save = input("[cmd]\n[1]将结果输出到控制台\n[2]将结果保存到csv文件\n[3]不保存，退出\n请输入命令(1-3的某个整数): ")
                if cmd_save.isdigit() and int(cmd_save) == 1:
                    print("[]每个人的详细结果如下")
                    index = 1
                    for item in user_list:
                        print(str(index) + "\t", item, user_list[item])
                        index += 1
                elif cmd_save.isdigit() and int(cmd_save) == 2:
                    dirs = 'result'
                    if not os.path.exists(dirs):
                        os.makedirs(dirs)

                    start_date = start_time.date()
                    end_date = end_time.date()

                    days = (end_date - start_date).days
                    csvFile = open("result/" + str(start_date) + "~" + str(end_date) + "_CET_Statistics.csv", 'w',
                                   newline='')
                    try:
                        writer = csv.writer(csvFile)
                        date_header = ['姓名']
                        task_header = ['单词', '阅读', '听力', '写作', '翻译', '分数']
                        for i in range(0, days + 1):
                            now_date = start_date + datetime.timedelta(days=i)
                            date_header.append(str(now_date))
                            for j in range(0, 5):
                                date_header.append('')
                        date_header.append('一共')
                        writer.writerow(date_header)
                        writer.writerow([''] + task_header * (days + 2))

                        for i in range(0, days + 1):
                            now_date = start_date + datetime.timedelta(days=i)

                        for user_name in user_list:
                            row = [user_name]
                            for i in range(0, days + 1):
                                now_date = str(start_date + datetime.timedelta(days=i))
                                if now_date in user_list[user_name]['everyday']:
                                    row += [
                                        user_list[user_name]['everyday'][now_date]['words'],
                                        user_list[user_name]['everyday'][now_date]['reading'],
                                        user_list[user_name]['everyday'][now_date]['listening'],
                                        user_list[user_name]['everyday'][now_date]['writing'],
                                        user_list[user_name]['everyday'][now_date]['translating'],
                                        user_list[user_name]['everyday'][now_date]['score']
                                    ]
                                else:
                                    row += [0, 0, 0, 0, 0, 0]
                            row += [
                                user_list[user_name]['words'],
                                user_list[user_name]['reading'],
                                user_list[user_name]['listening'],
                                user_list[user_name]['writing'],
                                user_list[user_name]['translating'],
                                user_list[user_name]['score'],
                            ]
                            writer.writerow(row)
                    finally:
                        csvFile.close()
                    print("文件已成功保存到result/" + str(start_date) + "~" + str(end_date) + "_CET_Statistics.csv")
                elif cmd_save.isdigit() and int(cmd_save) == 3:
                    print("已忽略本次统计, 正在返回上一级...")
                    break
                else:
                    cmd_save = input("[命令错误]请重新输入，请输入1-3的整数: ")
        elif int(cmd_mode) == 2:
            str_start_time = input("请输入日期(格式例如：2020-12-1): ")
            while True:
                try:
                    start_time = datetime.datetime.strptime(str_start_time + " 0:0:0", '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.datetime.strptime(str_start_time + " 23:59:59", '%Y-%m-%d %H:%M:%S')
                    break
                except:
                    str_start_time = input("[格式错误]请重新输入开始时间(格式例如：2020-12-1): ")
                    continue
            file_list = []
            user_list = {}
            print("正在进行检查，请稍后...")
            get_all_files(int(cmd_index) - 1, start_time, end_time)
            do_check()
            print(str_start_time + "上传失败的学生有" + str(len(user_list)) + "个")
            if len(user_list) > 0:
                print("姓名和相应的文件名分别是：")
            for user_name in user_list:
                print(user_name)
                for file in user_list[user_name]:
                    print(file)
            print("\n正在返回上一级...")
            continue
    else:
        print("[命令错误]请重新输入")



# Hm_lvt_11424cf6b4edd0c3886a337cf8df1ef9=1606100795; vsTY_2132_2132_2132_saltkey=n7QqR7Rq; vsTY_2132_2132_2132_lastvisit=1606098827; vsTY_2132_2132_2132_ulastactivity=1054u9U2mlJRzaVMFaR9IXfPefDIbFlrbbdnym9sHh6ve6k0bj6D; vsTY_2132_2132_2132_auth=740bi3hakJ1s6aV80TfKulq8QnmhToBnu25g07OWRJ%2FX5xi96PM%2BOyKxSN5swh%2FpV0ptg8g2Sio9MFFwtMmAPozhaA; vsTY_2132_2132_2132_lip=59.64.129.247%2C1606102427; vsTY_2132_2132_2132_shou_sort_default_95193=dateline; vsTY_2132_2132_2132_sendmail=1; Hm_lpvt_11424cf6b4edd0c3886a337cf8df1ef9=1606106130; vsTY_2132_2132_2132_sid=Ufa2FR; vsTY_2132_2132_2132_lastact=1606106294%09index.php%09

# vsTY_2132_2132_2132_saltkey=IkoQ9Vwm; vsTY_2132_2132_2132_lastvisit=1606875988; vsTY_2132_2132_2132_ulastactivity=15d8HstyuHpyU5jTpIHEZJwiYWHBmTwO433vEDZ%2B9QshrhfEeFbZ; vsTY_2132_2132_2132_shou_sort_default_114284=dateline; vsTY_2132_2132_2132_sendmail=1; Hm_lvt_11424cf6b4edd0c3886a337cf8df1ef9=1606875789,1606879145,1606881354,1606887093; vsTY_2132_2132_2132_sid=EUu4X4; vsTY_2132_2132_2132_auth=e2f4NSyzbGBTI2VuMM0i3YGsqhJWZNaslSqUZIfEeNw3%2BwRkKSv%2BDs4okMpkz68WIK4%2BEFmB4mpF1cll9%2BuzAKt4QkU; Hm_lpvt_11424cf6b4edd0c3886a337cf8df1ef9=1606887125; vsTY_2132_2132_2132_lastact=1606887131%09index.php%09

# 2019-12-1 23:30:0
