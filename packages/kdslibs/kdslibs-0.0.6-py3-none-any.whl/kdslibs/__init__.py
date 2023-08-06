import urllib.request
link = "https://raw.githubusercontent.com/akdiwahar/dataset/main/print1"
    
def printall():
  
  print(readData())

def printhead(dataSearch):
  strs=readData().split("###ENDOFSEGMENT###")
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
    
def readData():
  with urllib.request.urlopen(link) as url:
      s = url.read()
      # I'm guessing this would output the html source code ?
      return s.decode()
