# import libraries
import nltk
import re
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd
import urllib
from bs4 import BeautifulSoup
import tamil
#class 4 english text load and clean
with open("input.txt","r", encoding='utf8') as f:
    file_data = f.read()
f.close()

#load dictionary
with open("words.txt","r", encoding='utf8') as d:
    allWords = d.read()
d.close()
#remove everything except alphabets
file_data = re.sub("[^a-zA-Z ]+", "", file_data)
#convert all words to lowercase
file_data=file_data.lower()
#split the sentences to individual words
splitted=file_data.split()
#remove stop words
filtered_words = [w for w in splitted if not w in stopwords.words('english')]
#remove words not present in dictionary
filtered_words = [w for w in filtered_words if w in allWords]
#count the frequency of words
counts = Counter(filtered_words)
#put the counted frequency in the DataFrame and rename , then sort , save the DataFrame
df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
df = df.rename(columns={'index':'word', 0:'count'})
onlyFrequency04Eng = df.sort_values('count', ascending=False)
onlyFrequency04Eng.to_csv('onlyFrequency04Eng.csv', index=False)
fullList=onlyFrequency04Eng.head(n=5000).reset_index()
#get the synonyms from the internet
relevantList=[]
allSynonyms=[]
records=[]
i=len(df.index)+1
for index, row in fullList.iterrows():
    try:
        url = "http://www.thesaurus.com/browse/"+row['word']+"?s=t"
        content=urllib.request.urlopen(url)
        soup = BeautifulSoup(content, "lxml")
        relevantList=soup.find("div",{"class":"relevancy-list"}).find_all("li")
        for elem in relevantList:
            records.append(elem.find("span",{"class":"text"}).text.strip())
        allSynonyms.append(records)
        records=[]
    except:
        allSynonyms.append(records)
        records=[]
    print(i)
    i=i-1
fullList.loc[:,'Synonyms']=pd.Series(allSynonyms)
#get tamil meaning
allTamil=[]
for index, row in fullList.iterrows():
    words=row['word']
    try:
        url = "http://www.tamildict.com/english.php?action=search&sID=4b4ecb3fd478e8b0d9fbfb4f5137db1b%2F&word="+words
        content=urllib.request.urlopen(url)
        soup = BeautifulSoup(content, "lxml")
        relevantList=soup.find("table",{"class":"eigene_tabelle"})
        data = []
        tamilWords=[]
        table = soup.find('table', attrs={'class':'eigene_tabelle'})
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        for elem in data:
            for inelem in elem:
                if words in inelem:
                    if len(words) == len(inelem):
                        tamilWords.append(elem[1])
        allTamil.append(tamilWords)
    except:
        allTamil.append(tamilWords)
        tamilWords=[]
    
    print(i)
    i=i+1    

fullList.loc[:,'tamilTrans']=pd.Series(allTamil)


fullList.to_csv('output_math_07.csv', index=False, encoding='utf-8-sig')