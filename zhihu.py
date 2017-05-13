#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename: zhihu.py
import re
import urllib
import urllib2

headers = {

               }


def get_answer_list(maxpage):
    answerlist = []
    for page in range(1, maxpage+1):
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


def cbk(a, b, c):
    per = 100.0 * a * b / c
    if per > 0:
        per = 100
    print '%.2f%%' % per


def down_img(maxpage):
    _imglist = get_img_list(maxpage)
    for img in _imglist:
        imgname = img.split('/')[-1]
        local = 'C:\\Users\\Arc\\PycharmProjects\\urllib-study\\img\\' + imgname
        urllib.urlretrieve(img, local, cbk)
    print 'All images have been downloaded.'

down_img(1)
