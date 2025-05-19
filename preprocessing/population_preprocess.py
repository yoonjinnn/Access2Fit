import pandas as pd
from _utils import get_encoding

# 파일 경로
fpath = "C:/Users/yoonjin/DE6/4_DataWarehouse/project/data"
fname = "/raw_data/서울시 상권분석서비스(길단위인구-자치구).csv"

result=get_encoding(fpath,fname)

df = pd.read_csv(fpath+fname, encoding=result['encoding'])
df = df.sort_values(by=['자치구_코드','기준_년분기_코드'], ascending=[True,True])
df.rename(columns={
    '기준_년분기_코드': 'year_code',
    '자치구_코드': 'district_code',
    '자치구_코드_명': 'district',
    '총_유동인구_수': 'total',
    '남성_유동인구_수': 'male',
    '여성_유동인구_수': 'female',
    '연령대_10_유동인구_수': 'age_10',
    '연령대_20_유동인구_수': 'age_20',
    '연령대_30_유동인구_수': 'age_30',
    '연령대_40_유동인구_수': 'age_40',
    '연령대_50_유동인구_수': 'age_50',
    '연령대_60_이상_유동인구_수': 'age_60over',
    '시간대_00_06_유동인구_수': 'time_0006',
    '시간대_06_11_유동인구_수': 'time_0611',
    '시간대_11_14_유동인구_수': 'time_1114',
    '시간대_14_17_유동인구_수': 'time_1417',
    '시간대_17_21_유동인구_수': 'time_1721',
    '시간대_21_24_유동인구_수': 'time_2124',
    '월요일_유동인구_수': 'mon',
    '화요일_유동인구_수': 'tue',
    '수요일_유동인구_수': 'wed',
    '목요일_유동인구_수': 'thu',
    '금요일_유동인구_수': 'fri',
    '토요일_유동인구_수': 'sat',
    '일요일_유동인구_수': 'sun',    
}, inplace=True)


df.to_csv(fpath+'/clean_data/seoul_population_clean.csv', index=False)
