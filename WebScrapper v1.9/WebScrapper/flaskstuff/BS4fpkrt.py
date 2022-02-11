from types import TracebackType
from bs4 import BeautifulSoup
import requests
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}

import Getlink
def getNewlists(search_string,max):
    products=[]
    prices=[]
    links=[]
    images=[]
    source=requests.get(Getlink.get_flpkrt_url(search_string),headers=headers).content
    soup = BeautifulSoup(source,'lxml')
    search_results= soup.find_all('div',{'class':'_13oc-S'})
    i=1
    count=0
    while count<max:
        products.append(search_results[i].find('div',{'class':'_4rR01T'}).text)
        prices.append(search_results[i].find('div',{'class':'_30jeq3 _1_WHN1'}).text)
        images.append(search_results[i].find('img',{'class':'_396cs4 _3exPp9'})['src'])
        links.append('https://www.flipkart.com'+search_results[i].find('a',{'class':'_1fQZEK'})['href'])
        i+=1
        count+=1
    lists = [products, prices,links,images]
    return lists
if __name__=="__main__":
    listOlist=getNewlists("Iphone",4)
    print(listOlist[0][0])