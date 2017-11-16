"""
В некотором тексте найти все мужские и женские имена.
Определить самые популярные.
Озаглавить текст как "А и Б", где А и Б - мужское и женское имя соответственно.
"""

from bs4 import BeautifulSoup as BS  #Библиотека для парсинга страницы         
from requests import get   #Библиотека позволяет отправлять HTTP-запросы
from pymorphy2 import MorphAnalyzer as MA #морфологический анализатор для русского языка
from nltk.tokenize import PunktSentenceTokenizer as PST  #узнаем параметры из данного текста.
from nltk.tokenize import WordPunctTokenizer as WPT      #импорт маркировки

ma = MA()       #обозначение переменных как класс
st = PST()	#обозначение переменных как класс
wt = WPT()	#обозначение переменных как класс


try:  #попытаться
	my_file = open("some.txt", "r", encoding='utf-8')   #открвть вайс с именем some.txt с кодировкой utf-8 на чтение
	text = my_file.read()	#в переменную text запоминаем все данные из этого файла
except FileNotFoundError:	#если файл не найден отрабатываем исключение
	text = BS(get("http://lib.ru/KRAPIWIN/airplane.txt").content, fromEncoding="windows-1251").text	# парсим страницу
	# и заносим в переменную text
	my_file = open("some.txt", "w", encoding='utf-8')	#создаем файл на запись с кодировкой utf-8	
	my_file.write(text)	#записываем в файл данные которые спарсили(на строке 22)


			
print(text)	#выводим данные из переменной text
