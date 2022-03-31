from os import walk

filenames = next(walk('../tf-idf-tokens'), (None, None, []))[2]
doc_tokens = dict()
all_tokens = []

# print(filename[7:-4])
for filename in filenames:
    doc_tokens[filename[7:-4]] = dict()
    with open('../tf-idf-tokens/'+filename, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            token_info = line.split(' ')
            doc_tokens[filename[7:-4]][token_info[0]] = token_info[2]
            all_tokens.append(token_info[0])

tokens = list(set(all_tokens))

vectors = dict()

for doc in doc_tokens.keys():
    vectors[doc] = []
    for token in tokens:
        if token in doc_tokens[doc].keys():
            vectors[doc].append(doc_tokens[doc][token])
        else:
            vectors[doc].append(0)

for doc in doc_tokens.keys():
    with open('../vector/'+doc, mode='w', encoding='utf-8') as file:
        for el in vectors[doc]:
            file.write(f'{el}\n')

with open('../all-tokens-vector-direction.txt', mode='w', encoding='utf-8') as file:
    for token in tokens:
        file.write(f'{token}\n')