# coding:utf-8
# Time:2021-07-28  08:34
# Version:3.9.1
# Title:信息抓取.py
# Author:歆逸
import requests
from lxml import etree
import xlwt
import os
from get_free_ips import get_free_ip


class get_douban250(object):

    def __init__(self):
        self.movie_url_list = []
        self.rank_list = []
        self.name_list = []
        self.star_list = []
        self.comment_number_list = []
        self.describe_list = []
        self.img_url_list = []

    def get_info(self):
        ip = get_free_ip(1, 2)
        proxies = ip.proxies
        for i in range(10):
            url = f'https://movie.douban.com/top250?start={25 * i}&filter='
            headers = {
                'Cookie': 'bid=GAud7yT-9JQ; __utmz=223695111.1627975053.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=923d360165dd24d4-227e1594a7ca0024:T=1627975053:RT=1627975053:S=ALNI_MZ2phOIx62CrwW-az2ziXJlyXdfbA; ll="118253"; _vwo_uuid_v2=D64CC7CB2462A1A1BB9B0FED741ED518C|1260bb330bd10d13d5141064d399e6fe; __yadk_uid=nuOQ0WW8wduYgZWufIVZmMWuH56DfLLF; douban-fav-remind=1; __utmc=30149280; __utmz=30149280.1633619482.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.4cf6=329a12f37b05a38a.1627975053.6.1634229463.1628834135.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1181103758.1627975053.1633619482.1634229463.7; __utmb=30149280.0.10.1634229463; __utma=223695111.2116547257.1627975053.1628834121.1634229463.6; __utmb=223695111.0.10.1634229463; __utmc=223695111',
                'Referer': 'https://movie.douban.com/chart',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                'Host': 'movie.douban.com'
            }
            res = requests.get(url, headers=headers, proxies=proxies).content.decode()
            html = etree.HTML(res)
            # 影片链接
            movie_urls = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/@href')
            for url in movie_urls:
                self.movie_url_list.append(url)
            # 排名
            rankings = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/em/text()')
            for ranking in rankings:
                self.rank_list.append(ranking)
            # 电影名字
            names = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
            for name in names:
                self.name_list.append(name)
            # 评分数
            stars = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')
            for star in stars:
                self.star_list.append(star)
            # 评论人数
            comment_numbers = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[4]/text()')
            for num in comment_numbers:
                self.comment_number_list.append(num)
            # 热评
            for num in range(25):
                describe = html.xpath(f'//ol[@class="grid_view"]/li{[num + 1]}//span[@class="inq"]/text()')
                if len(describe) != 0:
                    self.describe_list.append(describe[0])
                else:
                    describe = '无热评'
                    self.describe_list.append(describe)
            # 图片地址
            img_urls = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src')
            for url in img_urls:
                self.img_url_list.append(url)
        return self.write_excel()

    def write_excel(self):
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
        col = ('排名', '电影名', '评分', '评价数', '概况', '影片链接', '图片链接')
        for i in range(0, 7):
            sheet.write(0, i, col[i])
        for j in range(250):
            sheet.write(j + 1, 0, self.rank_list[j])
            sheet.write(j + 1, 1, self.name_list[j])
            sheet.write(j + 1, 2, self.star_list[j])
            sheet.write(j + 1, 3, self.comment_number_list[j])
            sheet.write(j + 1, 4, self.describe_list[j])
            sheet.write(j + 1, 5, self.movie_url_list[j])
            sheet.write(j + 1, 6, self.img_url_list[j])
        book.save('豆瓣电影Top250信息.xls')

    def get_img(self):
        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }
        dir_name = 'images'  # 设置文件夹的名字
        if not os.path.exists(dir_name):  # os模块判断并创建
            os.mkdir(dir_name)
        for j in range(250):
            img_url = self.img_url_list[j]
            response = requests.get(img_url, headers=header).content
            with open(dir_name + '/' + self.name_list[j] + '.jpg', 'wb') as f:
                f.write(response)


if __name__ == '__main__':
    a = get_douban250()
    a.get_info()
    answer = input('是否下载图片y/n(仅限小写):')
    if answer == 'y':
        print('下载中')
        a.get_img()
        print('已完成,程序结束')
    else:
        print('已结束')

