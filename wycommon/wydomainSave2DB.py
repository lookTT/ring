#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import MySQLdb
import uuid

# 动态配置项
dbHost      = "192.168.138.131"
dbUser      = "root"
dbPassWd    = "root"
dbDataBase  = "test"
dbCharset   = "utf8"

def wydomain_save2db(domain_uuid, para_domain, wydomains):

    # 生成该域名的uuid方便查找，因可能对某个域名多次扫描，得到的信息也有所不同
    # domain_uuid = uuid.uuid1()
    domain_uuid = str(domain_uuid)
    para_domain = str(para_domain)

    # if domain_uuid=='' or para_domain=='' or type(wydomains)!=:
    #   pass

    # 打开数据库连接
    db = MySQLdb.connect(host=dbHost,user=dbUser,passwd=dbPassWd,db=dbDataBase,charset=dbCharset)
    for k in wydomains['domain']:

        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        query = "INSERT INTO domain (`taskid`, `domain`, `time`) VALUES ('%s','%s', NOW())" % (domain_uuid, k)
        try:
           # 执行sql语句
           cursor.execute(query)
           # 提交到数据库执行
           db.commit()
        except:
           # 返回错误消息
           db.rollback()

        for kk in wydomains['domain'][k]:
            print "kk=" , kk
            if -1 != kk.find(para_domain):
                #合法域名
                #A段IP
                if wydomains['domain'][k][kk].has_key("a"):
                    for x in wydomains['domain'][k][kk]["a"]:
                        query = "INSERT INTO pdomain (`taskid`, `subdomain`,`ip`) VALUES ('%s','%s','%s')" % (domain_uuid, kk, x)
                        print query
                        try:
                           # 执行sql语句
                           cursor.execute(query)
                           # 提交到数据库执行
                           db.commit()
                        except:
                           # 返回错误消息
                           db.rollback()

            else:
                print "不合法的kk=", kk

    for k in wydomains['ipaddress']:
        query = "INSERT INTO ip_addr (`taskid`, `ip_host`,`ip`) VALUES ('%s','%s','%s')" % (domain_uuid, k, "")
        print query
        try:
           # 执行sql语句
           cursor.execute(query)
           # 提交到数据库执行
           db.commit()
        except:
           # 返回错误消息
           db.rollback()

        for kk in wydomains['ipaddress'][k]:
            query = "INSERT INTO ip_addr (`taskid`, `ip_host`,`ip`) VALUES ('%s','%s','%s')" % (domain_uuid, k, kk)
            print query
            try:
               # 执行sql语句
               cursor.execute(query)
               # 提交到数据库执行
               db.commit()
            except:
               # 返回错误消息
               db.rollback()


if __name__ == "__main__":
    if len(sys.argv) == 4:
        # 打开文件
        fo = open(str(sys.argv[3]))
        result = fo.read();
        # 关闭打开的文件
        fo.close()
        wydomain_save2db(sys.argv[1], sys.argv[2], eval(result))
        sys.exit(0)
    else:
        print ("usage: %s domain" % sys.argv[0])
        sys.exit(-1)