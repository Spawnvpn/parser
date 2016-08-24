from urllib.request import urlopen
from lxml import etree
import time
import json


def parse(link=None):
    if not link:
        link = 'http://hotline.ua/computer/noutbuki-netbuki/872'

    site = urlopen(link)
    time.sleep(1)
    content = site.read()
    data_dict = dict()
    price = dict()
    result = list()
    root = etree.HTML(content)
    data = root.xpath("//a[@data-eventlabel='Product name']")
    price['min and max price'] = str(root.xpath('//div[contains(@class, "text-12-640")]/text()')).rstrip()
    price['average price'] = str(root.xpath('//div[contains(@class, "text-13-480")]/text()')).rstrip()
    for item in data:
        link = item.attrib['href']
        detail = get_detail(link)
        detail.insert(1, price)
        data_dict[detail[0]] = detail[1:]
        result.append(data_dict)
    if root.xpath('//a[@data-id="pager-next"]'):
        page_ref = root.xpath('//a[@data-id="pager-next"]')[0].attrib['href']
        link = 'http://hotline.ua/computer/noutbuki-netbuki/872/' + str(page_ref[0])
        parse(link)
    return result


def get_detail(link):
    description = dict()
    notebook = list()
    link = 'http://hotline.ua' + link + '#prop'
    detail_page = urlopen(link)
    time.sleep(1)
    content = detail_page.read()
    root = etree.HTML(content)
    if root.xpath('//*[@data-statistic-key="stat382"]/text()'):
        name = str(root.xpath('//*[@data-statistic-key="stat382"]/text()')[0])
        notebook.append(name)
    params = root.xpath('//*[@id="full-props-list"]/tr')
    for param in params:

        if param.xpath('.//td/span/text()'):
            val_path = './/td/span/text()'
        else:
            val_path = './/td/span/a/text()'
        key = param.xpath('.//th/span/text()')
        value = param.xpath(val_path)
        if value and key:
            key = str(key[0].rstrip())
            value = str(value[0].rstrip())
            description[key] = value
        else:
            continue
        notebook.append(description)
    return notebook

with open('data.txt', 'w') as outfile:
    json.dump(parse(), outfile)
