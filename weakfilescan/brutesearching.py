#!/usr/bin/env python
# encoding: utf-8

"""
    brutesearching
    userage: python brutesearching.py a.txt
"""

import sys
import uuid
import random
import MySQLdb
import urllib2
import argparse
import threadpool
from DBUtils.PooledDB import PooledDB
from urllib import quote

# 动态配置项
dbHost      = "127.0.0.1"
dbUser      = "root"
dbPassWd    = ""
dbDataBase  = "ring"
dbCharset   = "utf8"

#线程数
poolCount = 16

#mysql连接池
dbpool = PooledDB(MySQLdb,poolCount,host=dbHost,user=dbUser,passwd=dbPassWd,db=dbDataBase,charset=dbCharset,port=3306)

# 随机HTTP头
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# 随机生成User-Agent
def random_useragent(condition=False):
    if condition:
        return random.choice(USER_AGENTS)
    else:
        return USER_AGENTS[0]

# 随机X-Forwarded-For，动态IP
def random_x_forwarded_for(condition=False):
    if condition:
        return '%d.%d.%d.%d' % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254))
    else:
        return '8.8.8.8'

def is_legal(request):
    if request.getcode() == 200 or request.getcode() == 403:
        #判断文件内容
        keyWords = [
            "抱歉", "对不起", "无法打开", "稍后再试", "联系客服", "error", "page-error", "您请求的页面", "404", "Error?", "error?", "icon_404", "404bg", "icon icon_404", ".404bg", ".icon404"
        ]
        ss = request.read()
        count = 0
        for x in keyWords:
            if ss.find(x) != -1:
                count = count + 1

        count = count*1.0
        if count/len(keyWords) >= 0.2:
            # 估计是404地址
            return False
    else:
        return False

    return True
        

def run(args):
    domain = args.domain
    infile = args.infile
    outfile = args.outfile
    taskid = args.taskid

    if 0 != domain.find("http://") and 0 != domain.find("https://"):
        domain = "http://" + domain

    if not taskid:
        taskid = uuid.uuid3(uuid.NAMESPACE_DNS, "brutesearching")
    print taskid

    # 读取传入文件
    urllist = []
    fo = open(str(infile))
    while 1:
        line = fo.readline()
        if not line:
            break
        line = line.replace(' ', '').replace('\r', '').replace('\n', '')
        urllist.append(domain+quote(line))
    fo.close()

    # 检测出符合条件的
    out = []

    # 执行
    def collect(url):
        # HTTP 头设置
        headers = {
            'User-Agent': random_useragent(True),
            'X_FORWARDED_FOR': random_x_forwarded_for(True),
        }
        req = urllib2.Request(url, headers = headers)
        
        try:
            o = urllib2.urlopen(req)
            if is_legal(o):
                # 检查成功
                db = dbpool.connection() #获取链接
                cur = db.cursor() #获取游标
                url = url.replace("'", "\\'")
                query = "INSERT INTO weakfilescan (`taskid`, `subdomain`, `url`, `time`) VALUES ('%s','%s','%s',NOW())" % (taskid, domain, url)
                try: 
                    cur.execute(query) #执行语句
                    db.commit()
                    cur.close() #
                    db.close() #
                except MySQLdb.Error, e:
                    print "Error:%s" % str(e)
                    print query

                out.append(url)
                print "[%s]%s" % (o.getcode(), url)
            else:
                print "[-1]%s" % (url)


        except urllib2.HTTPError as e:
            print "[%s]%s" % (e.code, url)

        except Exception,e:
            print "Request:%s" % url
            print Exception,":",e

        
    #使用多线程执行
    pool = threadpool.ThreadPool(poolCount)
    requests = threadpool.makeRequests(collect, urllist)
    [pool.putRequest(req) for req in requests]  
    pool.wait()
    pool.dismissWorkers(poolCount, do_join=True)

    #写文件
    fo = open(outfile, "wb")
    fo.write(str(out))
    fo.close()

    # 将内容写入数据库
    # 打开数据库连接
    # db = MySQLdb.connect(host=dbHost,user=dbUser,passwd=dbPassWd,db=dbDataBase,charset=dbCharset)
    # # 使用cursor()方法获取操作游标 
    # cursor = db.cursor()
    # for k in out:
    #     query = "INSERT INTO weakfilescan (`taskid`, `subdomain`, `url`) VALUES ('%s','%s','%s')" % (taskid, domain, k)
    #     try:
    #        # 执行sql语句
    #        cursor.execute(query)
    #        # 提交到数据库执行
    #        db.commit()
    #     except:
    #        # 返回错误消息
    #        db.rollback()

    # db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="brutesearching v 0.1 to collect weak files path.")
    parser.add_argument("-d","--domain",metavar="",help="domain name")
    parser.add_argument("-i","--infile",metavar="",default="infile.txt",help="some dict")
    parser.add_argument("-o","--outfile",metavar="",default="brute_result.log",help="result out file")
    parser.add_argument("-t","--taskid",metavar="",help="the uuid")
    args = parser.parse_args()

    try:
        run(args)
    except KeyboardInterrupt:
        logging.info("Ctrl C - Stopping Client")
        sys.exit(1)