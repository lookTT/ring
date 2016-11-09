说明
--------------
使用了ring04h的3个工具，之后会持续进行更新
可直接参考ring04h的github主页 https://github.com/ring04h

我的测试环境为CentOS6.x

必要的工具
--------------
安装方式:

    $ yum install -y gcc-c++ libstdc++-devel uuid mysql-devel lua-devel
    $ yum install -y python-devel libxml2-devel libxslt-devel
    $ yum install -y openssl-devel freetype-devel fontconfig-devel libpcap-devel

    $ wget http://luajit.org/download/LuaJIT-2.0.4.tar.gz
    $ tar zxvf LuaJIT-2.0.4.tar.gz
    $ cd LuaJIT-2.0.4
    $ make
    $ sudo make install


    $ wget http://luarocks.org/releases/luarocks-2.4.0.tar.gz
    $ tar zxvf luarocks-2.4.0.tar.gz
    $ cd luarocks-2.4.0
    $ ./configure
    $ sudo make bootstrap


    $ luarocks install lua-cjson
    $ luarocks install lua-iconv
    $ luarocks install luasocket
    $ luarocks install luasql-mysql MYSQL_LIBDIR=/usr/lib64/mysql MYSQL_INCDIR=/usr/include/mysql
    $ luarocks install uuid


    # 建议安装python2.7
    
    $ pip install MySQL-python
    $ pip install lxml beautifulsoup4
    $ pip install dnspython
    $ pip install requests
    $ pip install threadpool
    $ pip install uuid

    $ sudo rpm -vhU https://nmap.org/dist/nmap-7.31-1.x86_64.rpm

    $ wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2
    $ tar vxf phantomjs-1.9.8-linux-x86_64.tar.bz2
    $ cd phantomjs-1.9.8-linux-x86_64
    $ cp ./bin/phantomjs /usr/bin/

    $ wget --no-check-certificate http://www.thc.org/releases/thc-ipv6-2.7.tar.gz
    $ tar zvxf thc-ipv6-2.7.tar.gz
    $ cd thc-ipv6-2.7
    $ make
    $ cp dnsdict6 /usr/bin/

快速开始
--------------
例子:

    $ git clone https://github.com/lookTT/ring.git
    $ cd ring
    $ sh main.sh wooyun.org

    建议后台运行，然后去睡觉，一觉醒来会有新发现！
    $ nohup sh main.sh wooyun.org > wooyun.org.out 2>&1 &

联系我
--------------
Email:zltdhr@gmail.com
