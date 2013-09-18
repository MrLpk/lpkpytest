#coding=UTF-8
'''
Created on 2013-9-11

@author: liaopengkai
'''

import urllib2
'''代理服务器地址'''
'''http://www.cnproxy.com/proxy1.html'''

def doRequest():
    url = 'http://cctv.cntv.cn/lm/xingguangdadao/xgddwltp/index.shtml'
    charcode = 'utf-8'
    proxy = '110.4.12.170:80'
    req = urllib2.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1")
    req.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    req.add_header("Accept-Charset",charcode)
    req.add_header("Connection","keep-alive")
    req.set_proxy(proxy,"http")
    resultHtml = urllib2.urlopen(req)
    print 'resultHtml=\n',resultHtml.read().decode('gbk')

if __name__ == '__main__':
    print 'start...'
    doRequest()
    print 'over...'