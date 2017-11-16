"""
В некотором тексте найти все мужские и женские имена.
Определить самые популярные.
Озаглавить текст как "А и Б", где А и Б - мужское и женское имя соответственно.
"""

from bs4 import BeautifulSoup as BS
from requests import get
from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT

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


			
print(text)
