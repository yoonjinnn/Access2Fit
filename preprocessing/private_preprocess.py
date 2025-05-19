import pandas as pd
from _load_data import get_districtCode
from _utils import get_encoding

# 자치구 코드 맵핑 정보 가져오기
district_dict=get_districtCode()

# 파일 경로
fpath = "C:/Users/yoonjin/DE6/4_DataWarehouse/project/Access2Fit/data"
fname = "/raw_data/서울시 체력단련장업 인허가 정보.csv"
result=get_encoding(fpath,fname) 
df = pd.read_csv(fpath+fname, encoding=result['encoding'])

# 영업상태코드가 1인 데이터만 가져오기 (영업인 데이터만)
# 1 - 영업/정상, 2 - 휴업, 3 - 폐업, 4 - 취소/말소/만료/정지/중지, 5 - 제외/삭제/전출
df = df[df['영업상태코드'] == 1]

# 지번주소와 도로명주소가 둘 다 결측인 경우 제외 (자치구 데이터를 가져올 수 없기 때문)
# 현재 data는 0case이긴 함
df = df[~(df['지번주소'].isna() & df['도로명주소'].isna())]

# 지번주소 또는 도로명주소에서 '자치구' 추출 (띄어쓰기 기준 1번째 요소)
def extract_gu(row):
    address = row['지번주소'] if pd.notna(row['지번주소']) else row['도로명주소']
    try:
        return address.split()[1]   # [0]: 시, [1]: 자치구
    except IndexError:
        return None

# df.apply(함수, axis, ...) : 특정함수를 데이터 프레임의 행또는 열에 적용
df['자치구'] = df.apply(extract_gu, axis=1)
df['자치구코드'] = df['자치구'].map(district_dict)
df['연도'] = df['인허가일자'].str.split('-').str[0]

df = df[['자치구코드','자치구','연도','사업장명']]
df = df.sort_values(by=['자치구코드','연도','사업장명'], ascending=[True,True,True])
df.rename(columns={
    '자치구코드': 'district_code',
    '자치구': 'district',
    '연도': 'year',
    '사업장명': 'private_name',
}, inplace=True)

df.to_csv(fpath+'/clean_data/seoul_private_clean.csv', index=False)
