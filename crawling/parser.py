from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def get_main_dish():
    """
    배민찬의 메인반찬 페이지의 전체보기 리스트를 크롤링

    - 아래의 추출 리스트 중 반찬이름의 정규표현식 수정이 필요합니다

    크롤링한 리스트
    (추출리스트: 변수명, (타입))

    이미지 사진: img, (str)
    상품번호: product_no, (str)
    상세페이지 url: detail_no, (str)
    생산자: supplier_name, (str)
    반찬이름: food_name, (str)
    무게: weight_check (str)
    가격: price (int)
    :return:
    """
    # 경로: 배민찬 > 메인반찬 > 전체보기
    base_url = 'https://www.baeminchan.com/main-courses/list.php?cno=30030000&page={}'

    # for 문을 돌려서 20개의 페이지를 추출
    for i in range(20):
        # base_url 과 base_url 안의 page={} 를 i 변수로 설정하여 1씩 증가
        url = base_url.format(i + 1)

        # 메인반찬의 각 페이지의 객체를 추출
        webpage = urlopen(url)
        # soup 변수에 BeautifulSoup 라이브러리, lxml 모듈 설치
        soup = BeautifulSoup(webpage, 'lxml')
        # CSS에서 id선택자는 고유하기 때문에 ul태그의 products를 선택하여 li만 선택
        ul_list = soup.select('ul#products > li')

        # ul_list를 for문을 돌려서 각 리스트의 요소를 담는다
        for li in ul_list:
            # src 요소 안에 추출하고자 하는 텍스트가 담겨있어 get('src')를 사용
            img = li.select_one('img').get('src')

            # ga_id 요소 안에 추출하고자 하는 텍스트가 담겨있어 get('ga_id')를 사용
            # ga_id 는  메인반찬 > 고기반찬/해산물반찬/생선반찬 등 카테고리를 구분할 수 있는 id값
            product_no = li.select_one('a').get('ga_id')

            # href 는 각 반찬이름 별로 구분할 수 있는 hash 값이 담겨있음
            detail_no = li.select_one('a').get('href')

            # content는 아래의 생산자/반찬이름/무게가 함께 담겨있어
            # 이 content 변수를 토대로 정규표현식이 이루어진다
            # content의 출력 텍스트 예시 - [미노리키친] 아게다시두부곤약조림 150g
            content = li.select_one('a').get('ga_name')

            print(f'content = {content}')

            # content에 중량이 포함되어 있는지 체크
            # (140g*2개)와 같은 표현은 중량으로 취급하지 않음(그대로 반찬이름으로 들어감)
            if re.compile('.+?\(?(\d*\,?\.?\d+)k?g(?!\*)\)?').match(content):
                # 중량이 포함되어 있으면 생산자, 반찬이름, 중량을 함께 추출하는 정규표현식 작성 - 미노리키친, 아게다시두부곤약조림, 150
                # 중량 단위가 kg이면 문자열에 k 포함
                supplier = re.findall('\[(.*)\]\s?(.+?)\s?\(?(\d*\,?\.?\d+k?)g\)?(\s.+)?', content)
            else:
                # 중량이 없으면 생산자, 반찬이름만 추출하는 정규표현식 작성 - 소중한식사, 명절실속세트
                supplier = re.findall('\[(.*)\]\s?(.+)', content)

            supplier_name = supplier[0][0]
            food_name = ''.join(supplier[0][1::2])

            # 중량이 없으면 문자열 0
            weight_check = supplier[0][2] if len(supplier[0]) >= 4 else '0'

            # 중량이 kg 단위인지 확인 후 그램 단위의 정수로 변환
            if 'k' in weight_check:
                weight_check = int(float(weight_check[:-1]) * 1000)
            else:
                weight_check = int(weight_check.replace(',', ''))

            # 추출하고자 하는 가격은 p 태그가 감싸고 있어 get이 아닌 get_text로 추출
            raw_price = li.select_one('p.selling-price').get_text()
            # re.sub 함수는 선택한 요소를 치환
            # re.sub('[^0-9] 숫자를 제외한 나머지 요소를
            # '' 빈값으로 치환
            # 즉, 숫자를 제외한 나머지를 ''로 변환
            result = re.sub('[^0-9]', '', raw_price)
            # 가격은 장바구니에서 int값으로 계산이 되어야 하기 때문에 int 로 형변환
            price = int(result)

            print(img)
            print(product_no)
            print(detail_no)
            print(supplier_name)
            print(food_name)
            print(weight_check)


get_main_dish()
