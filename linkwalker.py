from lxml import etree
from lxml import html
import requests
import lxml
import re
import csv
import codecs

root = 'http://www.gibdd.ru';
link_pattern = root + '/r/{0}/accident/?PAGEN_1={1}'
region = 52

def get_links(page_content):
    tree = html.fromstring(page_content)
    return get_links_by_tree(tree)

def get_links_by_tree(tree):
    raw_links = tree.xpath('//div[@id="content"]//p[@class="title"]/a/@href')
    links = []
    for raw_link in raw_links:
        links.append(root + raw_link)
    return links

def get_summary_by_link(link):
    page = requests.get(link)
    tree = html.fromstring(page.content)
    data = tree.xpath('//div[@class="news-detail"]//p/text()')
    summary = ''
    for row in data:
        summary += row + '\n'

    return summary


first_page_link = link_pattern.format(region, 1)

page = requests.get(first_page_link)
tree = html.fromstring(page.content)
last_page = int(tree.xpath('//div[@class="navigation-pages"]/a[last()]/text()')[0])

with open('data/raw_data.csv', 'wb') as csv_file:

    csv_writer = csv.writer(csv_file, delimiter=';')

    # 1st page
    links = get_links_by_tree(tree)
    for link in links:
        summary = get_summary_by_link(link)
        csv_writer.writerow([link, summary.encode('utf-8')])

    for page_num in xrange(2, last_page + 1):
        page_link = link_pattern.format(region, page_num)
        page = requests.get(page_link)
        links = get_links(page.content)

        for link in links:
            summary = get_summary_by_link(link)
            csv_writer.writerow([link, summary.encode('utf-8')])

        print page_num, ' done'
