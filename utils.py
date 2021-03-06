from collections import defaultdict

import numpy as np

def sort_data_by_length(data_X, data_y):
    data_X_lens = [len(com) for com in data_X]
    sorted_data_indexes = sorted(range(len(data_X_lens)), key=lambda x: -data_X_lens[x])

    data_X = [data_X[ind] for ind in sorted_data_indexes]
    data_y = [data_y[ind] for ind in sorted_data_indexes]
    return data_X, data_y

def build_word2count(file_path, w2c=None, vocab=None, min_len=1, max_len=10000, n_data=100000000):
    if w2c is None:
        w2c = defaultdict(lambda: 0)
    for i, line in enumerate(open(file_path, encoding='utf-8', errors='ignore')):
        sentence = line.strip().split()
        if len(sentence) < min_len or len(sentence) > max_len:
            continue
        for word in sentence:
            if vocab:
                if word in vocab:
                    w2c[word] += 1
            else:
                w2c[word] += 1
        if i >= n_data:
            break
    return w2c

def encode(sentence, w2i, unksym='<unk>'):
    encoded_sentence = []
    for word in sentence:
        if word in w2i:
            encoded_sentence.append(w2i[word])
        else:
            encoded_sentence.append(w2i[unksym])
    return encoded_sentence

def build_dataset(file_path, vocab_size=1000000, w2c=None, w2i=None, target=False, eos=False, padid=False, unksym='<unk>', min_len=1, max_len=1000, n_data=100000000):
    if w2i is None:
        sorted_w2c = sorted(w2c.items(), key=lambda x: -x[1])
        sorted_w = [w for w, c in sorted_w2c]

        w2i = {}
        word_id = 0
        if eos:
            w2i['<s>'], w2i['</s>'] = np.int32(word_id), np.int32(word_id+1)
            word_id += 2
        if padid:
            w2i['<pad>'] = np.int32(word_id)
            word_id += 1
        if unksym not in sorted_w:
            w2i[unksym] = np.int32(word_id)
            word_id += 1
        w2i_update = {w: np.int32(i+word_id) for i, w in enumerate(sorted_w[:vocab_size-word_id])}
        w2i.update(w2i_update)

    data = []
    for i, line in enumerate(open(file_path, encoding='utf-8', errors='ignore')):
        sentence = line.strip().split()
        if len(sentence) < min_len or len(sentence) > max_len:
            continue
        if target:
            sentence = ['<s>'] + sentence + ['</s>']
        encoded_sentence = encode(sentence, w2i, unksym)
        data.append(encoded_sentence)
        if i >= n_data:
            break
    i2w = {i: w for w, i in w2i.items()}
    return data, w2i, i2w
