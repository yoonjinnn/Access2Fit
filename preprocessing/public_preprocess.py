import pandas as pd
from _load_data import get_districtCode
from _utils import get_encoding

# 자치구 코드 맵핑 정보 가져오기
district_dict=get_districtCode()

#파일경로
fpath = "C:/Users/yoonjin/DE6/4_DataWarehouse/project/data"
fname = "/raw_data/서울시 공공체육시설 정보.csv"
result=get_encoding(fpath,fname)
df = pd.read_csv(fpath+fname, encoding=result['encoding'])

# 시설운영상태가 운영인 데이터만 가져옴
df = df[df['시설운영상태'] == '운영'][['자치구', '시설종류', '시설명']]

# 코드화를 위해 자치구는 'ㅇㅇ구'로 통일
def add_gu(value):
    value = str(value)
    if value.endswith('구'):
        return value
    else:
        return value + '구'

df['자치구'] = df['자치구'].apply(add_gu)
df['자치구코드'] = df['자치구'].map(district_dict)

df = df[['자치구코드','자치구','시설종류','시설명']]
df = df.sort_values(by=['자치구코드','시설명'], ascending=[True,True])
df.rename(columns={
    '자치구코드': 'district_code',
    '자치구': 'district',
    '시설종류': 'public_type',
    '시설명': 'public_name',
}, inplace=True)

df.to_csv(fpath+'/clean_data/seoul_public_clean.csv', index=False)
