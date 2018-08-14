"""
parser.py

products.json의 반찬 상세 페이지 url에 요청을 보내 크롤링하는 메소드 정의
메소들을 crawl.py 파일에서 사용함
"""
import requests
from bs4 import BeautifulSoup
import re


def get_soup(url):
    webpage = requests.get(url).text
    soup = BeautifulSoup(webpage, 'lxml')

    return soup


def parse_name(name):
    # content에 중량이 포함되어 있는지 체크
    # (140g*2개)와 같은 표현은 중량으로 취급하지 않음(그대로 반찬이름으로 들어감)
    if re.compile('.+?\(?(\d*,?\.?\d+)k?g(?!\*)\)?').match(name):
        # 중량이 포함되어 있으면 생산자, 반찬이름, 중량을 함께 추출하는 정규표현식 작성 - 미노리키친, 아게다시두부곤약조림, 150
        # 중량 단위가 kg이면 문자열에 k 포함
        parse = re.findall('\[(.*)\]\s?(.+?)\s?\(?(\d*,?\.?\d+k?)g\)?(\s.+)?', name)
    else:
        # 중량이 없으면 생산자, 반찬이름만 추출하는 정규표현식 작성 - 소중한식사, 명절실속세트
        parse = re.findall('\[(.*)\]\s?(.+)', name)

    # 생산자가 없는 경우
    if not parse:
        supplier_name = ''
        food_name = name
        weight_check = '0'
    else:
        supplier_name = parse[0][0]
        food_name = ''.join(parse[0][1::2])

        # 중량이 없으면 문자열 0
        weight_check = parse[0][2] if len(parse[0]) >= 4 else '0'

        # 중량이 kg 단위인지 확인 후 그램 단위의 정수로 변환
        if 'k' in weight_check:
            weight_check = int(float(weight_check[:-1]) * 1000)
        else:
            weight_check = int(weight_check.replace(',', ''))

    result = (supplier_name, food_name, weight_check)

    return result


def parse_product(soup):
    """
    반찬 상세 페이지에서 Product 인스턴스를 만들기 위한 정보 크롤링
    :param soup: 상세 페이지의 BeautifulSoup 인스턴스
    :return result: 크롤링한 정보를 저장한 딕셔너리 인스턴스
    """
    result = dict()

    product_name = soup.select_one('h1.desc_product_name').text
    result['raw_name'] = product_name
    result['supplier'], result['name'], result['weight'] = parse_name(product_name)

    result['description'] = soup.select_one('p.desc_bt_txt').text if soup.select_one('p.desc_bt_txt') else ''
    result['thumbnail_url'] = soup.select_one('div.image_top > img').get('src')

    origin_price = soup.select_one('del.origin-price')
    sale_price = int(soup.select_one('strong.sale-price').text[:-1].replace(',', ''))
    result['sale_price'] = sale_price

    if origin_price is not None:
        price = int(soup.select_one('del.origin-price').text[:-1].replace(',', ''))
        result['price'] = price
        result['discount_rate'] = round((1 - sale_price / price) * 100)
    else:
        result['price'] = 0
        result['discount_rate'] = 0

    details = soup.select('table.table_detail_info > tbody > tr')

    for detail in details:
        if detail.select_one('th').text == '식품의 유형':
            result['type'] = detail.select_one('td').text
        elif detail.select_one('th').text == '원재료명 및 함량':
            result['materials'] = detail.select_one('td').text
        elif detail.select_one('th').text == '알레르기 유발물질':
            result['alert_allergy'] = detail.select_one('td').text

    result['stock'] = 10
    result['available'] = True

    details = soup.select('dl.desc_info > dt')

    for i, detail in enumerate(details):
        if detail.text == '적립금':
            result['point_amount'] = soup.select_one(f'dl.desc_info > dd:nth-of-type({i+1})').text[:-1].replace(',', '')
        elif detail.text == '배송타입':
            result['delivery_type'] = soup.select_one(f'dl.desc_info > dd:nth-of-type({i+1})').text.strip()
        elif detail.text == '수령요일':
            result['delivery_days'] = soup.select_one('dl.desc_info > dd > strong').text

    print(result)

    return result


def parse_category(soup):
    result = dict()

    result['category'] = soup.select_one('ul.breadcrumb > li:nth-of-type(3) > a').text

    return result


def parse_product_image(soup):
    result = list()

    imgs = soup.select('div.product_detail_img_box > img')

    for img in imgs:
        result.append(img.get('src'))

    return result
