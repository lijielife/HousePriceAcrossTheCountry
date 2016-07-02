#!/usr/bin/python
from soufangwang import SouFangWang


def main():
    first_stair_citys = ['Bei Jing', 'Shang Hai', 'Guang Zhou',
                         'Shen Zhen', 'Tian Jin']
    second_stair_citys = ['Hang Zhou', 'Nan Jing', 'Ji Nan',
                          'Chong Qing', 'Qing Dao', 'Da Lian',
                          'Ning Bo', 'Xia Men', 'Wu Han']
    website = '.sofang.com'

    for (j, first_stair_city) in enumerate(first_stair_citys):
        crawler = SouFangWang(city=first_stair_city, website=website)
        crawler.run()

    for (j, second_stair_city) in enumerate(second_stair_citys):
        crawler = SouFangWang(city=second_stair_city, website=website)
        crawler.run()

if __name__ == '__main__':
    main()
