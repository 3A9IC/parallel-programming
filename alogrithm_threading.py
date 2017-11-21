from queue import Queue, Empty
from threading import Thread
from bs4 import BeautifulSoup as BS
from requests import get
from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT

ma = MA()
st = PST()
wt = WPT()

Names = {"Man": {}, "female":{}}

q = Queue()

try:
	my_file = open("some.txt", "r", encoding='utf-8')
	text = my_file.read()
except FileNotFoundError:
	text = BS(get("http://lib.ru/KRAPIWIN/airplane.txt").content, fromEncoding="windows-1251").text
	my_file = open("some.txt", "w", encoding='utf-8')
	my_file.write(text)
lenS=len(st.sentences_from_text(text))

text_=st.sentences_from_text(text)
Kx= list(text_)


def sentence_paral():
  pass #!!!!!!!!!!!!!!!!!!!!!!! Написать функцию для решения задачи!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
F = [sentence_paral, sentence_paral,sentence_paral,sentence_paral]
d = int(lenS/len(F))
n,m = 0,d
T = []

for f in F:
	test=range(n,m)
	q.put(test)
	t = Thread(target = f)
	t.start()
	n+=d
	m+=d
	T+=[t]

for t in T:
	t.join()

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
#print(Names)

print(B," и ", A)
