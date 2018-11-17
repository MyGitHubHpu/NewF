# coding: utf-8
import requests
from lxml import etree
import xlwt
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}
# 1.url
url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
# 2.发起请求，接受响应
response = requests.get(url, headers=headers)
# 3.转成树形节点结构
html = etree.HTML(response.text)
# //select[@name="sldd"]/option[last()]/text() last()找到多个标签中的最后一个标签
total_page = html.xpath('//select[@name="sldd"]/option[last()]/text()')[0]
print('共有%s页电影信息，正在准备爬取！'%total_page)
workbook = xlwt.Workbook(encoding='utf-8')
sheet = workbook.add_sheet(u'最新电影信息')
sheet.write(0, 0, '电影名称')
sheet.write(0, 1, '电影类型')
sheet.write(0, 2, '电影时长')
sheet.write(0, 3, '电影下载地址')
count = 0
# 循环遍历所有页
for x in range(1,int(total_page)+1):
    print('正在爬取第%s页数据，请稍后....'%x)
    # 根据x的值，拼接完整页面url地址
    url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_%s.html'%x
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    # 4.使用xpath查找所有的href属性值
    hrefs = html.xpath('//a[@class="ulink"]/@href')
    # for循环取出所有的href值
    for href in hrefs:
        count += 1
        # print('正在爬取第%s个电影信息..'%count)
        # 拼接完整的url地址
        detail_url = 'http://www.ygdy8.net%s'%href
        # 发送请求，拿回详情页面的数据
        detail_response = requests.get(detail_url, headers=headers)
        # print detail_response.content
        # 转换树形节点结构
        detail_html = etree.HTML(detail_response.content)
        # 根据xpath从详情页提取数据
        movie_info = detail_html.xpath('//div[@id="Zoom"]//text()')
        # for中存放的就是电影的所有信息
        for movie in movie_info:
            if u'译　　名' in movie:
                movie_name = movie.split(u'　')[-1]
            elif u'类　　别' in movie:
                movie_type = movie.split(u'　')[-1]
            elif u'片　　长' in movie:
                movie_time = movie.split(u'　')[-1]

        download_url = detail_html.xpath('//tbody/tr/td/a/@href')
        if download_url:
            # if download_url[0][0]!='m':
            if not download_url[0].startswith( 'm'):
                print(download_url)
                sheet.write(count, 0,movie_name)
                sheet.write(count, 1,movie_type)
                sheet.write(count, 2,movie_time)
                sheet.write(count, 3,download_url)

workbook.save(u'电影天堂数据.xls')








