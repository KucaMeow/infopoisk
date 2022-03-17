import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# Поиск
def find(word):
    # Перевожу слово в лемму, по которой храняться индексы
    parsed_word = morph.parse(word)[0]
    lemma = parsed_word.normal_form

    # Открываю файл с индексами и прохожусь по каждой строке
    with open('../indexes.txt', mode='r', encoding='utf-8') as index_file:
        lines = index_file.readlines()
        for line in lines:
            # Если нашлось слово, то возвращаю список номеров документов
            if lemma in line:
                return list(map(int, line.split(' ')[1:]))
    # Иначе, если такого слова нет, возвращаю пустой список (его нигде нет)
    return []


print('Запрос должен выглядеть так: \"WORD\" or \"WORD1 And|Or WORD2\"')
print('Чтобы закончить, введите \"Стоп\"')
while True:
    request = input().lower()
    if 'стоп' in request:
        break
    if len(request.split(' ')) == 3 and ('or' in request or 'and' in request):
        words = request.split(' ')
        word1 = find(words[0])
        word2 = find(words[2])

        if 'or' in request:
            print('For ' + request + ': ' + str(set(word1 + word2)))
        else:
            print('For ' + request + ': ' + str([w for w in word1 if w in word2]))
    elif len(request.split(' ')) == 1:
        print('For word ' + request + ': ' + str(find(request)))
    else:
        print("Error. Must be \"WORD\" or \"WORD1 And|Or WORD2\"")