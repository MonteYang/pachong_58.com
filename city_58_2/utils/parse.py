# -*- coding:utf-8 -*-
from pyquery import PyQuery

def get_xiaoqu_detail_url(response):
    '''
    在小区列表页：http://bj.58.com/xiaoqu/1142/
    获取小区详情页的url
    :param response:
    :return: list, 元素为小区详情页url
    '''
    jpy = PyQuery(response.text) # 构建PyQuery选择器对象
    tr_list = jpy('#infolist > div.listwrap > table > tbody > tr')
    result = set()
    for tr in tr_list.items():
        url = tr('td.info > ul > li.tli1 > a').attr('href')
        result.add(url)
    return result

def parse_xiaoqu_detail(response):
    '''
    在小区详情页：http://bj.58.com/xiaoqu/zhujiangdijing/
    获取小区信息：包括 name, price, detail_address, times(年代)
    :param response:
    :return: result: dict, 小区信息
    '''
    jpy = PyQuery(response.text)
    result = dict()
    result['name'] = jpy('body > div.body-wrapper > div.title-bar > span.title').text()
    result['price'] = jpy('body > div.body-wrapper > div.basic-container >'
                          ' div.info-container > div.price-container > span.price').text()
    result['address'] = jpy('body > div.body-wrapper > div.basic-container > div.info-container > '
                                   'div.info-tb-container > table > tr:nth-child(1) > td:nth-child(4)').text()
    result['times'] = jpy('body > div.body-wrapper > div.basic-container > div.info-container'
                          ' > div.info-tb-container > table > tr:nth-child(5) > td:nth-child(2)').text()
    return result

# 缺少功能：获取小区二手房url
def get_ershou_price_list(response):
    '''
    在小区二手房页面（某页）上：http://bj.58.com/xiaoqu/zhujiangdijing/ershoufang/
    获取价格，用于计算平均价格
    :param response:
    :return: 小区二手房价格列表
    '''
    jpy = PyQuery(response.text)
    tr_list = jpy('#infolist > div.listwrap > table > tr')
    price_list = []
    for tr in tr_list.items():
        price = tr('td.tc > b').text()
        price_list.append(price)
    return price_list

def get_xiaoqu_chuzu_url(response):
    '''
    测试页：http://bj.58.com/xiaoqu/zhujiangdijing/chuzu/

    :param response:
    :return: 一个list，为租房详情页url的列表
    '''
    jpy = PyQuery(response.text)
    tr_lsit = jpy('#infolist > div.listwrap > table > tr')
    result = [i('td.t > a.t').attr('href') for i in tr_lsit.items()]
    return result

def get_chuzu_detail(response):
    '''
    测试页面：http://bj.58.com/zufang/33830134012877x.shtml
    :param response:
    :return: 租房详细信息dict:
                key: name,price,type,area
    '''
    jpy = PyQuery(response.text)
    result = dict()
    result['name'] = jpy('body > div.main-wrap > div.house-title > h1').text()
    result['price'] = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr >'
                          ' div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_ff552e > b').text()
    result['type'] = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc'
                         ' > div.house-desc-item.fl.c_333 > ul > li:nth-child(2) > span:nth-child(2)').text().split()[0]
    area = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc'
                         ' > div.house-desc-item.fl.c_333 > ul > li:nth-child(2) > span:nth-child(2)').text().split()
    result['area'] = area[1] + area[2]
    return result


if __name__ == '__main__':
    import requests
    url = ['http://bj.58.com/xiaoqu/1142/',
           'http://bj.58.com/xiaoqu/zhujiangdijing/',
           'http://bj.58.com/xiaoqu/zhujiangdijing/chuzu/',
           'http://bj.58.com/xiaoqu/zhujiangdijing/chuzu/',
           'http://bj.58.com/zufang/33830134012877x.shtml'
           ][2]
    response = requests.get(url)
    # print(get_xiaoqu_detail_url(response))
    # print(parse_xiaoqu_detail(response))
    print(get_ershou_price_list(response))
    # print(get_xiaoqu_chuzu_url(response))
    # print(get_chuzu_detail(response))