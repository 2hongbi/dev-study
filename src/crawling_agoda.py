from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidArgumentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import chromedriver_autoinstaller
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.data_utils import cleansing, get_hotel_en, similar, get_room_area, calc_date, calc_weekend_price
import openpyxl

path = chromedriver_autoinstaller.install()  # 크롬 드라이버 install
driver = webdriver.Chrome(path)


def agoda_search(keyword, check_in_date='2021-12-13', check_out_date='2021-12-14'):
    # 호텔 서치 > 일단 부산만
    # URL = 'https://www.agoda.com/ko-kr/search?city=17172&currency=KRW&languageId=9&origin=KR&rooms=1&adults=2' \
    #        '&children=0&priceCur=KRW&los=1&textToSearch=부산&checkIn='+check_in_date+'&checkOut='+check_out_date
    
    # 서울특별시
    URL = 'https://www.agoda.com/ko-kr/search?city=14690&currency=KRW&languageId=9&origin=KR&rooms=1&adults=2&' \
           'children=0&priceCur=KRW&los=1&textToSearch=서울&checkIn='+check_in_date+'&checkOut='+check_out_date

    # 제주도
    # URL = 'https://www.agoda.com/ko-kr/search?city=16901&currency=KRW&languageId=9&origin=KR&rooms=1&adults=2' \
    #       '&children=0&priceCur=KRW&los=1&textToSearch=제주도&checkIn='+check_in_date+'&checkOut='+check_out_date

    # 경기도
    # URL = 'https://www.agoda.com/ko-kr/search?region=372&locale=ko-kr&languageId=9&origin=KR' \
    #       '&rooms=1&adults=2&children=0&priceCur=KRW&los=1&textToSearch=%EA%B2%BD%EA%B8%B0%EB%8F%84&travellerType=1' \
    #      '&familyMode=off&productType=-1&checkIn='+check_in_date+'&checkOut='+check_out_date

    driver.get(URL)

    time.sleep(random.uniform(3, 6))

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.IconBox__child")))
    # search_box = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[1]/div[1]/div[1]/div/div/div[1]/div')
    # search_box.click()

    # search_key
    search_box = driver.find_element(By.XPATH, '/html/body/div[9]/div/div[1]/div[1]/div[2]/div[1]/div[5]/div/input')
    search_box.send_keys(keyword, Keys.ENTER)

    time.sleep(random.uniform(3, 6))

    # ol class #hotel-list-container

    try:
        search_hotel = driver.find_element(By.CLASS_NAME, 'hotel-list-container')

        time.sleep(random.uniform(3, 6))

        first_hotel = search_hotel.find_element(By.TAG_NAME, 'li')
        first_hotel_url = first_hotel.find_element(By.TAG_NAME, 'a').get_attribute('href')
        return first_hotel_url
    except NoSuchElementException:
        return False


# 아고다 호텔룸의 디테일 정보를 갖고 옴
def get_room_info(element):
    # 방 이름
    room_nm = element.find_element(By.CLASS_NAME, 'MasterRoom__HotelName').text
    print(room_nm)

    time.sleep(random.uniform(3, 6))
    # 방 크기
    room_area = ''
    room_amenities = element.find_elements(By.CLASS_NAME, 'MasterRoom-amenitiesTitle')

    for ra in room_amenities:
        time.sleep(random.uniform(3, 6))
        check_room_area = get_room_area(ra.find_element(By.TAG_NAME, 'div').get_attribute('innerHTML'))
        if check_room_area:
            room_area = check_room_area
    print(room_area)

    # 방 가격
    try:
        price_cont = element.find_element(By.CLASS_NAME, 'PriceContainer')
        room_price = price_cont.find_element(By.CLASS_NAME, 'pd-price').text
        time.sleep(random.uniform(3, 6))
    except NoSuchElementException:
        try:
            price_cont = element.find_element(By.CLASS_NAME, 'cor-tooltip-wrapper')
            room_price = price_cont.find_element(By.CLASS_NAME, 'Typographystyled__TypographyStyled-sc-j18mtu-0').text
            time.sleep(random.uniform(3, 6))
        except NoSuchElementException:
            room_price = price_cont.find_element(By.CLASS_NAME, 'Typographystyled__TypographyStyled-sc-j18mtu-0').text
            time.sleep(random.uniform(3, 6))

    room_price = room_price.replace('₩', '').lstrip()
    print('room_price : ', room_price)

    return room_nm, room_area, room_price


def agoda_detail(url, origin_dic):
    if origin_dic['standard_date'] > '2022-01-31':
        return False

    # path = chromedriver_autoinstaller.install()
    # driver = webdriver.Chrome(path)
    time.sleep(random.uniform(3, 6))

    driver.get(url)

    time.sleep(random.uniform(3, 6))

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/head/meta[11]")))
    # latitude
    latitude = driver.find_element(By.XPATH, '/html/head/meta[11]').get_attribute('content')
    print(latitude)

    time.sleep(random.uniform(3, 6))

    # longitude
    longitude = driver.find_element(By.XPATH, '/html/head/meta[12]').get_attribute('content')
    print(longitude)

    time.sleep(random.uniform(3, 6))
    # address
    # address = driver.find_element(By.XPATH, '/html/head/meta[13]').get_attribute('content')
    # print(address)

    # hotel name
    name = driver.find_element(By.CLASS_NAME, 'HeaderCerebrum__Name').text
    print(name)

    time.sleep(random.uniform(3, 6))

    kor_nm = cleansing(name, type='HOTEL')
    eng_nm = get_hotel_en(name)

    time.sleep(random.uniform(3, 6))

    comp_dic = {'name': kor_nm, 'latitude': latitude, 'longitude': longitude}

    if similar(origin_dic, comp_dic):
        # similar 값이 True 이면 진행
        print(">>> Room details of [{0}]".format(origin_dic['standard_date']))
        try:
            # 맨 위의 방 찾기
            hotel_room = driver.find_element(By.CLASS_NAME, 'MasterRoom')

            time.sleep(random.uniform(3, 6))
            # 방 이름
            room_nm = cleansing(hotel_room.find_element(By.CLASS_NAME, 'MasterRoom__HotelName').text, type='HOTEL')
            print(room_nm)

            time.sleep(random.uniform(3, 6))

            # 방 이름, 방 크기, 가격
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "PriceContainer")))

            hotel_rooms = driver.find_elements(By.CLASS_NAME, 'MasterRoom')

            time.sleep(random.uniform(3, 6))

            index = 1 # room_index
            room_nm, room_area, room_price = get_room_info(hotel_rooms[0])
            print('>> first element of name, area, price : ', room_nm, room_area, room_price)
            if not room_area:
                for idx, hotel_room in enumerate(hotel_rooms[1:]):
                    nm, area, price = get_room_info(hotel_room)
                    if area:
                        index = idx
                        room_nm = nm
                        room_area = area
                        room_price = price
                        break

            print(index, room_nm, room_area, room_price)
            room_price_weekend = calc_weekend_price(room_price)

            crawl_dic = {'hotel_en_nm': eng_nm, 'room_index': index,'room_nm': room_nm, 'room_price': room_price,
                         'room_price_weekend': room_price_weekend,
                         'room_area': room_area, 'standard_date': origin_dic['standard_date']}

            return crawl_dic

        except NoSuchElementException:
            print("*** There's No room between {0} ***".format(origin_dic['standard_date']))
            start_dt, end_dt = calc_date(origin_dic['standard_date'], mode=True)
            url = url.replace(origin_dic['standard_date'], start_dt)
            origin_dic['standard_date'] = start_dt

            agoda_detail(url, origin_dic)
        except InvalidArgumentException:
            return False
    return False


def main():
    # df = pd.read_excel('./../data/hotel_2021_11_29_vol6.xlsx')  # 10개만 실행
    df = pd.read_csv('./../data/hotel_2021_11_29_vol6.csv')
    # df = df[df['호텔명(등록명칭)'] == '아르반시티 호텔']
    df = df[df['지역1(시도)'] == '서울특별시']
    print(df)

    df_values = df.values
    prc = []

    standard_date = '2022-01-10'
    check_in, check_out = calc_date(standard_date)
    try:
        for dfv in df_values:
            org = {'name': cleansing(dfv[4]), 'latitude': dfv[17], 'longitude': dfv[18], 'standard_date': standard_date}
            print('>> ', org)

            detail_url = agoda_search(org['name'], check_in, check_out)
            none_dic = {'hotel_en_nm': '', 'room_index': '', 'room_nm': '', 'room_price': '',
                        'room_price_weekend': '',
                        'room_area': '', 'standard_date': ''}
            if detail_url:
                result = agoda_detail(detail_url, org)
                print(result)
                if result:
                    prc.append(result)
                else:
                    prc.append(none_dic)
            else:
                prc.append(none_dic)
                continue
    except Exception:
        pass
    finally:
        print('>> price_list = ', prc)

        org_df = pd.DataFrame(df_values)
        price_df = pd.DataFrame(prc)
        result = pd.concat([org_df, price_df], axis=1)
        result.to_csv('./result/서울.csv', encoding='utf-8-sig')

        driver.quit()


if __name__ == '__main__':
    main()