from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize
from nltk.collocations import *

stopwords = ['a', 'about', 'above', 'abortion', 'across', 'after', 'afterwards', 'disney']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'disney', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['in', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'quiz', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'sex', 'sexy', 'sexually', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'the']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['to', 'together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']
stopwords += ['disney']
stopwords += ['the']
stopwords += ['to', 'police', 'lockdown', 'killed', 'zika', 'sobriety', 'sober', 'watch']

with open('headlines.txt', 'r') as myfile:
	data=myfile.read().lower().replace('\n', ' ')

def remove_punctuation(data):
	"""Get rid of spaces and punctuation"""
	line = data.translate(None, '!:@#$/\?-.&()|1234567890')
	wordlist = line.split()	
	return wordlist

def remove_stopwords(wordlist, stopwords):
	"""remove stopwords"""
	list_without_stops = [w for w in wordlist if w not in stopwords]

	return list_without_stops

def get_bigrams(list_without_stops):
	"""Find frequently occurring bigrams"""
	list_without_stops = remove_stopwords()
	bigrams = list(nltk.bigrams(list_without_stops))
	return bigrams

def wordlist_to_freqdict(list_without_stops):
	"""sort wordlist into a dictionary based on the frequency of the words"""
	wordfreq = [list_without_stops.count(p) for p in list_without_stops]
    	freqdict = dict(zip(list_without_stops,wordfreq))
    
    	return freqdict

def sort_freqdict(freqdict):
	"""sort frequency dictionary into a list of words ordered by descending frequency"""
	aux = [(freqdict[key], key) for key in freqdict]
	aux.sort()
	aux.reverse()
	return aux

# def assign_part_of_speech_tags(list_without_stops):
# 	"""classify words based on their part of speech"""

# 	patterns = [
# 	    (r'.*ing$', 'VBG'),
# 	    (r'.*ed$', 'VBD'),
# 	    (r'.*es$', 'VBZ'),
# 	    (r'.*ould$', 'MD'),
# 	    (r'.*\'s$', 'NN$'),
# 	    (r'.*s$', 'NNS'),
# 	    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
# 	    (r'.*', 'NN')
# 	    ]

#     	regexp_tagger = nltk.RegexpTagger(patterns)
#     	speech_tagged = regexp_tagger.tag(list_without_stops)

#     	return speech_tagged