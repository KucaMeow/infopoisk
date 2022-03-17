import nltk
from bs4 import BeautifulSoup
from os import walk
import pymorphy2

# ----Код аналогичен второму заданию, просто ещё раз отдельно проворачиваю похожие вещи для создания индексов
# Список для исключения союзов и предлогов
invalid_poses = ['CONJ', 'PREP']
# Вместо списка использую словарь Токен - Список документов, где встречается
token_file = dict()

morph = pymorphy2.MorphAnalyzer()

# Получение токенов (отдельных слов)
# Сначала прохожусь по всем файлам из папки pages (где в первом задании сохранил все страницы)
filenames = next(walk('../pages'), (None, None, []))[2]
for filename in filenames:
    with open('../pages/'+filename, mode='r', encoding='utf-8') as file:
        # Читаю текст из файла и с помощью библиотеки обрабатываю теги
        data = file.read()
        soup = BeautifulSoup(data, features='html.parser')
        # В википедии слова находятся в отедельных тегах <p>
        if not soup.find('p'):
            continue
        # Получаю все слова из тегов и очищаю их от знаков препинания, а так же делю на слова
        page_tokens = nltk.word_tokenize(' '.join(soup.find('p').stripped_strings).lower())
        # Записываю эти токены в список токенов, если они не союз или предлог
        for token in page_tokens:
            parsed_token = morph.parse(token)[0]
            if parsed_token.tag.POS and parsed_token.tag.POS not in invalid_poses:
                if token not in token_file.keys():
                    token_file[token] = [filename[:-4]]
                else:
                    token_file[token].append(filename[:-4])

# Получаю леммы. Для этого создаю словарь: Лемма - Список тоекнов
lemma_mapping = dict()
for token in token_file.keys():
    parsed_token = morph.parse(token)[0]
    # Как лемму беру начальную форму слова в токене
    token_lemma = parsed_token.normal_form
    # Добавляю токен в этот словарь по леммам
    if token_lemma not in lemma_mapping.keys():
        lemma_mapping[token_lemma] = [token]
    else:
        lemma_mapping[token_lemma].append(token)

# Сохраняю индексы
with open('../indexes.txt', mode='w', encoding='utf-8') as indexes:
    for key, values in lemma_mapping.items():
        docs = []
        for value in values:
            docs = docs + token_file[value]
        indexes.write(f'{key} {" ".join(set(docs))}\n')