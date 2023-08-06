import pandas as pd

def find_word():
    text_file = input('텍스트 파일의 경로를 입력하세요 : ',)
    my_word = input('찾을 단어를 입력하세요 : ',).split(',')
    # text_file = 'C:\Users\gjaischool\Downloads\금융규제운영규정.txt'
    # my_word = ['금융', '전자']
    found_sentence = []
    all_found_keywords = []
    with open(text_file) as file:
        for line in file:
            input_text = [sentence for sentence in line.split('\n')]
            for sentence in input_text:
                found_keywords = []
                for keyword in my_word:
                    if keyword in sentence:
                        [found_keywords.append(keyword) for i in range(sentence.count(keyword))]
                if found_keywords != []:
                    found_sentence.append(sentence)
                    all_found_keywords.append(found_keywords)

    data = {
        '찾은 문장' : found_sentence,
        '찾은 키워드' : all_found_keywords
    }
    df = pd.DataFrame(data)
    df.to_excel('./찾은 단어 목록.xlsx')
    print('해당 파일을 저장했습니다.')

find_word()

