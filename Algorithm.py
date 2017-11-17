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

for sentence in st.sentences_from_text(text):
	for word in wt.tokenize(sentence):
		for p in ma.parse(word):
			#print(p, p.tag.grammemes)
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
			
print(Names)	#выводим данные из Словаря
