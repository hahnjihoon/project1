# bs4, cx-Oracle, selenium 패키지 설치
# tk-html-widget, tkscrolledframe 설치

import tkinter
from tkinter import *
import os
from tkscrolledframe import ScrolledFrame
import bs4
import urllib.request
import common.oracle_db as oradb
import pandas as pd
from tkinter.filedialog import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm

font_path="c:/Windows/Fonts/NGULIM.TTF"
font=fm.FontProperties(fname=font_path).get_name()
mpl.rc('font', family=font)
mpl.rc('axes',unicode_minus=False)


def crawling():
    global news
    urlurl = entry.get()
    web_page = urllib.request.urlopen(urlurl)
    # 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001'
    result = bs4.BeautifulSoup(web_page, 'html.parser')
    news = result.find('div', class_="list_body newsflash_body").find('ul', class_="type06_headline").find_all('li')
    print('커맨드실행됨')
    for i in range(0, len(news)):
        news_title = news[i].find('dt', class_=None).find('a').text.strip()
        listbox.insert(i, news_title)


def crawl_com():
    urlurl = entry.get()
    web_page = urllib.request.urlopen(urlurl)
    # 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001'
    result = bs4.BeautifulSoup(web_page, 'html.parser')
    news2 = result.find('div', id="wrap").find('table',class_='container').find('ul', class_="type06_headline").find_all('li')
    print('커맨드실행됨')
    for i in range(0, len(news2)):
        news_com = news2[i].find('dd').find('span', class_='writing').text.strip()
        listbox.insert(i, news_com)


def show_pie():
    urlurl = entry.get()
    web_page = urllib.request.urlopen(urlurl)
    # 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001'
    result = bs4.BeautifulSoup(web_page, 'html.parser')
    news = {}
    for i in result.find_all('span', class_='writing'):
        if (news.get(i.string) == None):
            news[i.string] = 1
        else:
            news[i.string] += 1
    figure = plt.figure()
    axes = figure.add_subplot(111)
    axes.pie(news.values(), labels=news.keys())
    plt.show()

    # labels = ['채널a', '뉴스1', '조선일보', '코리아중앙데일리', '서울신문']
    # sizes=[2,2,3,5,2]
    # colors=['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'pink']
    # explode=(0,0.1,0,0,0)
    # plt.title("Pie Chart")
    # plt.pie(sizes, explode=explode,labels=labels,colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    # plt.axis('equal')
    # plt.show()


oradb.oracle_init()
conn = ''
cursor = ''
query = 'insert into breakingnews values (:1, :2)'
link_list = []
def insertnews():
    try:
        conn = oradb.connect()
        cursor = conn.cursor()

        for i in range(0, len(news)) :
            # news = result.find('div', class_="list_body newsflash_body").find('ul', class_="ty
            global link_list
            news_title = news[i].find('dt', class_=None).find('a').text.strip()
            # print(news_title)
            # news_info = '제목 : {}'.format(news_title)
            # print(news_info)
            link_list = ((i + 1), news_title)
            cursor.execute(query, link_list)

        oradb.commit(conn)
        print('저장완료')
        listbox.insert(END,'저장완료')

    except Exception as msg:
        oradb.rollback(conn)
        print('오라클 데이터 베이스 과제용 계정 breakingnews 테이블 기록관련 에러', msg)

    finally:
        cursor.close()
        oradb.close(conn)


def savefile():
    f = asksaveasfile(mode="w", defaultextension=".txt")
    if f is None:
        return
    listbox.delete(-1, -1)
    for i in range(0,len(news)):
        ts = str(listbox.get(i, i))+'\n'
        f.write(ts)
    f.close()


def openfile():
    f= askopenfile(mode='r', defaultextension=".txt")
    if f is None:
        return

    listbox.delete(END)
    index=10
    while index>=1:

        data = f.readline()

        listbox.insert(END, data)
        print(data)
        index -= 1
        if index==0 :
            break
    f.close()

    # listbox.insert(END, data)


def clear():
    listbox.delete(0,END)
    listbox.insert(0,'대기중...')


def ent_cmd(event):
    global entry
    entry.delete(0,END)



frame = tkinter.Tk()
frame.title('Crawler')
frame.geometry('1000x800')
frame.resizable(True, True)

menubar = Menu(frame)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="open", command=openfile)
file_menu.add_command(label='save', command=savefile)
file_menu.add_command(label="Exit", command=frame.quit)
menubar.add_cascade(label="File", menu=file_menu)
frame.config(menu=menubar)

#  버튼의 text 와 fg(색상)을 설정할 수 있다.  packer 호출시 side로 위치를 잡아주고,
#  expand는 윈도우가 확장될 때 상대적 위치로 잡아준다.
topFrame = Frame(frame)
topFrame.pack(side=TOP)
bottomFrame = Frame(frame)
bottomFrame.pack(side=BOTTOM)

btn0 = Button(bottomFrame, text='Start Crawling', width= 40, font='고딕,15', bd= 4, command=lambda : crawling())
btn1 = Button(bottomFrame, text='Add Database', width=40, font='고딕,15', bd= 4,command=lambda : insertnews())
btn2 = Button(bottomFrame, text='clear', width=40, font='고딕,15', bd= 4,command=clear)
btn3 = Button(bottomFrame, text='Crawling Company', width=40, font='고딕,15', bd= 4,command=lambda : crawl_com())
btn4 = Button(bottomFrame, text='show pie', width=40, font='고딕,15', bd= 4,command=lambda : show_pie())

btn0.grid(row=0, column=0, padx=3, pady=3, sticky=N + E + W + S)
btn1.grid(row=1, column=0, padx=3, pady=3, sticky=N + E + W + S)
btn2.grid(row=2, column=0, padx=3, pady=3, sticky=N + E + W + S)
btn3.grid(row=0, column=1, padx=3, pady=3, sticky=N + E + W + S)
btn4.grid(row=1, column=1, padx=3, pady=3, sticky=N + E + W + S)

sf = ScrolledFrame(frame, width=1000, height=800)
# 메인프레임의 width, height 와 맞춤
sf.pack(side="top", expand=1, fill="both")

# 마우스 휠버튼과 키보드의 화살표키와 스크롤기능 연결함
sf.bind_arrow_keys(frame)
sf.bind_scroll_wheel(frame)

# 스크롤프레임 안에 프레임 만들기
inner_frame = sf.display_widget(Frame)

listbox = tkinter.Listbox(inner_frame, width='280', height='60')
listbox.insert(END, '대기중..')
listbox.pack()

Label(topFrame, text='URL :', font='13,', bd=10).grid(row=0, column= 0)
entry = Entry(topFrame, width='140', fg='gray')
entry.grid(row=0, column= 1)
entry.insert(END,'주소입력')
entry.bind('<Button-1>', ent_cmd)
# entry.focus_set()
# entry.pack()


frame.mainloop()
# pyinstaller --onefile -noconsole -n crawling_test.exe main.py
# https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001
