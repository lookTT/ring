#!/usr/bin/env python
# encoding: utf-8
# email: ringzero@0x557.org
# http://github.com/ring04h/weakfilescan

"""
	weakfilescan
	userage: python wyspider.py http://wuyun.org
"""

import sys
import libs.requests as requests
from controller import *

if __name__ == "__main__":
	result = ''
	if len(sys.argv) == 3:
		result = json.dumps(start_wyspider(sys.argv[1]), indent=2)
		print result
		# 打开文件
		fo = open(str(sys.argv[2]), "wb")
		fo.write(str(result));
		# 关闭打开的文件
		fo.close()
		
		sys.exit(0)

	elif len(sys.argv) == 2:
		result = json.dumps(start_wyspider(sys.argv[1]), indent=2)
		print result
		sys.exit(0)
	else:
		print ("usage: %s http://wuyun.org php" % sys.argv[0])
		sys.exit(-1)
