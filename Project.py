from itertools import count
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import requests
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

class Backend:
    def __init__(self):
        self.__results = list()
        self.__Phrase = str()
        self.__matrix_list = list()
        self.__sentences = list()
        self.__corpus = str()
        self.__corpus_list = list()
        self.__score = 0                     #score
        self.__SentenceList = list()         #list of list of sentences of the individual corpuses
        self.Answer = bool()                 #true or fake news
        self.testing = list()
  
    def Search(self, Phrase):
        self.__Phrase = Phrase
        for j in search(self.__Phrase):
            self.__results.append(j)
            self.__results = list(set(self.__results))     #Removing the duplicate values from the list
  
    def Print_Search(self):
        for j in self.__results:
            print(j)

    def Clear_Score(self):
        self.__score = 0
        self.Answer = 0

    def Process(self):
        self.Clear_Score()
        for i in range(len(self.__results)):
            URL = self.__results[i]
            try:
                r = requests.get(URL) 
                soup = BeautifulSoup(r.content, 'html.parser') 
                self.__corpus = str(soup.get_text())   #collecting textual data from websites
                self.__corpus = " ".join(self.__corpus.split())
                self.__corpus_list.append(self.__corpus)
            except:
                continue
    
        word = nltk.word_tokenize(self.__Phrase)
        for i in range(len(self.__corpus_list)):
            self.__split_into_sentences(self.__corpus_list[i],1)                                    #splitting into sentences
            self.__SentenceList.append(self.__sentences)
            self.__checking(self.__sentences,word)

        if (self.__score > int((len(self.__SentenceList)/5))):
            return 1
           
        #Text Cleaning
        nltk.download('punkt')
        nltk.download('wordnet')
        stop_words = stopwords.words('english')
        lemmatizer=WordNetLemmatizer()
        filter_sentence = ''
        tfidf = TfidfTransformer(norm="l2")
        count_vectorizer = CountVectorizer()

        for i in range(len(self.__corpus_list)):
            self.__corpus_list[i] = nltk.word_tokenize(self.__corpus_list[i])      #Tokenisation
            self.__corpus_list[i] = [w for w in self.__corpus_list[i] if not w in stop_words]        #removal of stopwords

            for word in self.__corpus_list[i]:
                filter_sentence = filter_sentence + ' ' + str(lemmatizer.lemmatize(word)).lower()      #lemmatization
        #NLP Techniques
            count_vectorizer.fit_transform(self.__corpus_list[i])     
            self.__matrix_list.append(count_vectorizer.transform(self.__corpus_list[i]))
            tfidf.fit(self.__matrix_list[i])
            self.__matrix_list[i] = tfidf.transform(self.__matrix_list[i])



    def __split_into_sentences(self,text,choice=1):
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        self.__sentences = [s.strip() for s in sentences]

        if choice == 1:
            self.__remove_sentence_punctuation(self.__sentences)
        else:
            pass 

    def __checking(self,sentence,words):
        res = [all([k in s for k in words]) for s in sentence] 
        if len([sentence[i] for i in range(0, len(res)) if res[i]]) >= 1:
            self.__score = self.__score + 1
        return [sentence[i] for i in range(0, len(res)) if res[i]]

    def __remove_sentence_punctuation(self, sentences):
        j = 0
        self.__sentences = sentences
        for i in self.__sentences:
            self.__sentences[j] = re.sub(r'[^\w\s]','',i)
            j = j + 1

obj = Backend()
inp = str(input("Type in Headline... "))
obj.Search(inp)
if obj.Process() == 1:
    print("\nTrue News")
else:
    print("\nFake News")