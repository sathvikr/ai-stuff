# Chapter 2
# 26
from nltk.corpus import brown, wordnet as wn

print("----26----")

num_hyponyms = 0
sum_hyponyms = 0
for synset in wn.all_synsets('n'):
    hyponyms = synset.hyponyms()
    if len(hyponyms) > 0:
        num_hyponyms = num_hyponyms + 1
        sum_hyponyms = sum_hyponyms + len(hyponyms)

print(sum_hyponyms / num_hyponyms)

# 27
print("----27----")


def average_polysemy(category):
    seen_words = []
    num_poly = 0
    sum_poly = 0
    for synset in wn.all_synsets(category):
        if num_poly > 20000:
            break
        for lemma in synset.lemmas():
            lemma_name = lemma.name()
            if lemma_name not in seen_words:
                seen_words.append(lemma_name)
                num_poly = num_poly + 1
                sum_poly = sum_poly + len(wn.synsets(lemma_name, category))
    return sum_poly / num_poly


print(average_polysemy('n'))
print(average_polysemy('v'))
print(average_polysemy('a'))
print(average_polysemy('r'))

# 28
print("----28----")

pairs = [('car', 'automobile'), ('gem', 'jewel'), ('journey', 'voyage'), ('boy', 'lad'), ('coast', 'shore'),
         ('asylum', 'madhouse'), ('magician', 'wizard'), ('midday', 'noon'), ('furnace', 'stove'), ('food', 'fruit'),
         ('bird', 'cock'), ('bird', 'crane'), ('tool', 'implement'), ('brother', 'monk'), ('lad', 'brother'),
         ('crane', 'implement'), ('journey', 'car'), ('monk', 'oracle'), ('cemetery', 'woodland'), ('food', 'rooster'),
         ('coast', 'hill'), ('forest', 'graveyard'), ('shore', 'woodland'), ('monk', 'slave'), ('coast', 'forest'),
         ('lad', 'wizard'), ('chord', 'smile'), ('glass', 'magician'), ('rooster', 'voyage'), ('noon', 'string')]
lch = []
for word1, word2 in pairs:
    lch.append((word1, word2, wn.lch_similarity(wn.synsets(word1)[0], wn.synsets(word2)[0])))
from operator import itemgetter

print(sorted(lch, key=itemgetter(2), reverse=True))


# Chapter 4

def insert(trie, key, value):
    if key:
        first, rest = key[0], key[1:]
        if first not in trie:
            trie[first] = {}
        insert(trie[first], rest, value)
    else:
        trie['value'] = value


# 16

print("----16----")

import nltk

trie = nltk.defaultdict(dict)
insert(trie, 'chat', 'cat')
insert(trie, 'chien', 'dog')
insert(trie, 'chair', 'flesh')
insert(trie, 'chic', 'stylish')


def pprint_trie(trie, line=''):
    if 'value' in trie:
        print(line + ': \'' + trie['value'] + '\'')
        return
    for index, key in enumerate(sorted(trie.keys())):
        if (index == 0):
            pprint_trie(trie[key], line + key)
        else:
            pprint_trie(trie[key], ('-' * len(line)) + key)


pprint_trie(trie)

# 20
import nltk

print("----20----")


def summarize(text_sents, n):
    from operator import itemgetter
    freqDist = nltk.FreqDist([w.lower() for sent in text_sents for w in sent])
    scoresSents = [(sum(freqDist[word] for word in sent), index, sent) for (index, sent) in enumerate(text_sents)]
    sortByFreq = sorted(scoresSents, key=itemgetter(0), reverse=True)[:n]
    sortByIndex = sorted(sortByFreq, key=itemgetter(1))
    for (freq, index, sent) in sortByIndex:
        print(index, ': ', sent, '\n')


summarize(brown.sents(categories='religion'), 10)
