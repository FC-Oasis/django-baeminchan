import requests
from bs4 import BeautifulSoup

from .models import BmcDataMuchim


def collect_bmc_muchim():
    """
    밑반찬 리스트를 requests(200)로 받고
    Beautifulsoup 로 변환

    for문을 돌려서 ul#products에 있는 리스트를
    title, price, image를 순서대로 받아서 item 에 할당

    생성된 객체는 muchim에 저장

    :param request: string 값으로 받음
    :return: 배민찬의 밑반찬 리스트
    """
    request = requests.get('https://www.baeminchan.com/side-dish/list.php?cno=30010000')
    response = request.text

    soup = BeautifulSoup(response, 'lxml')

    ul = soup.select('ul#products > li')

    for item in ul:
        title = item.select_one('a').get('ga_name')
        price = item.select_one('p').get_text()
        image = item.select_one('img').get('src')

        muchim = BmcDataMuchim.objects.create(
            title=title,
            price=price,
            image=image,
        )
        return muchim
