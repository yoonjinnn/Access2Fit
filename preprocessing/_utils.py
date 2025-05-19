import chardet

def get_encoding(fpath, fname):
    # 한글이 있어서 인코딩 형식 판단해주는 chardet 추가해봄
    with open(fpath+fname, 'rb') as f:
        result = chardet.detect(f.read(10000))  # 앞부분만 샘플링
        # 출력예시
        # {'encoding': 'EUC-KR', 'confidence': 0.99, 'language': 'Korean'}
    return result