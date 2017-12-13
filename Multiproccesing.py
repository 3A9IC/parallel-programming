# получение текста из инета и
# распечатывание всех существительных
#from queue import Queue, Empty
#from threading import Thread
from multiprocessing import Process, freeze_support, Queue
from bs4 import BeautifulSoup as BS
from requests import get
from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT
from time import time, sleep
#tic = time()
ma = MA()
st = PST()
wt = WPT()

try:
	my_file = open("some.txt", "r", encoding='utf-8')
	text = my_file.read()
except FileNotFoundError:
	text = BS(get("http://lib.ru/KRAPIWIN/airplane.txt").content,"html.parser", fromEncoding="Windows-1251").text
	my_file = open("some.txt", "w", encoding="utf-8")
	my_file.write(text)


Names = {"Man": {}, "female":{}}






text_=st.sentences_from_text(text)
lenS=len(text_)


def sentence_paral(q,q2):
	_Kx = q2.get()
	for k in _Kx:
		xNames = text_[k]
		for word in wt.tokenize(xNames):
			for p in ma.parse(word):
				if "Name" in p.tag and p.score>=0.4:
					if "masc" in p.tag:
						if Names["Man"].get(p.normal_form) is None:
							Names["Man"].update({p.normal_form:1})
						else:
							Names["Man"][p.normal_form]+=1
					if "femn" in p.tag:
						if Names["female"].get(p.normal_form) is None:
							Names["female"].update({p.normal_form:1})
						else:
							Names["female"][p.normal_form]+=1
	q.put(Names)


N = 4
d = int(lenS/N)
lenS2 = d*N
n,m = 0,d
if lenS2!=lenS:
	m+=1
	lenS2+=1
t1 = []
t2 = []
for i in range(N):
	h = Queue()
	h2 = Queue()
	test=range(n,m)
	h2.put(test)
	t1+=[h]
	t2+=[h2]
	if lenS2!=lenS:
		n=m
		m+=d+1
		lenS2+=1
	else:
		n=m
		m+=d
G =[]
if __name__ == '__main__':
	freeze_support()
	for f in range(N):
		g=Process(target=sentence_paral, args= (t1[f],t2[f]))
		g.start()
		G+=[g]
	for pe in G:
		pe.join()
	
	Names = t1[0].get()
	
	if N != 1:
		for t in t1[1:]:
			temp = {}
			temp = t.get()
			for word in temp["Man"]:
				try:
					if Names["Man"][word] is not None:
						Names["Man"][word]+=temp["Man"][word]
				except KeyError:
					Names["Man"].update({word:1})
			for word in temp["female"]:
				try:
					if Names["female"][word] is not None:
						Names["female"][word]+=temp["female"][word]
				except KeyError:
					Names["female"].update({word:1})			
	maxM=0
	maxF=0

	for word in Names["Man"]:
		if Names["Man"][word]>maxM:
			maxM=Names["Man"][word]
			B=word	
	for word in Names["female"]:
		if Names["female"][word]>maxF:
			maxF=Names["female"][word]
			A=word
				
	print(Names)

	print(B," и ", A)
	#toc = time()
	#print(toc-tic)
			

