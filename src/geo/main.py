import psycopg2
import pandas as pd
import geocode
# import wareahouse_report
#host = 'iprlab-postgres.ctzlxhtnx075.ap-northeast-2.rds.amazonaws.com'
#dbname = 'ipr'
#user = 'iprlab'
#pwd = 'ipradmin900!'
#conn = psycopg2.connect('host={0} dbname={1} user={2} password={3}'.format(host, dbname, user, pwd))
#building_rows = pd.read_sql("select * from public.building", conn)

#dis = wareahouse_report.distance_to_ic_must_marker('경기도 포천시 군내면 구읍리 산 54-4')

op = pd.read_excel('./../../data/ratings/2019_hotel_data.xlsx', header=2)
#(op)
print(op, op.columns)
# op['addr'] = op['주소'].apply(lambda x : geocode.NaverAPI(x), axis=1)  # Naver API 변경
op['addr'] = op['주소(도로명주소)'].apply(lambda x : geocode.NaverAPI(x))  # Naver API 변경
op.to_excel('./../../data/ratings/2019_hotel_data_위경도추가.xlsx')
