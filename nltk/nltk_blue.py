import random
import re
from urllib import request
from bs4 import BeautifulSoup

import nltk
from matplotlib import pyplot, pyplot as plt
from nltk import FreqDist
from nltk.corpus import gutenberg, brown, state_union, wordnet as wn, cmudict, stopwords, movie_reviews, words
from nltk.book import text1 as moby_dick, text2 as sense_and_sensibility

# print("4---------------")
# cfd = nltk.ConditionalFreqDist(
#     (target, fileid[:4])
#     for fileid in state_union.fileids()
#     for w in state_union.words(fileid)
#     for target in ['men', 'women', 'people']
#     if w.lower().startswith(target))
#
# cfd.plot()

# print("5--------------")
#
# computer = wn.synset('computer.n.01')
# print(computer.part_meronyms())
# print(computer.part_holonyms())
# print()
#
# people = wn.synset('people.n.01')
# print(people.member_meronyms())
# print(people.member_holonyms())
# print()
#
# paper = wn.synset('paper.n.01')
# print(paper.substance_meronyms())
#
# print("7---------------")
# print(moby_dick.concordance('however'))
# print(sense_and_sensibility.concordance('however'))
#
# print("9---------------")
# news_data = nltk.Text(brown.words(categories='news'))
# religion_data = nltk.Text(brown.words(categories='religion'))
# # trying to find common words
# news_fd = nltk.FreqDist(news_data)
# religion_fd = nltk.FreqDist(religion_data)
# print(news_data.concordance('state'))
# print(religion_data.concordance('state'))
#
# print("12---------------")
# words = [word for word, pron in cmudict.entries()]
# wordset = set(words)
# cmu = cmudict.dict()
# print(len(words))
# print(len(wordset))
# more_than_one_pron = [word for word in wordset if len(cmu.get(word)) > 1]
# print(len(more_than_one_pron) / len(wordset) * 100, "% words have more than one pronounciation")
#
# print("17---------------")
# most_freq_50_fd = nltk.FreqDist(brown.words(categories='news'))
# # fd that includes stop words
# print(most_freq_50_fd.most_common(50))
# words = [word for word in most_freq_50_fd]
# for word in words:
#     if word in stopwords.words('english') or not word.isalpha():
#         most_freq_50_fd.pop(word)
# # fd that excludes stop words
# print(most_freq_50_fd.most_common(50))
#
# print("18---------------")
# bigrams_without_stopwords = []
#
# for a, b in nltk.bigrams(brown.words(categories="romance")):
#     if a not in stopwords.words('english') and b not in stopwords.words('english'):
#         bigrams_without_stopwords.append((a, b))
#
# bigrams_without_stopwords_fd = nltk.FreqDist(bigrams_without_stopwords)
# print(bigrams_without_stopwords_fd.most_common(50))

# print("23---------------")
#
#
# def zipf_law(text):
#     fdist = FreqDist([w.lower() for w in text if w.isalpha()])
#     fdist = fdist.most_common()  # sort the frequency distribution
#     # note that it converts the type from dict to list
#     rank = []
#     freq = []
#     n = 1  # the variable records the rank
#
#     for i in range(len(fdist)):
#         freq.append(fdist[i][1])  # fdist[i][0] is the word
#         # and fdist[i][1] is the corresponding frequency
#         rank.append(n)
#         n += 1
#
#     # I use matplotlib.pyplot istead, since it seems that pylab is discouraged nowadays
#     plt.plot(rank, freq, 'bs')
#     plt.xscale('log')  # set the x axis to log scale
#     # the above two statements are equivalent to: plt.semilogx(rank, freq, 'bs')
#
#     plt.title("Zipf's law")
#     plt.xlabel('word rank')
#     plt.ylabel('word frequency')
#     plt.show()


# zipf_law(brown.words())

# randomText = ''
# for i in range(10000000):
#     randomText = randomText + random.choice("abcdefg ")
# randomWord = randomText.split()
# zipf_law(randomWord)

# print("27---------------")
# import nltk
# from nltk.corpus import wordnet as wn
#
# poly_nouns = list(wn.all_synsets('n'))
# # poly_adjectives = list(wn.all_synsets('adj'))
# # poly_verbs = list(wn.all_synsets('v'))
# # poly_adverbs = list(wn.all_synsets('adv'))
#
#
# def calc_words(synset):
# 	all_words = []
# 	for syn in synset:
# 		all_words += syn.lemma_names()
# 	# eliminates duplicates and gets the count
# 	total = len(set(all_words))
# 	return total
#
# def total_senses(synset):
# 	senses = sum(1 for x in synset)
# 	return senses
#
#
# def average_polysemy(synset):
# 	average = total_senses(synset) / calc_words(synset)
# 	return average
#
#
# print(total_senses(poly_nouns))
# print(calc_words(poly_nouns))
# print(calc_words(poly_nouns))
# print(calc_words(poly_nouns))

# Chapter 3

print("20---------------")
url = "https://www.nltk.org/book/ch03.html"
html = request.urlopen(url).read().decode('utf8')
soup = BeautifulSoup(html)
today = soup.find(class_="info city-fcast-text")
print(today.get_text())

# print("22---------------")


# def unknown(url):
#     """Takes a URL as its argument and returns a list of unknown words that occur on that webpage."""
#
#     # gets the text of the page
#     html = request.urlopen(url).read().decode('utf8')
#     soup = BeautifulSoup(html, features="html.parser")
#     for script in soup.find_all('script'):
#         script.clear()
#     raw = soup.get_text()
#
#     # finds the lower case words by searching for a word boundary plus one or more lower case letters
#     lower_case_words = re.findall(r'\b[a-z]+', raw)
#     junk = set(words.words())
#
#     # searches through the list of lower case words and gets rid of those in the words corpus.
#     unknowns = [word for word in lower_case_words if word not in junk]
#     return unknowns
#
#
# unknown_words = unknown('http://news.bbc.co.uk/')
# print(unknown_words)

# Chapter 6

# print("4---------------")
# documents = [(list(movie_reviews.words(fileid)), category) for category in movie_reviews.categories() for fileid in movie_reviews.fileids(category)]
# random.shuffle(documents)
#
# all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
# word_features = list(all_words.keys())[:2000]
#
# def document_features(document):
#     document_words = set(document)
#     features = {}
#     for word in word_features:
#         features['contains(%s)' % word] = (word in document_words)
#     return features
#
# featuresets = [(document_features(d), c) for (d,c) in documents]
# train_set, test_set = featuresets[100:], featuresets[:100]
# classifier = nltk.NaiveBayesClassifier.train(train_set)
# print(nltk.classify.accuracy(classifier, test_set))
# classifier.show_most_informative_features(30)
