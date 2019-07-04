# YouTube

## CentOS 7
#### 添加yc普通用户
`useradd yc`  
`vi /etc/sudoers`  
更改密码  
`password yc`
添加如下内容  
>yc      ALL=(ALL)       ALL  


#### 关闭笔记本盖不休眠
`sudo vi /etc/systemd/logind.conf`  
将 HandleLidSwitch 的注释去掉并将值改为 lock


#### 腾讯云镜像
`sudo mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup`

`sudo curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.cloud.tencent.com/repo/centos7_base.repo`

`sudo yum clean all`  

`sudo yum makecache`

`vi ~/.pip/pip.conf`
>[global]  
index-url = https://mirrors.cloud.tencent.com/pypi/simple  
trusted-host = mirrors.cloud.tencent.com  

`sudo vi /etc/yum.repo.d/MariaDB.repo`
>[mariadb]  
name = MariaDB  
baseurl = http://mirrors.cloud.tencent.com/mariadb/yum/10.4/centos7-amd64  
gpgkey=https://mirrors.cloud.tencent.com/mariadb/yum/RPM-GPG-KEY-MariaDB  
gpgcheck=1  


#### Anaconda 清华大学镜像
Anaconda 安装包可以到 https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/ 下载  
Miniconda 安装包可以到 https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/ 下载  
`conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/`  
`conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/`  
`conda config --set show_channel_urls yes`  


#### 设置静态IP
xxx是使用 `ip a` 指令得到的网卡  
`sudo vi  /etc/sysconfig/network-scripts/ifcfg-xxx`

修改如下内容  
>BOOTPROTO="static" #dhcp改为static  
>ONBOOT="yes" #开机启用本配置  
>IPADDR=192.168.7.106 #静态IP  
>GATEWAY=192.168.7.1 #默认网关  
>NETMASK=255.255.255.0 #子网掩码  
>DNS1=192.168.7.1 #DNS 配置  

重启下网络服务  
`sudo systemctl restart network.service `

#### 开发者依赖全家桶
`sudo yum groupinstall "Development tools"`


## MariaDB
以root登录到Centos7，执行：  
`sudo curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash`

`sudo yum install MariaDB-server MariaDB-client`

远程登录：  
`sudo firewall-cmd --zone=public --add-service=mysql --permanent`

启停服务：  
`sudo systemctl start mariadb.service`

`sudo systemctl stop mariadb.service`

数据库在系统重启后自启：  
`sudo systemctl enable mariadb.service`

设置root密码：  
`sudo mysql_secure_installation`

登入数据库：  
`mysql -u root -p`

创建数据库：  
`CREATE DATABASE youtube CHARACTER SET utf8;`

`SHOW DATABASES;`

### 添加用户与授权：
`CREATE USER 'yc'@'localhost' IDENTIFIED BY 'wai25789';`

`CREATE USER 'yc'@'%' IDENTIFIED BY 'wai25789';`

`SELECT User, Host, Password FROM mysql.user;`

`GRANT ALL PRIVILEGES ON youtube.* to yc@localhost;`

`GRANT ALL PRIVILEGES ON youtube.* to yc@'%';`

`FLUSH PRIVILEGES;`

`SHOW GRANTS FOR 'yc'@'localhost';`

### 链接MariaDB的驱动：
https://pypi.org/project/mysqlclient/  
Centos7 中使用 `conda install mysqlcient`


## Nginx
`sudo yum install yum-utils`

`sudo vi /etc/yum.repos.d/nginx.repo`  

写入下面内容  
>[nginx-stable]  
>name=nginx stable repo  
>baseurl=http://nginx.org/packages/centos/$releasever/$basearch/  
>gpgcheck=1  
>enabled=1  
>gpgkey=https://nginx.org/keys/nginx_signing.key  
>[nginx-mainline]  
>name=nginx mainline repo  
>baseurl=http://nginx.org/packages/mainline/centos/$releasever/$basearch/  
>gpgcheck=1  
>enabled=0  
>gpgkey=https://nginx.org/keys/nginx_signing.key  

`sudo yum-config-manager --enable nginx-mainline`  

`sudo yum install nginx`

启动nginx  
`sudo nginx`

如果运行的时候不带 -c 参数，那就采用默认的配置文件，即/etc/nginx/conf.d/default.conf  

查看运行进程状态：  
`ps aux | grep nginx`

关闭防火墙  
`sudo setenforce 0`  
`sudo systemctl stop firewalld`  
`sudo systemctl disable firewalld`  
浏览器输入localhost或者远程主机ip检查是否启动成功

停止nginx:  
`sudo nginx -s stop`  
重启nginx:  
`sudo nginx -s reopen`  
重新载入配置文件:  
`sudo nginx -s reload`   
检查配置文件是否正确:  
`sudo nginx -t`   
查看nginx版本  
`nginx -v`


### SSL
`sudo yum-config-manager --enable rhui-REGION-rhel-server-extras rhui-REGION-rhel-server-optional`  
`sudo yum install certbot python2-certbot-nginx`  
如果提示pyOpenSSL版本过低就  
`wget http://cbs.centos.org/kojifiles/packages/pyOpenSSL/16.2.0/3.el7/noarch/python2-pyOpenSSL-16.2.0-3.el7.noarch.rpm`  
`sudo rpm -iUvh python2-pyOpenSSL-16.2.0-3.el7.noarch.rpm`  
生成配置文件  
`sudo certbot certonly --nginx`  
自动续期  
`echo "0 0,12 * * * root python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew" | sudo tee -a /etc/crontab > /dev/null`    


### uwsgi
>uwsgi: error while loading shared libraries: libicui18n.so.58: cannot open shared object file: No such file or directory

的解决方案

查看 uwsgi所在地址，然后使用 LDD 查看缺少的包

`which uwsgi`  
得到 ~/anaconda3/envs/pys/bin/uwsgi  
`ldd ~/anaconda3/envs/py3/bin/uwsgi`  
会看到
>libicui18n.so.58 => not found  
>libicuuc.so.58 => not found  
>libicudata.so.58 => not found  

于是就把 anaconda3/lib 下相应的包复制到/lib64下去（64bit 机器，如果时32bit 机器则软链到/lib下）  
`sudo cp ~/anaconda3/lib/libicui18n.so.58 /lib64/`  

`sudo cp ~/anaconda3/lib/libicuuc.so.58 /lib64/`  

`sudo cp ~/anaconda3/lib/libicudata.so.58 /lib64/`  

再使用ldd 测试结果如下  
>~/anaconda3/envs/py3/bin/uwsgi: /lib64/./libstdc++.so.6: version 'CXXABI_1.3.8' not found (required by /lib64/libicui18n.so.58)  
>~/anaconda3/envs/py3/bin/uwsgi: /lib64/./libstdc++.so.6: version 'CXXABI_1.3.9' not found (required by /lib64/libicui18n.so.58)  
>~/anaconda3/envs/py3/bin/uwsgi: /lib64/./libstdc++.so.6: version 'CXXABI_1.3.8' not found (required by ~/libicuuc.so.58)  
>~/anaconda3/envs/py3/bin/uwsgi: /lib64/./libstdc++.so.6: version 'CXXABI_1.3.9' not found (required by /lib64/libicuuc.so.58)  

`strings /usr/lib64/libstdc++.so.6 | grep CXXABI`  
确实没有CXXABI_1.3.8  CXXABI_1.3.9 之类的东西，那么就把 anaconda3 下的libstdc++.so.6移到/lib64下面  
`sudo cp libstdc++.so.6.0.24 /lib64/`  
版本可能比24高，写笔记时变成了25  

删除/lib64/下原来的libstdc++.so.6符号连接  
`sudo rm -rf libstdc++.so.6`  
新建新符号连接  
`ln -s libstdc++.so.6.0.24 libstdc++.so.6` 

再次执行查看结果符合就了。


### Deplyment
`git clone https://yc-ustc:whoami25789@github.com/USTCCS/youtube.git`  

`cd youtube`

安装项目依赖  
`pip install -r requiredments.txt`

导入表结构  
`python manage.py makemigrations users`

`python manage.py migrate users`

`python manage.py makemigrations videos`

`python manage.py migrate videos`

`python manage.py makemigrations comments`

`python manage.py migrate comments`

`python manage.py makemigrations myadmin`

`python manage.py migrate myadmin`

`python manage.py migrate admin`

`python manage.py migrate`


创建管理员  
`python manage.py createsuperuser`

管理静态文件(只在部署时用)  
`python manage.py collectstatic`

创建upload目录  
`mkdir upload`  
`chmod 777 upload`

`sudo cp youtube_nginx.conf /etc/nginx/conf.d/`

`uwsgi uwsgi.ini` 

`sudo nginx -c /etc/nginx/conf.d/youtube_nginx.conf`


### 注意
可能要改变 settings.py 里面关于 ALLOWED_HOSTS(27行) 和 DB(85行) 地址  
在本地开发要改一下126~130行

如果要更改上传视频的大小限制需要在 settings 的143行和  
myadmin/video_upload.js 的 39, 47, 60 行和  
youtube_nginx.conf 的 25 行更改
