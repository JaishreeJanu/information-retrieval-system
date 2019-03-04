# coding: utf-8
import os
import glob
import nltk
import re
#from string import maketrans
# nltk.download('all')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# nltk.download(stopwords)
from nltk.stem import PorterStemmer
#import InvertedIndex
from collections import defaultdict


ivdict = {}

cwd = os.getcwd()
os.chdir('../Data')
cwd = os.getcwd()

#print (os.getcwd())

files = os.listdir(cwd)
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
#stemmedData = ''


def invIndex(term,docID):
	#print("in function::"+term)
	if term in ivdict:
		fg=0
		for i in range(len(ivdict[term])):
			if ivdict[term][i][0] == docID:
				ivdict[term][i][1] += 1
				fg=1
				break;
		if fg == 0:
			ivdict[term].append([docID,1])			
	else:
		myList = [[docID,1]]
		ivdict.update({term : myList }) 
	return

def search():
	query1 = input("Enter query 1: ")
	query2 = input("Enter query 2: ")
	result = []
	if query1 not in ivdict or query2 not in ivdict:	
		print("No query resuts available, Please rebuild your query")
		return
	else:
		i=0 
		j=0
		while i<(len(ivdict[query1])) and j<(len(ivdict[query2])):
			a = ivdict[query1][i][0]
			b = ivdict[query2][j][0]
			if a == b:
				result.append(a)
				i+=1
				j+=1
			else: 
				if a > b:
					j+=1
				else:
					i+=1
	print("The search results for AND Boolean query:::",result)
	return

def preprocess(data):
	stringData = data
	stringData = stringData.lower()
	stringData = re.sub(r'\d+', '', stringData)
	stringData = re.sub(r'[^\w\s]','',stringData)
	tokens = word_tokenize(stringData)
	#print(tokens)
	result = [i for i in tokens if not i in stop_words]
	#print (result)
	for word in result:
		#print("stem this word::"+word)
		invIndex(stemmer.stem(word),doc)
#		stemmedData += (stemmer.stem(word))
#		stemmedData += ' '	
	return


for doc in files:
	with open(doc) as file:
		listData = file.readlines()
		# print (listData)
		stringData = ''.join(map(str, listData))
		preprocess(stringData)

print(ivdict)
search()



	
		






