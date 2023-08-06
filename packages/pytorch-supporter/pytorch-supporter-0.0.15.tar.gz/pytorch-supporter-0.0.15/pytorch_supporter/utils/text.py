from bs4 import BeautifulSoup
import re

#print(clean_english('테스트 입니다 test this is <b>')) #테스트 입니다 test this is 
def clean_english(text):
    text = BeautifulSoup(text, 'html.parser').text #HTML 태그 제거
    text = text.lower() # 소문자화
    text = re.sub('[!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~]', repl= ' ', string=text) #특수기호 제거, 정규 표현식
    return text

import re
from bs4 import BeautifulSoup

#print(clean_korean('테스트 입니다 test this is <b>')) #테스트 입니다
def clean_korean(text):
    #텍스트 정제 (HTML 태그 제거)
    text = BeautifulSoup(text, 'html.parser').text 
    #텍스트 정제 (특수기호 제거)
    text = re.sub(r'[^ ㄱ-ㅣ가-힣]', '', text) #특수기호 제거, 정규 표현식
    return text
