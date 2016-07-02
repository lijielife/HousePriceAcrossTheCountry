#!/usr/bin/python
from anjuke import AnJuKe


def main():
    first_stair_citys = ['Bei Jing', 'Shang Hai', 'Guang Zhou',
                         'Shen Zhen', 'Tian Jin']
    second_stair_citys = ['Hang Zhou', 'Nan Jing', 'Ji Nan',
                          'Chong Qing', 'Da Lian', 'Wu Han']
    website = '.anjuke.com'

    for (j, first_stair_city) in enumerate(first_stair_citys):
        crawler = AnJuKe(first_stair_city, website)
        crawler.run()

    for (j, first_stair_city) in enumerate(second_stair_citys):
        crawler = AnJuKe(first_stair_city, website)
        crawler.run()


if __name__ == '__main__':
    main()
