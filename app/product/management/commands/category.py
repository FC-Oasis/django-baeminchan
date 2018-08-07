"""
category.py

ParentCategory, Category 테이블에 추가할 정보를 크롤링
크롤링한 정보는 parent_categories_info.json 파일에 저장
"""
import requests
from bs4 import BeautifulSoup
import re
import json

root_url = 'https://www.baeminchan.com'


def get_parent_categories_info():
    parent_categories = [
        'side-dish',  # 밑반찬
        'soup',  # 찌개
        'main-courses',  # 메인반찬
        'kids',  # 아이반찬
        'set-of-side',  # 정기식단
        'fresh',  # 간편식
        'refreshment',  # 간식
    ]

    result = dict()

    for parent_category in parent_categories:
        result[parent_category] = dict()

        webpage = requests.get(f'{root_url}/{parent_category}/list.php').text
        soup = BeautifulSoup(webpage, 'lxml')
        
        # parent_category의 이미지
        image_url = re.findall('background: url\((.+)\)', soup.select_one('div.sub_visual_banner').get('style'))[0]
        result[parent_category]['image_url'] = image_url

        choice_category = soup.select('ul.choice_category_lst > li')

        for choice in choice_category[1:]:
            # parent_category의 하위 category
            category = choice.select_one('span').text
            category_params = choice.select_one('a').get('href')
            
            # 하위 category로 이동하는 URL
            link = f'{root_url}/{parent_category}/{category_params}'

            result[parent_category][category] = link

    return result

json.dump(get_parent_categories_info(), open('parent_categories_info.json', 'wt'))


"""
# 크롤링 결과 sample
result = {
    'fresh': {
        'image_url': 'https://cdn.bmf.kr/_data/files/category/category_30060000/69927336efaafaf0f499985c6ff02804.jpg',
        '간편국찌개': 'https://www.baeminchan.com/fresh/list.php?cno=30061200',
        '간편반찬': 'https://www.baeminchan.com/fresh/list.php?cno=30061100',
        '간편식품': 'https://www.baeminchan.com/fresh/list.php?cno=30061300'},
    'kids': {
        'image_url': 'https://cdn.bmf.kr/_data/files/category/category_30040000/3ca340607106f0343594f9f42bdb72bb.jpg',
        '간식·음료': 'https://www.baeminchan.com/kids/list.php?cno=30041500',
        '아이반찬': 'https://www.baeminchan.com/kids/list.php?cno=30041100',
        '어린이반찬': 'https://www.baeminchan.com/kids/list.php?cno=30041200',
        '이유식 초기/중기': 'https://www.baeminchan.com/kids/list.php?cno=30040900',
        '이유식 후기/완료기': 'https://www.baeminchan.com/kids/list.php?cno=30041000'},
    'main-courses': {
        'image_url': 'https://cdn.bmf.kr/_data/files/category/category_30030000/e33f8e28f5844abb06c3f03775971ca7.jpg',
        '고기반찬': 'https://www.baeminchan.com/main-courses/list.php?cno=30030100',
        '덮밥': 'https://www.baeminchan.com/main-courses/list.php?cno=30030900',
        '면': 'https://www.baeminchan.com/main-courses/list.php?cno=30031500',
        '분식': 'https://www.baeminchan.com/main-courses/list.php?cno=30030600',
        '생선반찬': 'https://www.baeminchan.com/main-courses/list.php?cno=30031200',
        '세트': 'https://www.baeminchan.com/main-courses/list.php?cno=30031400',
        '아시아식': 'https://www.baeminchan.com/main-courses/list.php?cno=30030400',
        '양식': 'https://www.baeminchan.com/main-courses/list.php?cno=30030500',
        '죽': 'https://www.baeminchan.com/main-courses/list.php?cno=30030800',
        '튀김': 'https://www.baeminchan.com/main-courses/list.php?cno=30031700',
        '해산물반찬': 'https://www.baeminchan.com/main-courses/list.php?cno=30030200'},
    'refreshment': {
        'image_url': 'https://cdn.bmf.kr/_data/files/category/category_30070000/2100bf2485cf1ba76ff84eaabeed0576.jpg',
        '과일': 'https://www.baeminchan.com/refreshment/list.php?cno=30071500',
        '기타간식': 'https://www.baeminchan.com/refreshment/list.php?cno=30070900',
        '베이커리': 'https://www.baeminchan.com/refreshment/list.php?cno=30070400',
        '스무디': 'https://www.baeminchan.com/refreshment/list.php?cno=30070600',
        '유제품·커피': 'https://www.baeminchan.com/refreshment/list.php?cno=30070800',
        '주스': 'https://www.baeminchan.com/refreshment/list.php?cno=30070700'},
    'set-of-side': {
        '1~2인': 'https://www.baeminchan.com/set-of-side/list.php?cno=30050100',
        '3~4인': 'https://www.baeminchan.com/set-of-side/list.php?cno=30050200',
        'image_url': 'https://cdn.bmf.kr/_data/files/category/category_30050000/355bc4352d9fb42a2e29c319797bb2d9.jpg',
        '아이반찬': 'https://www.baeminchan.com/set-of-side/list.php?cno=30050700'},
    'side-dish': {
        'image_url': 'https://cdn.bmf.kr/_data/files/category/category_30010000/9a798785d8e2ceb31c664cb2b949f4bc.jpg',
        '김치': 'https://www.baeminchan.com/side-dish/list.php?cno=30010800',
        '나물무침': 'https://www.baeminchan.com/side-dish/list.php?cno=30011300',
        '무침': 'https://www.baeminchan.com/side-dish/list.php?cno=30010200',
        '볶음': 'https://www.baeminchan.com/side-dish/list.php?cno=30011800',
        '세트': 'https://www.baeminchan.com/side-dish/list.php?cno=30011900',
        '장아찌·피클': 'https://www.baeminchan.com/side-dish/list.php?cno=30011600',
        '전': 'https://www.baeminchan.com/side-dish/list.php?cno=30011400',
        '젓갈·장·소스': 'https://www.baeminchan.com/side-dish/list.php?cno=30010500',
        '조림': 'https://www.baeminchan.com/side-dish/list.php?cno=30010400'},
    'soup': {
        'image_url': 'https://cdn.bmf.kr/_data/files/category/category_30020000/04e3ddd26b8d4c2307dace6bcab57615.jpg',
        '국': 'https://www.baeminchan.com/soup/list.php?cno=30020100',
        '세트': 'https://www.baeminchan.com/soup/list.php?cno=30021200',
        '전골': 'https://www.baeminchan.com/soup/list.php?cno=30021100',
        '찌개': 'https://www.baeminchan.com/soup/list.php?cno=30020200',
        '탕': 'https://www.baeminchan.com/soup/list.php?cno=30020300'}
}
"""