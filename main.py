from bs4 import BeautifulSoup
import requests
from opencc import OpenCC
import re
import json
import os

# 创建OpenCC对象，选择转换的模式
cc = OpenCC('t2s')  # 繁体中文转简体中文
# 定义提取函数
def extract_events_from_html(html_content):
    events_day = []
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')

    content_div = soup.find('div', id='mw-content-text')
    # 找到所有 ul 元素
    uls = content_div.find_all('ul', class_='')
    # 在 tds 找到所有带有 class="event" 的 li 元素
    for ul in uls:
        event_lis = ul.find_all('li', class_='')
        # 提取日期和事件信息
        for event_li in event_lis:
            event = event_li.text.strip()
            event = cc.convert(event).split("：")
            pattern = r'\b\d+年\b'
            if event == []: continue
            if event.__len__() == 1: continue
            if event[0] == "":
                event[0] = event[1]
                event[1] = event[2]
            if event[1] == "":
                event[1] = event[2]
            if re.match(pattern, event[0]):
                events_day.append({"year": event[0],"event": re.sub(r'\[\d+\]', '', event[1])})
    
    return events_day


# # 定义目标页面的URL
# # month = input("请输入月份:")
# # day = input("请输入日期:")
# month = 1
# day = 1
# date = "%u月%u日" % (month, day)
# url = "https://zh.wikipedia.org/wiki/" + date

# # 发送GET请求
# response = requests.get(url)

# # 检查请求是否成功
# if response.status_code == 200:
#     # 提取事件信息
#     events = extract_events_from_html(response.text)

#     # 打印提取的事件信息
#     for event in events:
#         print(event)
# else:
#     print("请求失败，状态码:", response.status_code)



# 保存文件
# file = "history_toDay.json"
# fileOpen = open(file, mode='w+', encoding='utf-8')
# fileOpen.write("[")
# fileOpen.close()
# for month in range(1, 13):
#     events_month = []
#     for day in range(1, 32):
#         date = "%u月%u日" % (month, day)
#         url = "https://zh.wikipedia.org/wiki/" + date
#         # 发送GET请求
#         response = requests.get(url)
#         # 检查请求是否成功
#         if response.status_code == 200:
#             # 提取事件信息
#             events = extract_events_from_html(response.text)
#             if events:
#                 events_month.append(events)
#                 print(date)
#         else:
#             print("请求失败，状态码:", response.status_code)
#     fileOpen = open(file, mode='a+', encoding='utf-8')
#     if month != 1:
#         fileOpen.write(",")
#     fileOpen.write(json.dumps(events_month, ensure_ascii=False))
#     fileOpen.close()
# fileOpen = open(file, mode='a+', encoding='utf-8')
# fileOpen.write("]")
# fileOpen.close()

file = "month_history_toDay.json"

for month in range(1, 13):
    events_month = []
    for day in range(1, 32):
        date = "%u月%u日" % (month, day)
        url = "https://zh.wikipedia.org/wiki/" + date

        # 发送GET请求
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 提取事件信息
            events = extract_events_from_html(response.text)
            if events:
                events_month.append(events)
                print(date)

        else:
            print("请求失败，状态码:", response.status_code)

    fileOpen = open(str(month) + file, mode='w+', encoding='utf-8')
    fileOpen.write(json.dumps(events_month, ensure_ascii=False))
    fileOpen.close()