import pandas as pd
from _utils import get_encoding

# 서울시 상권분석서비스(길단위인구-자치구) 기준으로 구 코드 맵핑하기 위함
def get_districtCode():
    fpath = "C:/Users/yoonjin/DE6/4_DataWarehouse/project/data"
    fname = "/raw_data/서울시 상권분석서비스(길단위인구-자치구).csv"
    result=get_encoding(fpath,fname)    
    df = pd.read_csv(fpath+fname, encoding=result['encoding'])

    # 중복제외
    district_df = df[['자치구_코드','자치구_코드_명']].drop_duplicates().reset_index(drop=True)
    district_dict = dict(zip(district_df['자치구_코드_명'], district_df['자치구_코드']))
    return district_dict