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
from src.data_utils import cleansing, get_hotel_en, similar, get_room_area, calc_date

path = chromedriver_autoinstaller.install()  # 크롬 드라이버 install
driver = webdriver.Chrome(path)

def agoda_search(keyword, check_in_date='2021-12-13', check_out_date='2021-12-14'):
    # 호텔 서치 > 일단 부산만
    URL = 'https://www.agoda.com/ko-kr/search?guid=bf397690-2f46-488c-bcbd-cff9cffb2b17' \
          '&asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb9' \
          '%2BhzuLOrKzSr6JFEJ0k3mSyfy0007nWWyKbObtVe6S9McO%2F40GalFBfqxHkgpPRBg1f4tMtCkUOcG6AQSFmkuYt' \
          '%2ByDbhank09acW2V3PHXdWgz2CrV%2BniEOdBqQjmR%2FUT4vYBSd86EVFMQNW14nE%2FIg%3D%3D&' \
          'city=17172&tick=637740703793&txtuuid=bf397690-2f46-488c-bcbd-cff9cffb2b17&' \
          'locale=ko-kr&ckuid=b751e731-0680-4493-a511-cc53a607df65&prid=0&' \
          'currency=KRW&correlationId=35bf3988-5ba9-4180-ab23-9b3c567fe6f5&pageTypeId=1&' \
          'realLanguageId=9&languageId=9&origin=KR' \
          '&cid=-1&userId=b751e731-0680-4493-a511-cc53a607df65&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=26' \
          '&currencyCode=KRW&htmlLanguage=ko-kr&cultureInfoName=ko-kr&machineName=hk-crweb-2019&' \
          'trafficGroupId=4&sessionId=qd3vrdnhvdv5lf2vgfu1sdt2&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&' \
          'cttp=4&isRealUser=true&mode=production&checkIn=2021-12-07&checkOut=2021-12-08&rooms=1&adults=2&children=0' \
          '&priceCur=KRW&los=1&textToSearch=%EB%B6%80%EC%82%B0&productType=-1&travellerType=1&familyMode=off'
    URL = URL.replace('2021-12-07', check_in_date)
    URL = URL.replace('2021-12-08', check_out_date)
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


def agoda_detail(url, origin_dic):
    if origin_dic['standard_date'] > '2021-12-31':
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
            # 방 크기
            room_area = ''
            room_amenities = hotel_room.find_elements(By.CLASS_NAME, 'MasterRoom-amenitiesTitle')
            for ra in room_amenities:
                check_room_area = get_room_area(ra.find_element(By.TAG_NAME, 'div').get_attribute('innerHTML'))
                if check_room_area:
                    room_area = check_room_area
            print(room_area)

            time.sleep(random.uniform(3, 6))
            # 방 가격
            price_cont = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "PriceContainer")))
            room_price = price_cont.find_element(By.CLASS_NAME, 'pd-price').text
            room_price = room_price.replace('₩', '').lstrip()
            print(room_price)

            crawl_dic = {'hotel_en_nm': eng_nm, 'room_nm': room_nm, 'room_price': room_price,
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
    df = pd.read_csv('./../data/busan_hotel_2021_12_01.csv').loc[:60]  # 10개만 실행

    df_values = df.values
    prc = []

    standard_date = '2021-12-13'
    check_in, check_out = calc_date(standard_date)
    try:
        for dfv in df_values:
            org = {'name': cleansing(dfv[5]), 'latitude': dfv[18], 'longitude': dfv[19], 'standard_date': standard_date}
            print('>> ', org)

            detail_url = agoda_search(org['name'], check_in, check_out)
            none_dic = {'hotel_en_nm': '', 'room_nm': '', 'room_price': '', 'room_area': '', 'standard_date': ''}
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
        result.to_csv('test.csv', encoding='utf-8-sig')

        driver.quit()


if __name__ == '__main__':
    main()