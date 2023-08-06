from collections import Counter
import urllib

def count_in_list(l, word):
    c = Counter(l)
    return c[word]
    
    
def printlibs():
 link = "https://raw.githubusercontent.com/akdiwahar/dataset/main/print1"
 f = urllib.urlopen(link)
 myfile = f.read()
 print(myfile)
    

