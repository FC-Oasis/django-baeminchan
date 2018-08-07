"""
crawl.py

실질적으로 배민찬 반찬 크롤링 후 모델에 맞는 인스턴스 생성함(DB 최신화)
./manage.py crawl 명령어로 실행함
"""
import json
import os

from django.core.management import BaseCommand

from product.models.product_info import Product, ProductImage
from product.models.category import ParentCategory, Category
from .parser import *

base_dir = os.path.dirname(__file__)

# 배민찬의 각 상품들의 상세 페이지 url이 담긴 json
urls = json.load(open(os.path.join(base_dir, 'products.json'), 'rt'))

# 배민찬의 카테고리 정보가 담긴 json
parent_categories_info = json.load(open(os.path.join(base_dir, 'parent_categories_info.json'), 'rt'))


class Command(BaseCommand):
    def handle(self, *args, **options):

        # ParentCategory, Category 테이블 업데이트
        self.make_categories(parent_categories_info)

        for url in urls:
            print(url)

            soup = get_soup(url)

            parent_category_name = re.findall('.com/(.+)/', url)[0]

            result = parse_category(soup)
            parent_category = ParentCategory.objects.get(
                name=parent_category_name,
            )
            category = Category.objects.get(
                parent_category=parent_category,
                name=result['category'],
            )

            result = parse_product(soup)
            product, __ = Product.objects.get_or_create(
                category=category,
                **result,
            )

            result = parse_product_image(soup)

            for image_url in result:
                ProductImage.objects.get_or_create(
                    product=product,
                    image_url=image_url,
                )

            print(f'making : {product}')

    @staticmethod
    def make_categories(categories_info):
        for parent_category_name, info in categories_info.items():
            parent_category, __ = ParentCategory.objects.get_or_create(
                name=parent_category_name,
                image_url=info['image_url'],
            )

            for category_name, __ in info.items():
                if category_name == 'image_url':
                    continue
                Category.objects.get_or_create(
                    parent_category=parent_category,
                    name=category_name,
                )
