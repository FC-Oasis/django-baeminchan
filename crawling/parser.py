import re

import requests
from bs4 import BeautifulSoup


def get_price():
    """
    가격과 상품 정보의 태그가 조금 달라서 일단 가격 정보만 따로 메서드로 만듦
    가격과 상품 정보를 한꺼번에 묶을 수 있도록 시도할 예정

    가격을 int 형식으로 만들기 위해서 콤마(,)는 제외시킴
    ex) 3,800원 -> 3800

    이 코드는 주피터 노트북에서 실행 가능함
    :return:
    """
    req = requests.get('https://www.baeminchan.com/side-dish/list.php?cno=30010000')

    response = req.text
    soup = BeautifulSoup(response, 'lxml')
    prices = soup.select('ul#products .prd_thumb_price')

    for result in prices:
        # price 로 '가격', '원' 2개의 요소를 추출한다
        price = result.select_one('.selling-price').get_text()
        # 정규표현식을 사용하여 가격만을 추출
        res = re.findall('\d+[,]\d+', price)
        # join 함수를 사용해서 str로 변환
        final = ''.join(res)
        # replace함수를 사용해서 가격의 가운데 콤마(,)를 공백으로 대체
        get_price = final.replace(',', '')
        # int로 형변환
        real_price = int(get_price)

        print(real_price)


get_price()


def get_product_muchim():
    """
    img: 상품이미지
    product_no: 상품등록번호(추정)
    company_name: 회사이름
    food_name: 상품명(현재 정규표현식에 문제가 있어 수정 중)
    weight_check: 상품무게

    문제점 1. '아이반찬 2종세트' 와 같이 중간에 숫자가 들어간
            텍스트를 제외하고 출력함에 어려움을 겪고 있음
    문제점 2. 정규표현식으로 food_name 과 함께
            무게의 2개 숫자가 계속 같이 딸려옴

    이 코드는 주피터 노트북에서 실행 가능함
    :return:
    """
    req = requests.get('https://www.baeminchan.com/side-dish/list.php?cno=30010000')

    response = req.text
    soup = BeautifulSoup(response, 'lxml')

    ul_list = soup.select('ul#products > li')

    for li in ul_list:
        img = li.select_one('img').get('src')

        # li의 a 태그의 ga_id 속성을 추출
        detail_page = li.select_one('a').get('ga_id')

        # li의 a 태그에 ga_name 속성을 추출
        # 아래의 회사/음식이름/무게를 위한 변수로 실제 출력은 이루어지지 않는다
        content = li.select_one('a').get('ga_name')

        # escape '\'를 이용하여 []안의 문자를 추출
        company = re.findall('\[.*\]', content)
        company_name = ''.join(company)

        # []특수기호 안의 문자를 제거, \s 문자부터, 숫자를 제외한 모든 문자까지 추출
        food = re.findall('[\[\]]\s(\w.*)[^\D]', content)
        food_name = ''.join(food)

        # [^\w] 모든 단어는 제외, 숫자부터 다음 2글자를 추출한다
        #                 .. <- 2개 지정한 이유는 g 또는 kg
        weight = re.findall('[^\w]\d+..', content)
        weight_check = ''.join(weight)

        print(img)
        print(detail_page)
        print(company_name)
        print(food_name)
        print(weight_check)


get_product_muchim()