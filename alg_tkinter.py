# получение текста из инета и
# распечатывание всех существительных
from queue import Queue, Empty
from tkinter import *
from bs4 import BeautifulSoup as BS
from requests import get
from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT
from time import time, sleep

root = Tk()	#обозначаем переменную root как класс tkinter
ma = MA()
st = PST()
wt = WPT()

try:
	my_file = open("some.txt", "r", encoding='utf-8')
	text = my_file.read()
except FileNotFoundError:
	text = BS(get("http://lib.ru/KRAPIWIN/airplane.txt").content, fromEncoding="windows-1251").text
	my_file = open("some.txt", "w", encoding='utf-8')
	my_file.write(text)


Names = {"Man": {}, "female":{}}





q = Queue()



text_=st.sentences_from_text(text)
lenS=len(text_)


def sentence_paral():
	_Kx = q.get()
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

N = 4
d = int(lenS/N)
n,m = 0,d


for f in range(N):
	test=range(n,m)
	q.put(test)
	root.after(1,sentence_paral)	#запустить sentence_paral через 1 милисекунду
	n+=d
	m+=d


root.mainloop()		#используем функцию mainloop для создания окна




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
