# coding: utf-8
import os
import glob
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from collections import defaultdict
import csv
import json
from operator import itemgetter

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

data_path = os.getcwd()


def readfile(path, filename):
	'''
	Reads file contents
	Parameters:
	path (str) : File path
	filename : File to be read
	Returns:
		file_as_string (str) : file contents as string
	'''
	with open(path + filename) as file:
		file_as_list = file.readlines()
		file_as_string = ''.join(map(str, file_as_list))

	return file_as_string

def preprocess(text):
	'''
	Convert text file into list of normalized tokens
	Parameters:
	    text (str) : text to be preprocessed

	Returns:
	    normalized (str) : list of normalized tokens
	'''
	normalized = []
	text = text.lower()
	text = re.sub(r'\b[0-9]+\b', '', text) # Removes terms containing only numbers
	tokens = word_tokenize(text) # divides string into lists of substrings
	text_list = [i for i in tokens if not i in stop_words] # Removing stopwords
	for word in text_list:
		word = re.sub(r'[^\w\s]','',word) # Removes punctuation characters (except underscore)
		word = re.sub(r'\_','',word)
		# stemmed_word = wordnet_lemmatizer.lemmatize(word)
		stemmed_word = (stemmer.stem(word)) # It takes out the root of the word
		normalized.append(stemmed_word)
	return normalized


def create_index(terms, docID):
	'''
	Creates Inverted Index using dictionary data structure and then saves dictionary in a json file.

	Parameters:
	    text (str) : text to be indexed in dictionary
	    docID (str) : Unique document ID
	'''
	with open(data_path+'/dict.json', 'r') as index:
		ivdict = json.loads(index.read())
	for term in terms:
		if term in ivdict:
			postings_list = [posting[0] for posting in ivdict[term]]
			if docID in postings_list:
				ivdict[term][-1][1] += 1
			else:
				ivdict[term].append([docID,1])         
		else:
			ivdict.update({term : [[docID,1]] })

	index_file = open(data_path+"/dict.json","w")
	index_file.write(json.dumps(ivdict))
	index_file.close()
	return

def search(query):
	'''
	Returns list of documents containing the terms present in query

	Parameters:
	    query (str) : Query received from user input
	Returns:
	    A list of documents containing query terms
	'''
	# ** QUERY OPTIMIZATION **
	query_list = query
	postings = []
	query_output = []
	# Load Inverted Index
	with open(data_path+"/dict.json","rb") as iv:
		ivdict = json.load(iv)
	# Sorting postings lists based on document frequency for query optimization
	for query in query_list:
		postings.append([ivdict[query],len(ivdict[query])])
	postings = sorted(postings, key = itemgetter(1), reverse=False)
	first_list = [posting[0] for posting in postings[0][0]]
	for posting in postings:
		second_list = [list_item[0] for list_item in posting[0]]
		fp = 0 # pointer to first list
		sp = 0 # pointer to second list
		while fp<len(first_list) and sp<len(second_list):
			if first_list[fp]==second_list[sp]:
				if first_list[fp] not in query_output:
					query_output.append(first_list[fp])
				fp += 1
				sp += 1
			elif first_list[fp] < second_list[sp]:
				fp += 1
			else:
				sp += 1
		first_list = query_output

	return query_output

path = os.getcwd() + '/document_collection/'
files = os.listdir(path)
docID=1
docID_map = {} # mapping doc IDs to the filenames
for filename in files:
	print(filename)
	text = readfile(path, filename)
	terms = preprocess(text)
	create_index(terms, docID)
	docID_map[docID] = filename
	docID += 1


# Conjunctive query
query = input()
query = preprocess(query)

query_output = search(query)

# Retrieving file name
for doc_item in query_output:
	print(docID_map[doc_item])
