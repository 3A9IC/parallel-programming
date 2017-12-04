from queue import Queue, Empty # импортируем библиотеку очереди
from threading import Thread # ипортируем библиотеку для многопоточного программирования
from bs4 import BeautifulSoup as BS #Библиотека для парсинга страницы 
from requests import get   #импортируем метод get для запросов
from pymorphy2 import MorphAnalyzer as MA #морфологический анализатор для русского языка
from nltk.tokenize import PunktSentenceTokenizer as PST  #Класс для выделения предложений
from nltk.tokenize import WordPunctTokenizer as WPT      #класс для разделения слов в предложении

ma = MA()       #обозначение переменных как класс
st = PST()	#обозначение переменных как класс
wt = WPT()	#обозначение переменных как класс

Names = {"Man": {}, "female":{}} #создаем словарь Names с двумя вложенными, пустыми словарями Man и female

q = Queue() # создаем переменную q типа очередь

try:  #попытаться
	my_file = open("some.txt", "r", encoding='utf-8')   #открыть файл с именем some.txt с кодировкой utf-8 на чтение
	text = my_file.read()	#в переменную text запоминаем все данные из этого файла
except FileNotFoundError:	#если файл не найден отрабатываем исключение
	text = BS(get("http://lib.ru/KRAPIWIN/airplane.txt").content, fromEncoding="windows-1251").text	# парсим страницу
	# и заносим в переменную text
	my_file = open("some.txt", "w", encoding='utf-8')	#создаем файл на запись с кодировкой utf-8	
	my_file.write(text)	#записываем в файл данные, которые спарсили
	
text_=st.sentences_from_text(text) # заносим в переменную text_ список разбитый по предложениям
lenS=len(text_) # заносим в переменную lenS количество предложений из text_

def sentence_paral(): #функция
	_Kx = q.get() # Достаем данные из очереди
	for k in _Kx: # бежим по этим данным
		xNames = text_[k] # в xNames заносим предложение k
		for word in wt.tokenize(xNames): #бежим по словам в этом предложении
			for p in ma.parse(word): #морфологический разбор слова
				if "Name" in p.tag and p.score>=0.4:#если мы считаем, что вероятность больше 0.4 и слово = имя
									# то мы считаем это слово именем
					if "masc" in p.tag: #если имя мужское
						if Names["Man"].get(p.normal_form) is None:# ищем в нормальной форме мужское имя
												# в словаре Man, если его нет
							Names["Man"].update({p.normal_form:1})#то добавляем его в словарь Man со значением 1
						else:#иначе
							Names["Man"][p.normal_form]+=1#инкрементируем значение
					if "femn" in p.tag:#если имя женское
						if Names["female"].get(p.normal_form) is None:# ищем в нормальной форме женское имя
												# в словаре female, если его нет
							Names["female"].update({p.normal_form:1})#то добавляем его в словарь
													#female со значением 1
						else:#иначе
							Names["female"][p.normal_form]+=1#инкрементируем значение
N = 4 # задаем количество процессов
d = int(lenS/N) # считаем количество предложений разбитых равно на 4 процесса 
n,m = 0,d # создаем промежутки из этих предложений
T = [] # пустой список

for f in range(0,N): #цикл по N
	test=range(n,m) # заносим в test промежуток из значеий от n до m
	q.put(test) # заносим значения из test в очередь q
	t = Thread(target = sentence_paral) #выбираем цель threding'a - функцию
	t.start() # запускаем метод start()
	n+=d # увеличиваем промежутки
	m+=d # увеличиваем промежутки
	T+=[t] # заносим в список t

for t in T:
	t.join() # вызываем метод join

maxM=0 # в maxM присваиваем 0
maxF=0 # в maxF присваиваем 0

for word in Names["Man"]: # бежим по словам из мужского словарика
	if Names["Man"][word]>maxM: # если количество вхождение этого слова больше maxM
		maxM=Names["Man"][word] # присваиваем в maxM это количество
		B=word	# записываем в В это имя
for word in Names["female"]: # бежим по словам из женского словарика
	if Names["female"][word]>maxF: # если количество вхождение этого слова больше maxF
		maxF=Names["female"][word] # присваиваем в maxF это количество
		A=word # записываем в A это имя
#print(Names)

print(B," и ", A) # Вывод имен
