from collections import Counter
import urllib

import urllib.request

def count_in_list(l, word):
    c = Counter(l)
    return c[word]
    
    
def printlibs():
 link = "https://raw.githubusercontent.com/akdiwahar/dataset/main/print1"
 with urllib.request.urlopen(link) as url:
    s = url.read()
    # I'm guessing this would output the html source code ?
    print(s)

    

