"""
В некотором тексте найти все мужские и женские имена.
Определить самые популярные.
Озаглавить текст как "А и Б", где А и Б - мужское и женское имя соответственно.
"""

from bs4 import BeautifulSoup as BS  #Библиотека для парсинга страницы         
from requests import get   #импортируем метод get для запросов
from pymorphy2 import MorphAnalyzer as MA #морфологический анализатор для русского языка
from nltk.tokenize import PunktSentenceTokenizer as PST  #Класс для выделения предложений
from nltk.tokenize import WordPunctTokenizer as WPT      #класс для разделения слов в предложении

ma = MA()       #обозначение переменных как класс
st = PST()	#обозначение переменных как класс
wt = WPT()	#обозначение переменных как класс

Names = {"Man": {}, "female":{}} #создаем словарь Names с двумя вложенными, пустыми словарями Man и female

try:  #попытаться
	my_file = open("some.txt", "r", encoding='utf-8')   #открыть файл с именем some.txt с кодировкой utf-8 на чтение
	text = my_file.read()	#в переменную text запоминаем все данные из этого файла
except FileNotFoundError:	#если файл не найден отрабатываем исключение
	text = BS(get("http://lib.ru/KRAPIWIN/airplane.txt").content, fromEncoding="windows-1251").text	# парсим страницу
	# и заносим в переменную text
	my_file = open("some.txt", "w", encoding='utf-8')	#создаем файл на запись с кодировкой utf-8	
	my_file.write(text)	#записываем в файл данные которые спарсили(на строке 22)

for sentence in st.sentences_from_text(text):	#выделяем из текста предложение и бежим по нему
	for word in wt.tokenize(sentence):	#бежим по словам в выделенном тексте
		for p in ma.parse(word):	#морфологический разбор слова
			#print(p, p.tag.grammemes)
			if "Name" in p.tag and p.score>=0.4:	#если мы считаем, что вероятность больше 0.4
				# то мы считаем это слово именем
				if "masc" in p.tag:	#если имя мужское
					if Names["Man"].get(p.normal_form) is None:	# ищем в нормальной форме мужское имя
						# в словаре Man, если его нет
						Names["Man"].update({p.normal_form:1}) #то добавляем его в словарь Man со значением 1
					else:	#иначе
						Names["Man"][p.normal_form]+=1	#инкрементируем значение
				if "femn" in p.tag:	#если имя женское
					if Names["female"].get(p.normal_form) is None:	# ищем в нормальной форме женское имя
						# в словаре female, если его нет
						Names["female"].update({p.normal_form:1}) #то добавляем его в словарь
					#female со значением 1
					else:	#иначе
						Names["female"][p.normal_form]+=1	#инкрементируем значение
			
maxM=0 # Объявляем переменную maxM с значением 0
maxF=0 # Объявляем переменную maxF с значением 0

for word in Names["Man"]: # пробегаем по мужским именам
	if Names["Man"][word]>maxM: # если количество вхождений этого слова > maxM
		maxM=Names["Man"][word] # то к maxM присваиваем это количество
		B=word	# запоминаем в B это слово
for word in Names["female"]: # пробегаем по женским именам
	if Names["female"][word]>maxF: # если количество вхождений этого слова > maxF
		maxF=Names["female"][word] # то к maxF присваиваем это количество
		A=word # запоминаем в A это слово
#print(B," ", maxM, " ", A, " ", maxF)
#print(Names)

print(B," и ", A) # Выводим B и A
