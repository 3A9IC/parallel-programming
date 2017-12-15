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


Names = {"Man": {}, "female":{}} # будем использовать этот словарь для работы параллельных процессов и для сбора результатов выполнения этих процессов






text_=st.sentences_from_text(text)
lenS=len(text_)


def sentence_paral(q,q2): # определяем функцию с двумя аргументами - очередями 
	_Kx = q2.get() # вытаскиваем список первого и последнего предложения, используемые для данного процесса, из q2
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
	q.put(Names) # кладем в очередь q получившийся словарь


N = 4 # задаем количество процессов
d = int(lenS/N)
lenS2 = d*N # создаем переменную что бы определить количество предложений, невошедших в распораллеливаемые процессы
n,m = 0,d
if lenS2!=lenS: # если все предложения не равны с lenS2
	m+=1 # увеличиваем конечную границу для процесса
	lenS2+=1 # увеличиваем переменную lenS2
t1 = [] # создаем пустой список t1
t2 = [] # создаем пустой список t2
for i in range(N): # бежим по всем процессам
	h = Queue() # создаем переменную h типа очередь
	h2 = Queue() # создаем переменную h типа очередь
	test=range(n,m)
	h2.put(test) # кладем в очередь h2 список test
	t1+=[h] # кладем в 1 список очередь h
	t2+=[h2] # кладем в 2 список очередь h2
	if lenS2!=lenS: # если все предложения не равны с lenS2
		n=m # присваиваем начальной границе конечную
		m+=d+1 # увеличиваем конечную границу на d+1
		lenS2+=1 # увеличиваем количество используемых предложений
	else: # в противном случае
		n=m # присваиваем начальной границе конечную
		m+=d # увеличиваем конечную границу на d
G =[] # создаем пустой список 
if __name__ == '__main__': # используем это условие для работы с параллельными процессами на винде
	freeze_support() # проверка того, должен ли исполняемый процесс запускать код, полученный по каналу, или нет.
	for f in range(N):
		g=Process(target=sentence_paral, args= (t1[f],t2[f])) # создаем процесс с целью функцией sentence_paral и аргументами - очередями
		g.start() # старт процесса
		G+=[g] # процессы в список
	for pe in G: # запускаем все процессы
		pe.join() # вызываем метод join
	
	Names = t1[0].get() # достаем словарь из первой очереди
	
	if N != 1: # если у нас больше одного процесса
		for t in t1[1:]: # бежим по оставшимся очередям
			temp = {} # создаем пустой словарь
			temp = t.get() # заносим в него текущий, вытащенный из очереди, словарь
			for word in temp["Man"]: # бежим по мужским именам в этом словаре
				try: # пытаемся
					if Names["Man"][word] is not None: # если имя из temp присутствует в Names
						Names["Man"][word]+=temp["Man"][word] # то увеличиваем количество вхождение этого слова в Names
				except KeyError: # исключаем ошибку доступа ключа(т.е. если у нас в Names нет такого имени из temp)
					Names["Man"].update({word:1}) # заносим это имя со значением 1 в Names
			for word in temp["female"]:# аналогично как с мужскими только для женских имен
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
			

