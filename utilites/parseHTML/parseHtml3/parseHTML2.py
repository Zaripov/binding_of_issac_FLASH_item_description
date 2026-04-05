# -*- coding: utf-8 -*-
import re
import os
import io
from lxml import html
from lxml import etree
import csv
from urllib import parse

def Log(url, text):
    f = open('log.txt', 'a')
    f.write('{0}\t{1}\r\n'.format(url,text))
    f.close()

def tableParse(tblNode, rowLimit):
    print('--itemCnt',len(tblNode.xpath('//tr')))
    items = []
    for i, tr in enumerate(tblNode.xpath('//tr')[1:]):#skip header
        if(i==rowLimit):
            break
        print(i, end=' ')
        nameRU = tr.xpath('.//td[1]//a')[0].text_content().strip()  #ингода "p" тэг а не толко "td"
        print(nameRU)
        nameEN = tr.xpath('.//td[2]')[0].text_content().strip()
        imgSrc = tr.xpath('.//td[1]//img/@src')[0].strip()
        descr = tr.xpath ('.//td[3]')[0].text_content().strip()
        
        unquoted_url = parse.unquote(imgSrc)
        path = parse.urlparse(unquoted_url).path
        imgName = path.rstrip("/").split("/")[-1]
        items.append([nameRU,nameEN,imgSrc,descr,imgName])
    
    return items

if (__name__ == '__main__'):
    filePath = './ALL/Артефакты (Flash) _ The Binding of Isaac вики _ Fandom.HTML' 
    #f = open(filePath,'rt')
    f = open(filePath,'rt', encoding="utf-8")
    #f = io.open(filePath, mode="r", encoding="UTF-8")
    #f = io.open(filePath, mode="r", encoding="CP1251")
    #f = io.open(filePath, mode="r", encoding="CP866")
    #f = io.open(filePath, mode="r", encoding="gb2312")
    #f = io.open(filePath, mode="r", encoding="EUC-JP")
    text = f.read() 
    f.close()
    tree = html.fromstring(text) #tree = etree.parse('xmlfile')

    #//h2/following-sibling::table
    tableNodes = tree.xpath('//table[@class]')
    items = tableParse(tableNodes[0], 34 )
    with open('1.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(items)  # writing all data rows at once

    items = tableParse(tableNodes[2] , -1)
    with open('2.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(items)  # writing all data rows at once
    '''
    #foreach all tags
    for tag in tree.iter():
        if not len(tag):
            print (tag.tag, tag.text)
    '''

    #text not utf-8
    #text = urllib.unquote(text)#html has russian letters in %HEX, it's invisible i dont knot why
    #text = text.decode('utf-8') #= u'' . make text unicode
    #print(text)
    #PageTree = html.fromstring(text) #html.tostring(pageTree) cant extract &# after pagetree made
    #etree.XML(text) etree.XPath etree.tostring(etreeTree) etree.unicode(etreeTree)
    #s = etree.tostring(PageTree) #notWork
    #s = etree.tounicode(PageTree)
    #print(s)


    
