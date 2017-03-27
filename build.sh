#########################################################################
# File Name: build.sh
# Author: summy
# mail: summychou@gmail.com
#########################################################################
#!/bin/bash

echo "[+] Automatically Create Database ... "
mysql -uroot < sql/Anjuke.sql
echo "[+] Create Anjuke Database On MySQL Server ... "
mysql -uroot < sql/SouFangWang.sql
echo "[+] Create SouFangWang Database On MySQL Server ... "
mysql -uroot < sql/QFangWang.sql
echo "[+] Create QFangWang Database On MySQL Server ... "
mysql -uroot < sql/LianJia.sql
echo "[+] Create LianJia Database On MySQL Server ... "
echo "************* MySQL Database List ****************"
mysql -uroot < sql/Show.sql
echo "**************************************************"

echo "[+] Install dependent libraries ... "
sudo apt-get install python-dev python-pip
sudo apt-get install libatlas-base-dev
sudo apt-get install python-numpy python-scipy python-matplotlib python-pandas
sudo apt-get install python-mysqldb
sudo pip2 install shadowsocks
sudo pip2 install flask
sudo pip2 install tqdm
sudo pip2 install bs4 requests
sudo pip2 install xlrd xlwt xlutils
sudo pip2 install scikit-learn
sudo pip2 install theano
sudo pip2 install keras
