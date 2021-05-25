#from simplified_scrapy import SimplifiedDoc,req,utils
from bs4 import BeautifulSoup
import requests
from googlesearch import search

class Backend:
  def __init__(self):
    self.results = list()
    self.Phrase = str()
  
  def Search(self, Phrase):
    self.Phrase = Phrase
    

    for j in search(self.Phrase):
      self.results.append(j)
    
    self.results = list(set(self.results))     #Removing the duplicate values from the list
  
  def Print_Search(self):
    for j in self.results:
      print(j)

  def Process(self):
    #this function must process all the information and return a binary answer.
    #make a file in python that documents the frequency of the number of times a website appears in the searches. later in practice the websites needs to be given a greater preference if it has appeared multiple times.
    #webscrap the webpages here
    
    URL = self.results[1]
    
    #URL = "https://www.geeksforgeeks.org/data-structures/"
    r = requests.get(URL)
    #print(r.content)

    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    print(soup.prettify())

    

obj = Backend()
inp = str(input("Type in Headline... "))
obj.Search(inp)
obj.Print_Search()
obj.Process()