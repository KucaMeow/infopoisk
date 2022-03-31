import nltk
from bs4 import BeautifulSoup
from os import walk
import pymorphy2
import math

invalid_poses = ['CONJ', 'PREP']
morph = pymorphy2.MorphAnalyzer()
inverted_index = dict()
token_inverted_index = dict()

# Загружаю все номера документов, где содержится лемма
with open('../indexes.txt', encoding='utf-8') as input_file:
    lines = input_file.readlines()
    for line in lines:
        word = line.rstrip().split(' ')[0]
        docs = line.rstrip().split(' ')[1:]
        inverted_index[word] = docs


# Загружаю все файлы в filenames
filenames = next(walk('../pages'), (None, None, []))[2]
N = len(filenames)

for filename in filenames:
    with open('../pages/' + filename, mode='r', encoding='utf-8') as file:
        data = file.read()
        soup = BeautifulSoup(data, features='html.parser')
        if not soup.find('p'):
            continue
        page_tokens = nltk.word_tokenize(' '.join(soup.find('p').stripped_strings).lower())
        for token in page_tokens:
            if token not in token_inverted_index.keys():
                token_inverted_index[token] = []
            if filename not in token_inverted_index[token]:
                token_inverted_index[token].append(filename)

for filename in filenames:
    # Массив токенов документа
    cleaned_tokens = []
    # Подсчет лемм в документе
    cleaned_lemmas_amount = dict()
    with open('../pages/'+filename, mode='r', encoding='utf-8') as file:
        data = file.read()
        soup = BeautifulSoup(data, features='html.parser')
        if not soup.find('p'):
            continue
        page_tokens = nltk.word_tokenize(' '.join(soup.find('p').stripped_strings).lower())
        print(len(page_tokens))
        for token in page_tokens:
            parsed_token = morph.parse(token)[0]
            if parsed_token.tag.POS and parsed_token.tag.POS not in invalid_poses:
                token_lemma = parsed_token.normal_form
                if token_lemma not in cleaned_lemmas_amount.keys():
                    cleaned_lemmas_amount[token_lemma] = 1
                else:
                    cleaned_lemmas_amount[token_lemma] += 1
                cleaned_tokens.append(token)
    tokens_set = set(cleaned_tokens)
    with open(f'../tf-idf-lemmas/lemmas-{filename}', mode='w', encoding='utf-8') as output:
        for lemma in cleaned_lemmas_amount.keys():
            Nw = len(inverted_index[lemma])
            tf = cleaned_lemmas_amount[lemma]
            idf = math.log(Nw/N)
            tf_idf = tf * idf
            output.write(f'{lemma} {idf} {tf_idf}\n')
    with open(f'../tf-idf-tokens/tokens-{filename}', mode='w', encoding='utf-8') as output:
        for token in tokens_set:
            Nw = len(token_inverted_index[token])
            tf = cleaned_tokens.count(token)
            idf = math.log(Nw / N)
            tf_idf = tf * idf
            output.write(f'{token} {idf} {tf_idf}\n')