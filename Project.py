class Backend:
  def __init__(self):
    self.results = list()
    self.Phrase = str()
  
  def Search(self, Phrase):
    self.Phrase = Phrase
    from googlesearch import search

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
    pass

obj = Backend()
inp = str(input("Type in Headline... "))
obj.Search(inp)
obj.Print_Search()