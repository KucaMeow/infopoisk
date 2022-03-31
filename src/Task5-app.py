import math

from easygui import *
from os import walk
import nltk
from bs4 import BeautifulSoup

filenames = next(walk('../vector'), (None, None, []))[2]

vectors = dict()
tokens = []
urls = []

for filename in filenames:
    with open('../vector/' + filename, mode='r', encoding='utf-8') as doc:
        lines = doc.readlines()
        vector = []
        for line in lines:
            if line != '\n':
                vector.append(line)
        vectors[filename] = vector

for i in range(100):
    if str(i) not in vectors.keys():
        vectors[str(i)] = [0.0, 0.0]

with open('../all-tokens-vector-direction.txt', mode='r', encoding='utf-8') as token_file:
    tokens = token_file.readlines()
with open('../index.txt', mode='r', encoding='utf-8') as file:
    urls = file.readlines()

filenames = next(walk('../pages'), (None, None, []))[2]
token_inverted_index = dict()

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


def vectorFromQuery(query_t):
    words = query_t.split(' ')
    tf_idf = dict()
    for word in words:
        if word+'\n' in tokens:
            tf_idf[word] = 1
    vector_t = []
    for token_t in tokens:
        if token_t[:-1] in words:
            vector_t.append(tf_idf[token_t[:-1]])
        else:
            vector_t.append(0)
    return vector_t


def compare(vec1, vec2):
    if len(vec1) != len(vec2):
        return -1
    a = 0
    b = 0
    c = 0
    for i in range(len(vec1)):
        a += float(vec1[i]) * float(vec2[i])
        b += float(vec1[i]) * float(vec1[i])
        c += float(vec2[i]) * float(vec2[i])
    if (b == 0.0) | (c == 0.0):
        return -1
    return abs(a / (math.sqrt(b) * math.sqrt(c)))


def getSimmilar(query_t):
    vec = vectorFromQuery(query_t)
    to_return = urls.copy()

    to_return.sort(key=lambda a: compare(vec, vectors[a.split(' ')[0]]))

    most_similar = to_return.pop()
    if compare(vec, vectors[most_similar.split(' ')[0]]) <= 0:
        return 'Нет результата'
    else:
        return most_similar.split(' ')[1] + ' с похожестью ' + str(compare(vec, vectors[most_similar.split(' ')[0]]))

def creatingQuery():
    values = enterbox('Введите запрос', 'Запрос')
    query_tmp = values
    return query_tmp


def showSearchResult(query_t):
    msg = getSimmilar(query_t)
    msgbox(msg, 'Результат самых похожих:', 'Назад')


while True:
    query = creatingQuery()
    if query is None:
        break
    if len(query.split(' ')) < 1:
        continue
    showSearchResult(query)
