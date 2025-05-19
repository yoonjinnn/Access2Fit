import pandas as pd
from _load_data import get_districtCode
from _utils import get_encoding

# 자치구 코드 맵핑 정보 가져오기
district_dict=get_districtCode()

# 파일 경로
fpath = "C:/Users/yoonjin/DE6/4_DataWarehouse/project/data"
fname = "/raw_data/서울시 따릉이대여소 마스터 정보.csv"
result=get_encoding(fpath,fname)
df = pd.read_csv(fpath+fname, encoding=result['encoding'])

# 주소정보가 있는 데이터만 가져오기
# '주소없음'과 경기도 데이터도 포함되어있어서 해당 데이터 제외
df = df[df['주소1'].str.contains('서울특별시', na=False)]

# 지번주소 또는 도로명주소에서 '자치구' 추출 (띄어쓰기 기준 1번째 요소)
def extract_gu(row):
    address = row['주소1']
    try:
        return address.split()[1]   # [0]: 시, [1]: 자치구
    except IndexError:
        return None

# df.apply(함수, axis, ...) : 특정함수를 데이터 프레임의 행또는 열에 적용
df['자치구'] = df.apply(extract_gu, axis=1)
df['자치구코드'] = df['자치구'].map(district_dict)

df = df[['자치구코드','자치구', '대여소_ID']]
df = df.sort_values(by=['자치구코드','대여소_ID'], ascending=[True,True])
df.rename(columns={
    '자치구코드': 'disctrict_code',
    '자치구': 'district',
    '대여소_ID': 'station_id',
}, inplace=True)

df.to_csv(fpath+'/clean_data/bicycle_clean.csv', index=False)


