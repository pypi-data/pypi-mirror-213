import pandas as pd

def find_sentences_with_keywords(file_path, keywords):
    # 파일 불러오기 (인코딩 지정)
    with open(file_path, 'r', encoding='cp949') as file:
        text = file.read()

    # 문장 분리
    sentences = text.split('.')

    # 키워드를 포함하는 문장 찾기
    found_sentences = []
    for sentence in sentences:
        sentence_keywords = []
        for keyword in keywords:
            if keyword in sentence:
                sentence_keywords.extend([keyword] * sentence.count(keyword))
        if sentence_keywords:
            found_sentences.append((sentence.strip(), sentence_keywords))

    return found_sentences

def save_sentences_to_excel(sentences, output_file):
    # 데이터프레임 생성
    data = {'Sentence': [], 'Keywords': []}
    for sentence, keyword_list in sentences:
        data['Sentence'].append(sentence)
        data['Keywords'].append(', '.join(keyword_list))

    df = pd.DataFrame(data)

    # 엑셀로 저장
    df.to_excel(output_file, index=False)

if __name__ == '__main__':
    file_path = r'C:\Users\gjaischool\PycharmProjects\pythonProject\neroTextRead\금융규제운영규정.txt'

    # 사용자 입력으로 키워드 받기
    keywords = ['금융', '전자']

    # 문장에서 키워드를 찾아서 결과 얻기
    found_sentences = find_sentences_with_keywords(file_path, keywords)

    # 결과 출력
    for sentence, keyword_list in found_sentences:
        print(f'Sentence: {sentence}')
        print(f'Keywords: {", ".join(keyword_list)}')
        print()

    # 결과를 엑셀 파일로 저장
    output_file = '검색결과.xlsx'
    save_sentences_to_excel(found_sentences, output_file)









