import pandas as pd
from _load_data import get_districtCode
from _utils import get_encoding

# 자치구 코드 맵핑 정보 가져오기
district_dict=get_districtCode()

# 파일 경로
fpath = "C:/Users/yoonjin/DE6/4_DataWarehouse/project/Access2Fit/data"
fname = "/raw_data/행정구역(구별).csv"
result=get_encoding(fpath,fname) 
df = pd.read_csv(fpath+fname, encoding=result['encoding'])

# 지표명이 있는 두 번째 행
area_row = df.iloc[1]

temp_columns=[]
# 연도 - df.columns, 면적 - 3열의 면적 (km²) 데이터 위치 정보 담음
for idx, a in enumerate(area_row):
    if "면적 (km²)" in str(a):
        year = str(df.columns[idx]).strip()
        temp_columns.append((year, idx))

# 자치구 목록
gu_values = df.iloc[3:, 1].reset_index(drop=True)

# 자치구, 연도, 면적 추출
records = []
for year, col_idx in temp_columns:
    values = df.iloc[3:, col_idx].reset_index(drop=True)
    for gu, val in zip(gu_values, values):
        if gu != "소계" and pd.notnull(val):
            records.append({"자치구": gu, "연도": year, "면적": val})

df = pd.DataFrame(records)

df['자치구코드'] = df['자치구'].map(district_dict)

df = df[['자치구코드','자치구', '연도', '면적']]
df = df.sort_values(by=['자치구코드','연도'], ascending=[True,True])
df.rename(columns={
    '자치구코드': 'district_code',
    '자치구': 'district',
    '연도': 'year',
    '면적': 'area',
}, inplace=True)

df.to_csv(fpath+'/clean_data/area_clean.csv', index=False)