# -*- coding: utf-8 -*-

import sys
import time
import feedparser
import nltk
import coding
import numpy as np
import nltk
import string
from nltk.corpus import stopwords


#coding.setup_console("utf8")

if __name__ == "__main__":
    start_time = time.time()

    if len(sys.argv) >= 1:
        print "Старт " + str(start_time)
       #app = locomotive.app.Application()
       # ... дополнительная логика  ...

#print feedparser.parse("http://feeds.nytimes.com/nyt/rss/Technology")
#print nltk.corpus.stopwords.words('russian')
#print nltk.download()

def read_data_file(file_name="data.csv"):
    # Загружаем файл с кодировкай utf8
    text = open(file_name,'r').read()
    # Декодируем из utf8 в unicode - из внешней в рабочую
    text = text.decode('cp1251')
    # Работаем с текстом
    return  text

def save_result_file(file_name="data.csv", text=""):
    # Кодируем тест из unicode в utf8 - из рабочей во внешнюю
    text = text.encode('utf8')
    # Сохраняем в файл с кодировкий utf8
    open("new_" + file_name,'w').write(text)

def tokenize_me(file_text):
    #firstly let's apply nltk tokenization
    tokens = nltk.word_tokenize(file_text)

    #let's delete punctuation symbols
    tokens = [i for i in tokens if ( i not in string.punctuation )]

    #deleting stop_words
    stop_words = stopwords.words('russian')
    stop_words.extend([u'что', u'это', u'так', u'вот', u'быть', u'как', u'в', u'—', u'к', u'на'])
    tokens = [i for i in tokens if ( i not in stop_words )]

    #cleaning words
    tokens = [i.replace(u"«", "").replace(u"»", "") for i in tokens]

    return tokens

text = read_data_file("data1.csv")

#s = text.rstrip(";")
print text
#d = np.array(text)

#d = ['Тест','списка']
tokens = tokenize_me(text)
#print ','.join(d)
print ','.join(tokens)

save_result_file("data1.csv",'\n'.join(tokens))
