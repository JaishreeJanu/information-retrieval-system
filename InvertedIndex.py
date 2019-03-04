# coding: utf-8
import os
import glob
import nltk
import re
# nltk.download('all')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# nltk.download(stopwords)
from nltk.stem import PorterStemmer
from collections import defaultdict

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

path = os.getcwd() + '/data/'

files = os.listdir(path)


def readfile(path, filename):
	'''
	Reads file given in parameter name "filename".

	Parameters:
		path (str) : Path where file is present
		filename : File to be read

	Returns read file in string type
	'''
	with open(path + filename) as file:
		file_as_list = file.readlines()
		file_as_string = ''.join(map(str, file_as_list))

	return file_as_string

def preprocess(text):
	'''
	Preprocesses text.

	Parameters:
		text (str) : text to preprocessed
	
	Returns:
		stemmed (str) : Preprocessed text
	'''
	stemmed = []
	text = text.lower()
	text = re.sub(r'\d+', '', text)
	text = re.sub(r'[^\w\s]','',text)
	tokens = word_tokenize(text)
	text_list = [i for i in tokens if not i in stop_words]
	for word in text_list:
		stemmed_word = (stemmer.stem(word))
		stemmed.append(stemmed_word)	
	return stemmed


def inverted_index(text,docID):
	'''
	Creates Inverted Index in Data structure called dictionary. Term is index and list of lists is stored as values. Each list item in list is combination of docID and frequency of term in docID.

	Parameters:
		text (str) : text to be indexed in dictionary
		docID (str) : Document Name

	'''
	for term in text:
		if term in ivdict:
			flag=0
			for i in range(len(ivdict[term])):
				if ivdict[term][i][0] == docID:
					ivdict[term][i][1] += 1
					flag=1
					break;
			if flag == 0:
				ivdict[term].append([docID,1])			
		else:
			myList = [[docID,1]]
			ivdict.update({term : myList }) 
	return

def search(query):
	'''
	Returns list of documents containing the terms present in query
	
	Parameters:
		query (str) : Query entered by user 
	Returns:
		A list of documents containing query terms
	'''
	query = list(query.split(" "))
	query1 = query[0]
	query2 = query[1]
	result = []
	if query1 not in ivdict or query2 not in ivdict:	
		print("No query resuts available, Please rebuild your query")
		return
	else:
		i=0 
		j=0
		query1_list = ivdict[query1]
		query2_list = ivdict[query2]
		query1_list.sort()
		query2_list.sort()
		while i<(len(query1_list)) and j<(len(query2_list)):
			a = query1_list[i][0]
			b = query2_list[j][0]
			if a == b:
				result.append(a)
				i+=1
				j+=1
			else: 
				if a > b:
					j+=1
				else:
					i+=1
#	print("The search results for AND Boolean query:::",result)
	return result


ivdict = {}
for filename in files:
	text = readfile(path, filename)
	text = preprocess(text) 
	inverted_index(text, filename)

#print(ivdict)
query = input("Enter your query")
print(search(query))	

