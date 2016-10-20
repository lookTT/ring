#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import MySQLdb

# 动态配置项
dbHost      = "192.168.138.131"
dbUser      = "root"
dbPassWd    = "root"
dbDataBase  = "test"
dbCharset   = "utf8"

def wyportmap_transfer(taskid, filepath=None):  
    # 某项任务的绝对唯一ID
    taskid = str(taskid)

    # 打开数据库连接
    db = MySQLdb.connect(host=dbHost,user=dbUser,passwd=dbPassWd,db=dbDataBase,charset=dbCharset)
    sql = "SELECT `ip` FROM pdomain WHERE taskid='%s'" % (taskid)

    dictIP = {}

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
          ip = row[0]
          #去重
          dictIP[ip] = ip

    except Exception as e:
        print "Error: unable to fecth data"

    if filepath is not None:
      filepath = str(filepath)
      fo = open(filepath, "wb")
      for ip in dictIP:
        fo.write( "%s\n" % ip)
      fo.close()

    return dictIP

if __name__ == "__main__":
    if len(sys.argv) == 3:
        # 读取数据库中的数据
        print str(wyportmap_transfer(sys.argv[1], sys.argv[2]))

        sys.exit(0)
    elif len(sys.argv) == 2:
        print str(wyportmap_transfer(sys.argv[1]))
        sys.exit(0)
    else:
        print ("Error: Script %s expect 2 or 1 parameter(s), got %s " % sys.argv[0], len(sys.argv)-1)
        sys.exit(-1)
