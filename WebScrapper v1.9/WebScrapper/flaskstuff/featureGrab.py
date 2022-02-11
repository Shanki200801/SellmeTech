from bs4 import BeautifulSoup
import requests
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
def getAmzFeatures(amzlink):
    sourceA=requests.get(amzlink,headers=headers).content  
    soupA = BeautifulSoup(sourceA,'lxml')
    featuresA=[]
    data1=soupA.find('ul',{'class':"a-unordered-list a-vertical a-spacing-mini"})
    for li in data1.find_all("li"):
        featuresA.append(li.text)
       
    return featuresA
    
def getFpkFeatures(Fpklink):
    sourceF=requests.get(Fpklink,headers=headers).content  
    soupF = BeautifulSoup(sourceF,'lxml')
    featuresF=[]
    data2=soupF.find('div',{'class':"_2418kt"})
    for li in data2.find_all("li"):
        featuresF.append(li.text)
     
    return featuresF

if(__name__=="__main__"):
    print(getAmzFeatures("https://www.amazon.in/Apple-iPhone-13-128GB-Pink/dp/B09G9FPGTN/ref=sr_1_3?crid=17TCB2EF5AJLU&keywords=iphone+13&qid=1642432247&sprefix=iph%2Caps%2C276&sr=8-3"))
    print(getFpkFeatures("https://www.flipkart.com/apple-iphone-13-pro-max-gold-1-tb/p/itmdbbad9da2b178?pid=MOBG6VF5GHTNXG9K&lid=LSTMOBG6VF5GHTNXG9KQLRPNA&marketplace=FLIPKART&q=i+phone+13+pro+max&store=tyy%2F4io&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&fm=SEARCH&iid=1bfd2ec4-bcbc-40ce-8050-a4d1b5234afe.MOBG6VF5GHTNXG9K.SEARCH&ppt=sp&ppn=sp&ssid=zumlaynzps0000001642434327507&qH=db0b1e3384f9c46c"))