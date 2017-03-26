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

# echo "[+] Install dependent libraries ... "
# sudo apt-get install python-dev python-pip
# sudo apt-get install libatlas-base-dev
# sudo apt-get install python-numpy python-scipy python-matplotlib
# sudo apt-get install python-mysqldb
# sudo pip install shadowsocks
# sudo pip install flask
# sudo pip install tqdm
# sudo pip install bs4 requests
# sudo pip install xlrd xlwt xlutils
# sudo pip install scikit-learn
# sudo pip install theano
# sudo pip install keras
