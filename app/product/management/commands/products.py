"""
products.py

배민찬 반찬의 상세 페이지 url을 크롤링
크롤링한 데이터는 products.json 파일에 저장
"""
import json

import requests
from bs4 import BeautifulSoup

parent_categories_info = json.load(open('parent_categories_info.json', 'rt'))
result = list()

for parent_category, info in parent_categories_info.items():
    for category, link in info.items():
        webpage = requests.get(link).text
        soup = BeautifulSoup(webpage, 'lxml')
        products = soup.select('ul#products > li')
        for product in products:
            params = product.select_one('div.imgthumb > a').get('href')
            result.append(f'https://www.baeminchan.com/{parent_category}/{params}')

json.dump(result, open('products.json', 'wt'))
