import pandas as pd
from _load_data import get_districtCode
from _utils import get_encoding

# 자치구 코드 맵핑 정보 가져오기
district_dict=get_districtCode()

# 파일 경로
fpath = "C:/Users/yoonjin/DE6/4_DataWarehouse/project/data"
fname = "/raw_data/지역사회+건강통계(건강행태).csv"
result=get_encoding(fpath,fname) 
# columns 설정될때 2018, 2019가 중복되니까 자동적으로 뒤에 2018.1, 2018.2 등 데이터가 자동으로 붙음
# 그래서 이 데이터는 header=None 옵션을 줌
df = pd.read_csv(fpath+fname, encoding=result['encoding'], header=None)
# 서울시 데이터 제외

year_row = df.iloc[0]
cat1_row = df.iloc[1]
cat2_row = df.iloc[2]

temp_columns=[]
# 데이터가 -가 아닌 열만 가져오기 (현재 구조 바꿔야함)
for idx, a in enumerate(year_row):
    if (idx>0) & (not('-' in str(a))):
        year = str(year_row[idx]).strip()
        cat1 = str(cat1_row[idx]).strip()
        cat2 = str(cat2_row[idx]).strip()
        temp_columns.append((year, cat1, cat2, idx))


gu_values = df.iloc[3:, 0].reset_index(drop=True)

# 자치구, 연도, 통계량, 카테고리1, 카테고리2 추출
records=[]
for year, cat1, cat2, col_idx in temp_columns:
    values = df.iloc[3:, col_idx].reset_index(drop=True)
    for gu, val in zip(gu_values,values):
        if pd.notnull(val):
            records.append({
                "자치구": gu,
                "연도": year,
                "카테고리1": cat1,
                "카테고리2": cat2,
                "값": val
            })

df = pd.DataFrame(records)
df = df[df["자치구"]!="서울시"]

df['자치구코드'] = df['자치구'].map(district_dict)

df = df[['자치구코드','자치구', '연도', '카테고리1','카테고리2','값']]
df = df.sort_values(by=['자치구코드','연도','카테고리1'], ascending=[True,True,True])
df.rename(columns={
    '자치구코드': 'disctrict_code',
    '자치구': 'district',
    '연도': 'year',
    '카테고리1' : 'cat1',
    '카테고리2' : 'cat2',
    '값': 'val',
}, inplace=True)

df.to_csv(fpath+'/clean_data/health_clean.csv', index=False)