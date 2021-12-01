# 호텔명 -> 영한 바꾸는 것 처리
# 같은 호텔인지 확인하기
# 호텔 검색 시 규칙 정의
import datetime
import re
from datetime import timedelta
from difflib import SequenceMatcher
from haversine import haversine


def similar(a, b):
    # a : origin, b : to compare; key: name, loc, latitude, longitude
    if check_distance(a['latitude'], a['longitude'], b['latitude'], b['longitude']):
        if check_loc(a['loc'], b['loc']):
            if check_name(a['name'], b['name']):
                return True
    return False


def check_name(a, b):
    # a : search keyword, b : search result name
    res = SequenceMatcher(None, a, b).ratio()
    if res > 0.6:
        return True
    return False


def check_distance(a_x, a_y, b_x, b_y):
    origin = (a_x, a_y)
    compare = (b_x, b_y)

    res = haversine(origin, compare, unit='km')
    if res > 5.0:
        return False
    return True


def check_loc(a, b):
    if a == b:
        return True
    return False


def cleansing(text, type=None):
    if type == 'URL':
        main_url = "https://www.hotelnjoy.com"
        text = re.search("(?P<url>/[^\s]+)", text).group("url")
        text = text.replace(");", "")
        text = main_url + text

        return text

    # (), [] 및 사이 단어들 제거
    pattern = '[\(\[].*?[\)\]]'
    text = re.sub(pattern, repl='', string=text)

    # 관광호텔 제거
    text = text.replace('관광호텔', '')

    # 공백 제거
    text = text.replace(" ", "")

    return text


def calc_date(text, mode=None):
    days = timedelta(days=1)
    convert_date = datetime.datetime.strptime(text, "%Y-%m-%d").date()
    if mode:
        convert_date = convert_date + timedelta(days=7)
    in_date = convert_date.isoformat()
    out_date = (convert_date + days).isoformat()
    return in_date, out_date


if __name__ == '__main__':
    print(calc_date('2021-12-25'))