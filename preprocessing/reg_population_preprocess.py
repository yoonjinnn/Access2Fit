import pandas as pd
import csv
from _load_data import get_districtCode
from _utils import get_encoding

# 자치구 코드 맵핑 정보 가져오기
district_dict=get_districtCode()

# 파일 경로
fpath = "C:/Users/yoonjin/DE6/4_DataWarehouse/project/data"
fname = "/raw_data/서울시 등록인구.csv"
result=get_encoding(fpath,fname)

# 이 파일은 특이하게, 모든 데이터가 "" 로 둘러쌓여있고, 맨 마지막에 "" 맵핑이 제대로 되지않아
# df 파일을 불러올때부터 에러발생
# import csv 후 에러 무시하는 옵션이 있길래 추가해봄
df = pd.read_csv(
    fpath+fname,
    quoting=csv.QUOTE_NONE,        # 따옴표 무시 
    encoding=result['encoding'],
    on_bad_lines="skip",           # 에러 줄 무시 (pandas 1.3 이후)
    engine="python"                # C parser보다 유연함
    )    

# "", 앞뒤 공백 제거
df = df.astype(str).replace('"', '', regex=True)
# 위에걸로는 columns 명은 바뀌지 않아서 따로 한번 더 처리해줌
df.columns = df.columns.str.replace('"', '', regex=False).str.strip()
df = df.astype(str).applymap(lambda x: x.strip())


# 동별이 합계가아니고 항목에서는 계인 데이터만 추출
df = df[(df["동별"]!="합계") & (df["항목"]=="계") & (df["연령별"]!="합계")]

data_row = df.iloc[1]
gu_row = df.iloc[1]
age_row = df.iloc[2]

temp_columns=[]
# 연도 - df.columns, 면적 - 3열의 면적 (km²) 데이터 위치 정보 담음
for idx, a in enumerate(data_row):
    # 연도 데이터 중에 값이 비어있는 line이 있다면 제외
    # 여기선 0 case
    if (idx>=4) & (str(a)!=""):
        year = str(df.columns[idx]).strip()
        temp_columns.append((year, idx))

records=[]    
for year, col_idx in temp_columns:
    values = df.iloc[1:, col_idx].reset_index(drop=True)
    districs = df["동별"].iloc[1:].reset_index(drop=True)
    ages = df["연령별"].iloc[1:].reset_index(drop=True)
    for gu, age, val in zip(districs, ages, values):
        # 데이터 중에 nan데이터가 존재해서 제외하기 위함
        # 앞에서 replace쓰느라 str로 바꾸어서 none값이 문자열 nan이 되어버려서 조건문 추가
        if (pd.notnull(val)) & (str(val).lower() != "nan"):
            records.append({
                "자치구": gu,
                "연도": year,
                "연령": age,
                "값": val
            })
            
df = pd.DataFrame(records)
df['자치구코드'] = df['자치구'].map(district_dict)

# 분기별 데이터 들어가있는 것은 데이터 형태 논의 필요
def clean_year(val):
    year=0
    if '.' in str(val):
        val = str(val).split('.')
        val[0] = val[0].strip()
        val[1] = val[1].strip()
        if val[1] == "1/4":
            year = int(val[0]+'1')
        elif val[1] == "2/4":
            year = int(val[0]+'2')
        elif val[1] == "3/4":
            year = int(val[0]+'3')
        elif val[1] == "4/4":
            year = int(val[0]+'4')
    else:
        year = int(val.replace('년', '').strip())
    return year

df["연도"] = df["연도"].apply(clean_year)
#원래 바로 category 쓰려고했으나 0~4세, 100세 이상, 10~14세 / 55~59세, 5~9세, 60~64세 순으로 맵핑되서 사용하지않음
#df["연령코드"] = df["연령"].astype("category").cat.codes + 1
age_list = [
    "0~4세", "5~9세", "10~14세", "15~19세",
    "20~24세", "25~29세", "30~34세", "35~39세",
    "40~44세", "45~49세", "50~54세", "55~59세",
    "60~64세", "65~69세", "70~74세", "75~79세",
    "80~84세", "85~89세", "90~94세", "95~99세",
    "100세 이상"
]
df["연령코드"] = pd.Categorical(df["연령"], categories=age_list, ordered=True)
df["연령코드"] = df["연령코드"].cat.codes + 1

df = df[['자치구코드','자치구', '연도', '연령코드', '연령', '값']]
df = df.sort_values(by=['자치구코드','연도','연령코드'], ascending=[True,True,True])
df.rename(columns={
    '자치구코드': 'disctrict_code',
    '자치구': 'district',
    '연도': 'year',
    '연령코드' : 'age_code',
    '연령' : 'age',
    '값': 'val',
}, inplace=True)

df.to_csv(fpath+'/clean_data/reg_population_clean.csv', index=False)