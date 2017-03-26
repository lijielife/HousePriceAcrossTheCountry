# HousePriceAcrossTheCountry

> 数据来源

* 安居客
* Q房网
* 搜房网
* 链家网

### 自动配置

执行脚本build.sh

### 实现命令行无密码登录MySQL / 命令行无密码执行SQL脚本

创建client.cnf, 写入

```sql
[client]
port     = 3306
socket   = /var/run/mysqld/mysqld.sock
host     = localhost
user     = root
password = 'your password'
```
保存到MySQL配置文件夹下的conf.d子文件夹中，例如对于Ubuntu，配置文件夹一般为/etc/mysql

### 使用MySQLClient

编译安装Qt5.7+

进入MySQLClient子文件夹，解压mysql.tar.gz至本地目录，得到mysql connector c++ SDK，将mysql/lib下的文件复制到/usr/local/lib即可



