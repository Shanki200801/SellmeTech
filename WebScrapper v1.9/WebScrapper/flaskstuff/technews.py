from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='191ca85549494e78b23ae8e4e08f3f1d')



# /v2/top-headlines
def top_articles(page):
    page=int(page)*10
    top_headlines = newsapi.get_top_headlines(#q='bitcoin',
                                            #sources='bbc-news,the-verge',
                                            category='technology',
                                            language='en',
                                            country='in')
    return top_headlines['articles'][page-10:page]

# /v2/everything
# all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       from_param='2022-01-14',
#                                       to='2022-01-25',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=2)

# /v2/top-headlines/sources
#sources = newsapi.get_sources()

if __name__=='__main__':
    top_headlines = top_articles(1)
    #print(sources)
    print(top_headlines)                            # top_headlines['articles'] returns a list of dictionaries
    print(top_headlines[0]['source']['name'])       #returns the source
    print(top_headlines[0]['title'])                #returns the title
    print(top_headlines[0]['description'])          #returns the description
    print(top_headlines[0]['url'])                  #returns the url of the article
    print(top_headlines[0]['urlToImage'])           #returns the image of the url 
    print(top_headlines[0]['content'])              #returns the content of the article 
    pass

