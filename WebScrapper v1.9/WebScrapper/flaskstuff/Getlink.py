def get_amz_url(keyword):
    keyword=str(keyword).split()
    amazon_url='https://www.amazon.in/s?k='
    for item in keyword:
        amazon_url += item+'+'
    amazon_url = amazon_url[:-1]
    return amazon_url
def get_flpkrt_url(keyword):
    keyword=str(keyword).split()
    flipkart_url='https://www.flipkart.com/search?q='
    for item in keyword:
        flipkart_url += item+'%20'
    flipkart_url = flipkart_url[:-3]
    return flipkart_url
def main():
    print(get_amz_url('I phone'))
    print(get_flpkrt_url('I phone'))

if __name__=='__main__':
    main()
