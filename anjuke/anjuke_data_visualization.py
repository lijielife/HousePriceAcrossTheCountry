#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import warnings
warnings.filterwarnings('ignore')

try:
    import pandas as pd
except ImportError, e:
    print '>> pandas Module is not found, please install it first'
try:
    import numpy as np
except ImportError, e:
    print '>> numpy Module is not found, please install it first'
try:
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    FONT = FontProperties(fname=(os.getcwd() + "/wqy-microhei.ttc"), size=10)
except ImportError, e:
    print '>> numpy Module is not found, please install it first'

CITY = [u'北京', u'上海', u'广州', u'深圳', u'杭州', u'武汉']

def read_csv(filename):
    pandas_data = pd.read_csv(filename)
    return pandas_data

def plot(df):
    df_list = []

    beijing = df[df[u'楼盘链接'.encode('utf8')].str.startswith('http://bj.fang.anjuke.com/')]
    df_list.append(beijing)
    print u'北京的有效数据为{}条'.format(beijing.shape[0])
    shanghai = df[df[u'楼盘链接'.encode('utf8')].str.startswith('http://sh.fang.anjuke.com/')]
    df_list.append(shanghai)
    print u'上海的有效数据为{}条'.format(shanghai.shape[0])
    guangzhou = df[df[u'楼盘链接'.encode('utf8')].str.startswith('http://gz.fang.anjuke.com/')]
    df_list.append(guangzhou)
    print u'广州的有效数据为{}条'.format(guangzhou.shape[0])
    shenzhen = df[df[u'楼盘链接'.encode('utf8')].str.startswith('http://sz.fang.anjuke.com/')]
    df_list.append(shenzhen)
    print u'深圳的有效数据为{}条'.format(shenzhen.shape[0])
    hangzhou = df[df[u'楼盘链接'.encode('utf8')].str.startswith('http://hz.fang.anjuke.com/')]
    df_list.append(hangzhou)
    print u'杭州的有效数据为{}条'.format(hangzhou.shape[0])
    wuhan = df[df[u'楼盘链接'.encode('utf8')].str.startswith('http://wh.fang.anjuke.com/')]
    df_list.append(wuhan)
    print u'武汉的有效数据为{}条'.format(wuhan.shape[0])

    X = np.arange(6)
    Y = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for index, dataframe in enumerate(df_list):
        Y[index] = dataframe[u'价格|元/m2'.encode('utf8')].mean()
    
    plt.bar(X, +Y, alpha=1., facecolor='#101010', edgecolor='white')
    for x, y, city in zip(X, Y, CITY):
        plt.text(x + 0.4, y + 100, city + '/%.0f' % y, ha='center', va= 'bottom', fontproperties=FONT, fontsize=12)
    
    plt.xlabel(u'城市', fontproperties=FONT, fontsize=14)
    plt.xticks([])
    plt.ylabel(u'均价/m^2', fontproperties=FONT, fontsize=15)
    plt.ylim([0, 100000])
    plt.yticks(np.arange(0, 100001, 10000))
    plt.title(u'北上广深+杭州+武汉，各地新楼盘均价', fontproperties=FONT, fontsize=17)
    plt.grid(color='#707070', linestyle='--', linewidth=1)
    plt.show()

def run():
    dataframe = read_csv('anjuke_new_house_data/AnJuKe_New_House.csv')
    print u'AnJuKe_New_House_DataFrame的有效数据为{}条'.format(dataframe.shape[0])
    plot(dataframe)

if __name__ == '__main__':
    run()
