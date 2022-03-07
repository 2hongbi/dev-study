import random
import time
import pandas as pd
import chromedriver_autoinstaller
from src.data_utils import calc_date, cleansing, similar
from random import uniform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    InvalidArgumentException


# driver = webdriver.Chrome(executable_path='./../webdriver/chromedriver.exe')

def joy_main(hotel):
    # hotel type = dict; name, loc, latitude, longitude
    url = 'https://www.hotelnjoy.com/svc/info/list.php?v_sttdate=2021-12-13&v_enddate=2021-12-14&v_sWord=' + hotel
    print(url)

    path = chromedriver_autoinstaller.install()  # 크롬 드라이버 install
    driver = webdriver.Chrome(path)

    driver.get(url)

    time.sleep(random.uniform(3, 6))

    try:
        # 판매완료 제외 checkbox 해제
        driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[2]/div[1]/ul[2]/li[1]/label/i").click()
    except ElementClickInterceptedException:
        pass

    time.sleep(random.uniform(3, 6))

    hotel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#hotelList")))

    # hotel_list = hotel.find_elements(By.CSS_SELECTOR, "#hotelList > li:not(.block)")
    hotel_list = hotel.find_elements(By.XPATH, "//ul[@id='hotelList']/li[not(@style='display: block;')]")

    time.sleep(random.uniform(3, 6))

    result = []
    if len(hotel_list) > 0:
        for hotel in hotel_list:
            h3 = hotel.find_element(By.TAG_NAME, "h3")
            name = cleansing(h3.text)
            url = cleansing(h3.find_element(By.TAG_NAME, "a").get_attribute("href"), type='URL')
            location = hotel.find_element(By.CLASS_NAME, "sch_loca")
            latitude = location.get_attribute("latitude")
            if latitude != '':
                latitude = float(latitude)
            longitude = location.get_attribute("longitude")
            if longitude != '':
                longitude = float(longitude)

            res = {'name': name, 'loc': location.text, 'latitude': latitude, 'longitude': longitude, 'url': url}
            print(">> res : ", res)
            result.append(res)
    else:
        print(">>> There's no results with {0}".format(hotel))
    return result


def joy_detail(url, start_dt='2021-12-13', end_dt='2021-12-14'):

    path = chromedriver_autoinstaller.install()  # 크롬 드라이버 install
    driver = webdriver.Chrome(path)

    driver.get(url)

    try:
        print(">>> Room details of [{0} ~ {1}]".format(start_dt, end_dt))

        # 호텔 정보
        room = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.roomList")))

        time.sleep(random.uniform(3, 6))

        try:
            # 방 크기
            room_area = room.find_element(By.CLASS_NAME, "res_area").text
            print(room_area)
        except NoSuchElementException:
            # 방 크기에 관한 정보가 없는 경우
            room_area = ''
            print("There's no info about room area.")

        time.sleep(random.uniform(3, 6))

        # 방 이름
        room_name = room.find_element(By.XPATH, '//*[@id="roomListArea"]/ul[1]/li/div[1]/div[1]/div[2]/p').text
        print(room_name)

        time.sleep(random.uniform(3, 6))

        # 방 가격
        room_price = room.find_element(By.XPATH, '//*[@id="roomListArea"]/ul/li/div[1]/div[2]/ul/li[2]/span/b').text
        print(room_price)

        time.sleep(random.uniform(3, 6))

        # 호텔 주소 (검사용)
        # hotel_addr = driver.find_element(By.CLASS_NAME, "add").text
        # print(hotel_addr)

        price_dic = {'room_nm': cleansing(room_name, type='HOTEL_NM'), 'room_price': room_price, 'room_area': room_area, 'standard_date': start_dt}
        time.sleep(random.uniform(3, 6))

        return price_dic

    except TimeoutException:
        print("*** There's No room between {0} & {1} ***".format(start_dt, end_dt))
        start_dt, end_dt = calc_date(start_dt, mode=True)
        joy_detail(start_dt, end_dt)
    except NoSuchElementException:
        pass
    except InvalidArgumentException:
        pass


def main():
    df = pd.read_csv('./../data/busan_hotel_2021_12_01.csv')

    df_values = df.values
    prc = []
    try:
        for dfv in df_values:
            res = {'name': cleansing(dfv[5]), 'loc': dfv[2][:2] + dfv[3], 'latitude': dfv[18], 'longitude': dfv[19]}
            crawling_list = joy_main(res['name'])

            price_dic = {'room_nm': '', 'room_price': '', 'room_area': '', 'standard_date': ''}

            for item in crawling_list:
                if similar(res, item):
                    price_dic = joy_detail(item['url'])
                    print('>> price dic : ', price_dic)
                    break
                else:
                    print('Does not match anything')

            prc.append(price_dic)
    except Exception:
        pass
    finally:
        # org_df = pd.DataFrame(res, index=[0])
        price_df = pd.DataFrame(prc, index=[0])
        # result = pd.concat([org_df, price_df], axis=1)
        price_df.to_csv('test.csv', encoding='utf-8-sig')
        print(price_df)


if __name__ == '__main__':
    print(main())