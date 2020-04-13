#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import requests,base64,re,time
from lxml import etree
from urllib.parse import quote

cookie = 'cd988c484bc8f1a6e5c99a613440d861'

def spider():
    header = {
        "user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/80.0.835.163 Safari/535.1",
        "Cookie": "_fofapro_ars_session=" + cookie
    }
    search = input()
    searchbs64 = str(base64.b64encode(search.encode('utf-8')),'utf-8')
    searchbs64_encode = quote(searchbs64,'utf-8')    #fofa的url  是需要把base64部分进行url编码
    print("需要爬行的链接为:\nhttps://fofa.so/result?q=" + search + "&qbase64=" + searchbs64_encode)

    html = requests.get(url="https://fofa.so/result?q=" + search + "&qbase64=" + searchbs64_encode,headers=header).text
    pagesnum = re.findall('>(\d*)</a> <a class="next_page" rel="next"',html)
    print("发现的总页数: "+pagesnum[0])
    get_pages = input("请输入需要获取的页数（一页有10个链接）: \n")

    try:
        with open("result1.txt","w+") as result:
            for i in range(1,int(pagesnum[0])):
                print("\n现在写入第 " + str(i) + " 页。\n")
                pagesurl = requests.get("https://fofa.so/result?page=" + str(i) + "&q=" + search + "&qbase64=" + searchbs64_encode,headers=header)
                print("https://fofa.so/result?page=" + str(i) + "&q=" + search + "&qbase64=" + searchbs64_encode + "\n")
                tree = etree.HTML(pagesurl.text)
                urllist = tree.xpath('//div[@class="list_mod_t"]//a[@target="_blank"]/@href')
                for j in urllist:
                    result.write(j + "\n")
                    print(j)
                if i == int(get_pages):
                    break
                time.sleep(10)
            print("已完成！请查看输出的txt！！")
    except IndexError:
        print('\n获得 0 条匹配结果,可能是语法或关键字或者搜索结果少于一页，请检查语法或者搜索的关键字。')

def start():
    print('''
    ***使用说明***
    0.此py为直接爬取fofa搜索结果后的url链接并生成txt.\n
    1.运行此py前，请先在此py里填写自己fofa Pro帐号的cookie.\n
    2.普通帐号只能获取不多于5页的url.\n
    3.如果出现不能获取多页url的情况，请查看cookie是否过期.\n
    4.防止被封IP，所以没做多线程，sleep为10秒.\n
    5.请直接输入fofa的搜索规则,例如输入:title="白帽子".\n
    6.可以进行多语句查询，例如输入：title="白帽子" && country="CN".\n
    7.不支持只有一页搜索结果，都只有一页了，还爬什么虫？\n   
    请输入搜索规则：\n 
    '''
        )

def main():
    start()
    spider()

if __name__ == '__main__':
    main()
