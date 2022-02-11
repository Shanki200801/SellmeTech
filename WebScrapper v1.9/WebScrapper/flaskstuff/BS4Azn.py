from bs4 import BeautifulSoup
import requests
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

import Getlink

from urllib.error import HTTPError
def amzLists(search_string,max):   
    products=[]
    prices=[]
    links=[]
    images=[]
    #print(Getlink.get_amz_url(search_string))
    source=requests.get(Getlink.get_amz_url(search_string),headers=headers)
    source=source.content
    #print(source)
    soup = BeautifulSoup(source,'lxml')
    search_results= soup.find('div',{'class':'s-main-slot'})
    result_row=soup.find_all('div',
    {'class':"s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"},
    {'data-component-id'})
    for i in range(0,max):
        if not result_row[i]['data-asin']:
            continue
        else:
            products.append(result_row[i].find('span',{"class":"a-size-medium a-color-base a-text-normal"}).text)
            prices.append(result_row[i].find('span', {'class': 'a-price-whole'}).text)
            links.append('https://www.amazon.in'+result_row[i].find('a',{'class':'a-link-normal'},{'target':'_blank'})['href'])
            images.append(result_row[i].find('img',{'class':'s-image'})['src'])
            combinedlist=[products,prices,links,images]
    return combinedlist

if __name__=="__main__":
    listOlist=amzLists("Iphone")
    print(listOlist[0][0])