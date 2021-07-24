from tkinter.constants import END
from bs4 import BeautifulSoup
import math
import tkinter as tk
from threading import *
import requests
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
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
        self.__sentences = list()
        self.__corpus = str()
        self.__corpus_list = list()
        self.__score = 0                     #score
        self.__SentenceList = list()         #list of list of sentences of the individual corpuses
        self.Answer = bool()                 #true or fake news
        self.testing = list()
        self.__score_matrix = list()
        self.__elim = list()
  
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
                self.__corpus = str(soup.get_text())                                            #collecting textual data from websites
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

        for i in range(len(self.__corpus_list)):                                                 #removal of punctuation and blocked URLs
            self.__corpus_list[i] = self.__punctuation_REM(self.__corpus_list[i])
            if len(str(self.__corpus_list[i])) <= 25:
                self.__elim.append(i)
        
        for i in self.__elim:
            self.__corpus_list.remove(self.__corpus_list[i])

        length = int(math.ceil(len(self.__corpus_list)/2))
        temporary_matrix = list()
        
        for i in range(length):
            for j in range(length):
                if i != j:
                    temporary_matrix.append(self.__cosine_sim(self.__corpus_list[i],self.__corpus_list[j]))
                else:
                    continue
            self.__score_matrix.append(temporary_matrix)
            temporary_matrix = []  

        __avg = 0
        for i in range(length):
            for j in range(length-1):
                __avg = __avg + self.__score_matrix[i][j]
        __avg = float(__avg/(length*(length-1)))*100
        print(__avg)
        if int(__avg*1000) < 98250:
            return 0
        else:
            return 1
        
    def __cosine_sim(self,text1, text2):
        vectorizer = TfidfVectorizer(tokenizer=self.__normalise)
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]
    
    def __normalise(self,corpus):
        stop_words = stopwords.words('english')
        corpus = self.__Lemmatize(nltk.word_tokenize(corpus))
        return [w for w in corpus if not w in stop_words]  

    def __Lemmatize(self,words):
        lemmatizer=WordNetLemmatizer()
        filter_sentence = ''
        for word in words:
            filter_sentence = filter_sentence + ' ' + str(lemmatizer.lemmatize(word)).lower()
        return filter_sentence

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

    def __punctuation_REM(self,corpus):
        corpus = re.sub(r'[^\w\s]',' ',corpus)
        corpus = re.sub(r'[\s\s+]' , ' ', corpus)
        return corpus

News = ''
def clr():
    global News
    News = ''
    text_entry.delete("1.0","end")
    Ans.config(text=News)
    state_window.config(text = '', bg='white')

def threading():
    # Call work function
    Thread1=Thread(target=result)
    Thread1.start()

def result():
    global News
    phrase = text_entry.get('1.0',END)
    print('Processing')
    state_window.config(text = 'Processing', bg = 'tomato')
    obj = Backend()
    obj.Search(phrase)
    if obj.Process() == 1:
        News = 'True News'
    else:
        News = 'False News'
    print('processed')
    Ans.config(text = News)
    state_window.config(text = 'Processed',bg = 'green')

window = tk.Tk()

#gui.iconbitmap(r'commitment.ico')

window.title('Fake News Zapper')
window.geometry("800x700")
window.state("zoomed")
window.iconbitmap(r'thunder.ico')

lbl1=tk.Label(window, text ='Fake News Detection', fg='Black', font=("Helvetica",20))
lbl1.place(relx=0.4,rely=0.05) 

lbl2 = tk.Label(window, text = 'Type In Headline', fg='green',font=("Helvetica",16))
lbl2.place(relx=0.25,rely=0.10, relwidth=0.5, relheight=0.1) 

lbl3 = tk.Label(window, text = 'Text', fg='green',font=("Helvetica",12))
lbl3.place(relx=0.25,rely=0.17, relwidth=0.5, relheight=0.05) 

text_entry = tk.Text(window, width=155, bg = 'coral')
text_entry.place(relx=0.05,rely=0.22, relheight=0.2)

lbl = tk.Label(window, text = 'Status', fg='green',font=("Helvetica",12))
lbl.place(relx=0.45,rely=0.45, relwidth=0.05, relheight=0.05)

state_window = tk.Label(window, text = News , width=30,  bg = 'white')
state_window.place(relx=0.52,rely=0.45, relheight=0.05)

button1 = tk.Button(window, text = "Submit", width = 25,  fg='red', font=("Helvetica",12), command = threading) 
button1.place(relx=0.325,rely=0.52)

button2 = tk.Button(window, text = "Clear", width = 25,  fg='red', font=("Helvetica",12), command = clr) 
button2.place(relx=0.52,rely=0.52)

lbl4 = tk.Label(window, text = 'The News is: ', width = 25, fg='green', font=("Helvetica",12))
lbl4.place(relx=0.42,rely=0.6)

Ans = tk.Label(window, text = News , width=50,  bg = 'coral')
Ans.place(relx=0.37,rely=0.65, relheight=0.05)

button2 = tk.Button(window, text = "Click & Quit", width = 25,  fg='red', font=("Helvetica",12),command = window.destroy )
button2.place(relx=0.42,rely=0.75)

lbl6 = tk.Label(window, text = 'Fake News Zapper', width = 100, fg='grey', font=("Helvetica",8))
lbl6.place(relx=0.28,rely=0.9)

lbl7 = tk.Label(window, text = 'Developed by Sujoy Das, Shivam Gupta, Prastuti Koch', width = 100, fg='grey', font=("Helvetica",8))
lbl7.place(relx=0.28,rely=0.93)

window.mainloop()