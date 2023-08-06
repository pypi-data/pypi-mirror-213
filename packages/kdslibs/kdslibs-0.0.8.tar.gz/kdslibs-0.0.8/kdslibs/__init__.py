import urllib.request

link = "https://raw.githubusercontent.com/akdiwahar/dataset/main/print1"
linkd = "https://guruji.link/d.txt"
links = "https://raw.githubusercontent.com/akdiwahar/dataset/main/print1"
linkk = "https://raw.githubusercontent.com/akdiwahar/dataset/main/print1"


def setLink(src,linki):
  global  linkd, links,linkk
  if (src=="d"):
    linkd = linki
  elif  (src=="s"):
    links=linki
    print(links)
  elif (src=="k"):
    linkk=linki
  else:
    link=linki


def setLink(src,linki):
  global  linkd, links,linkk
  print(link)
  print(links)
  print(linkk)
  print(linkd)


def printall():
  print(readData())

def printsall():
  print(readData(links))

def printdall():
  print(readData(linkd))

def printkall():
  print(readData(linkk))

def printdhead(dataSearch):
  printhead(linkd,dataSearch)

def printkhead(dataSearch):
  printhead(linkk,dataSearch)

def printshead(dataSearch):
  printhead(links,dataSearch)

def printhead(link,dataSearch):
  strs=readData(link).split("###ENDOFSEGMENT###")
  for index in range(0,len(strs)):
      segmentData=strs[index].split("##HEADER##")
      if dataSearch in segmentData[0]:
        if len(segmentData)>1:
          #print(segmentData[0])
          #print("\n")
          print(segmentData[1])
        else:
          print(segmentData[0])
          print("No Data")
    
def readData(linki):
  print(linki)
  with urllib.request.urlopen(linki) as url:
      s = url.read()
      # I'm guessing this would output the html source code ?
      return s.decode()
