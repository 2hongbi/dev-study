from numpy.lib.shape_base import _put_along_axis_dispatcher
import pandas as pd
import requests
import json
from pandas import json_normalize
from tqdm import tqdm


def find_addr(table):
    if table['시도_1'] =='세종특별자치시':
        addr = NaverAPI(table['시도_1'] +' ' + table['법정동_1'] + ' ' + str(table['번']) + ' ' + str(table['지']))
    else:
        addr = NaverAPI(table['시도_1']+' '+table['시군구_1']+' '+table['법정동_1']+' '+str(table['번'])+' '+str(table['지']))
    #print(addr)
    return addr


def NaverAPI(addr):
    '''
    네이버 API를 사용해 주소로부터 위경도를 추출하는 함수
    '''
    headers = {
    'X-NCP-APIGW-API-KEY-ID' : 'x7fkd3b5zb',
    'X-NCP-APIGW-API-KEY' : '1vAWsmSAnK8jj81UbQ7jBPcmaMD3VNWSph3rJ75T'
    }
    url = f'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={addr}'
    response = requests.get(url, headers = headers)
    try:
        result = json.loads(response.text)
        jibun = result['addresses'][0]['jibunAddress']
        try:
            road = result['addresses'][0]['roadAddress']
        except:
            road = '없음'
        y = float(result['addresses'][0]['y'])
        x = float(result['addresses'][0]['x'])
        value = [jibun, road, y, x]
    except:
        value = ['없음', '없음', float('nan'), float('nan')]
    return value
    

def kakaoAPI(addr):
    '''
    카카오 API를 사용해 주소로부터 위경도를 추출하는 함수 
    '''
    key = '48815410f86948ccb7065f36427d06a1'
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+addr
    headers = {"Authorization": ''}
    response = requests.get(url,headers=headers)
    try:
        result = json.loads(str(response.text))
        match_first = result['documents'][0]['address']
        jibun = result['documents'][0]['address']['address_name']
        try:
            road = result['documents'][0]['road_address']['address_name']
        except:
            road = '없음'
        y = float(match_first['y'])
        x = float(match_first['x'])
        value = [jibun, road,y, x]
    except:
        value = ['없음', '없음', 0, 0]
    return value


def kakaoBdongAPI(longitude,latitude):
    '''
    위경도로부터 해당하는 법정동(B)을 추출하는 함수
    '''
    key = '48815410f86948ccb7065f36427d06a1'
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'
    headers = {'Content-Type':'application/json; charset=utf-8',
              'Authorization':'KakaoAK {}'.format(key)}
    params = {
        'x':longitude,
        'y':latitude
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        result = json_normalize(json.loads(response.text)['documents'][0])
    except:
        result = pd.DataFrame()
    return result


def kakaoBdongAPI(longitude,latitude):
    '''
    위경도로부터 해당하는 행정동(H)을 추출하는 함수
    '''
    key = '48815410f86948ccb7065f36427d06a1'
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'
    headers = {'Content-Type':'application/json; charset=utf-8',
              'Authorization':'KakaoAK {}'.format(key)}
    params = {
        'x':longitude,
        'y':latitude
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        result = json_normalize(json.loads(response.text)['documents'][1])
    except:
        result = pd.DataFrame()
    return result
