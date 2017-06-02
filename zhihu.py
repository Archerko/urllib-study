#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename: zhihu.py
import re
import urllib
import urllib2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
               }


def get_answer_list(maxpage):
    answerlist = []
    for page in range(17, maxpage+1):
        url = 'https://www.zhihu.com/collection/78172986?page=%s' % page
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        html = response.read()

        pattern = re.compile(u'<link itemprop="url" href="(/question/\d+/answer/\d+)">')
        answerlist = answerlist + pattern.findall(html)
    return answerlist


def abs_answer_list(maxpage):
    alist = get_answer_list(maxpage)
    _abs_answer_list = map(lambda x: 'https://www.zhihu.com' + x, alist)
    return _abs_answer_list


def get_img_list(maxpage):
    imglist = []
    abslist = abs_answer_list(maxpage)
    for absanswer in abslist:
        request = urllib2.Request(absanswer, headers=headers)
        response = urllib2.urlopen(request)
        html1 = response.read()

        pattern = re.compile(u'data-original="(https://[a-zA-Z0-9./\-:_]*)"')
        imglist = imglist + pattern.findall(html1)
    return imglist


def cbk(block_read, block_size, total_size):
    amout_size = block_read * block_size
    per = 100 * amout_size / float(total_size)
    if per > 100:
        per = 100
    if not block_read:
        print "connection opened"
    elif total_size < 0:
        # unknown size
        print "Downloaded %d blocks (%dbytes)" % (block_read, amout_size)
    else:
        print 'Downloaded %.2f%% ------------ %d blocks,or %d/%d ' % (per, block_read, amout_size, total_size)
        # print 'Read %d blocks,or %d/%d' % (block_read, block_read*block_size, total_size)


def down_img(maxpage):
    _imglist = get_img_list(maxpage)
    for img in _imglist:
        imgname = img.split('/')[-1]
        local = 'C:\\Users\\Arc\\PycharmProjects\\urllib-study\\img\\' + imgname
        urllib.urlretrieve(img, local, cbk)
    print 'All images have been downloaded.'
    print 'The last downloaded answer is %s' % abs_answer_list(maxpage)[-1]
    with open('last_answer.txt', 'a') as f:
        f.write('Last page:%s' % maxpage + ' Last answer:%s' % abs_answer_list(maxpage)[-1]+'\n')

down_img(17)
