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
    print("a : {0}, \n b: {1}".format(a, b))
    if check_distance(a['latitude'], a['longitude'], b['latitude'], b['longitude']):
        # if check_loc(a['loc'], b['loc']):
        if check_name(a['name'], b['name']):
            print('** The room is same!')
            return True
    return False


def check_name(a, b):
    # a : search keyword, b : search result name
    res = SequenceMatcher(None, a, b).ratio()
    print('>> Check name : ', res)
    if res > 0.6:
        return True
    return False


def check_distance(a_x, a_y, b_x, b_y):
    origin = (float(a_x), float(a_y))
    compare = (float(b_x), float(b_y))
    try:
        res = haversine(origin, compare, unit='km')
        print('>> Check distance : ', res)
        if res > 5.0:
            return False
    except TypeError:
        return False
    return True


def check_loc(a, b):
    print('>> Check location : ', a == b)
    if a == b:
        return True
    return False


def calc_weekend_price(price):
    price = int(price.replace(',', '')) * 1.2
    price = '{:,.0f}'.format(price)
    return price


def get_hotel_en(text):
    pattern = '[\(\[].*?[\)\]]'
    text = re.search(pattern, text)
    text = text.group()
    text = text.replace(')', '')
    text = text.replace('(', '')

    return text


def get_room_area(text):
    pattern = '\d+m²'
    text = re.search(pattern, text)
    if text:
        return text.group()
    else:
        return False


def cleansing(text, type=None):

    # (), [] 및 사이 단어들 제거
    pattern = '[\(\[].*?[\)\]]'
    text = re.sub(pattern, repl='', string=text)

    if type == 'HOTEL':
        return text.rstrip()

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


def cleansing_rate(text):
    text = str(text)
    text = text.replace(" ", "")
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    if re.search('기간만료', text):     # 기간만료, 5성급(기간만료)
        text = '기간만료'
    elif re.search('신청완료|신청중', text):   # 신청중, 등급신청완료, 호텔등급신청중\r\n(코로나로 인한 연기)
        text = '신청중'
    elif re.search('^\d{4,8}|없음|-|만료|예정|_|미등급|가족|호스텔|호스급|미대상|미신청|소형호텔|X|x|제외|신규|미해당|미정|준비중', text):
        text = ''
    elif re.search('평가|심사|심의|결정|보류', text):
        text = '평가중'
    elif re.search('^\d$', text):    # 숫자만 있는 경우(1, 2 ... )
        text = text + '성급'
    elif re.search('특\d등급|특\d급', text):  # 특~등급 > ~성급
        if text == '특1등급':
            text = '5성급'
        elif text == '특2등급' or text == '특2급':
            text = '4성급'
    elif re.search('\d등급', text):   # ~등급 > ~성급
        if text == '1등급':
            text = '3성급'
        elif text == '2등급':
            text = '2성급'
        elif text == '3등급':
            text = '1성급'
        elif text == '4등급':
            text = '4성급'
    elif re.search('\d성', text):    # ~성 > ~성급
        text = text + '급'
    return text


if __name__ == '__main__':
    print(calc_date('2021-12-25'))
