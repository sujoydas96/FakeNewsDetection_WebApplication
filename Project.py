class Backend:
  def __init__(self):
    self.results = list()

  def Query_Input(self, Phrase):
    self.Phrase = Phrase
  
  def Search(self):
    from googlesearch import search

    for j in search(self.Phrase, tld="co.in", num=5, stop=20, pause=2):
      self.results.append(j)
    for j in search(self.Phrase, tld="com", num=20, stop=20, pause=2):
      self.results.append(j)
    
    self.results = list(set(self.results))     #Removing the duplicate values from the list
  
  def Print_Search(self):
    print(self.results)

  def Process(self):
    #this function must process all the information and return a binary answer.
    #make a file in python that documents the frequency of the number of times a website appears in the searches. later in practice the websites needs to be given a greater preference if it has appeared multiple times.
    #webscrap the webpages here
    pass

obj = Backend()
inp = str(input("Type in Headline..."))
obj.Query_Input(inp)
obj.Search()
obj.Print_Search()