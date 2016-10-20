说明
--------------
使用了ring04h的3个工具，之后会持续进行更新
可直接参考ring04h的github主页 https://github.com/ring04h

必要的工具
--------------
Simple as:

    $ yum install -y gcc-c++ libstdc++-devel
    $ yum install -y uuid
    $ yum install -y mysql-devel
    $ yum install -y lua-devel


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
    $ yum install python-devel libxml2-devel libxslt-devel
    $ pip install lxml beautifulsoup4

    $ sudo rpm -vhU https://nmap.org/dist/nmap-6.47-1.x86_64.rpm

    $ wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2
    $ tar vxf phantomjs-1.9.8-linux-x86_64.tar.bz2
    $ yum install openssl-devel freetype-devel fontconfig-devel
    $ cd phantomjs-1.9.8-linux-x86_64
    $ cp ./bin/phantomjs /usr/bin/

    $ wget --no-check-certificate http://www.thc.org/releases/thc-ipv6-2.7.tar.gz
    $ tar zvxf thc-ipv6-2.7.tar.gz
    $ cd thc-ipv6-2.7
    $ yum install libpcap-devel openssl-devel
    $ make
    $ cp dnsdict6 /usr/bin/

联系我
--------------
Email:zltdhr@gmail.com
