# MiniProject on Webscraping
  This project is aimed to provide parallel phone products, their images, hyperlinks and their prices from both amazon and flipkart by webscraping the 2 websites. 

# Installations required to run this project:
  1. requests
  2. flask
  3. oauthlib
  4. pyOpenSSL
  5. Flask-Login
  6. rauth
  7. WTForms
  8. Flask-WTF
  9. urllib3
  10. newsapi-python

# Sample steps to run this project:
  1. Run app.py in flaskstuff
  2. Go to your terminal and click on https://127.0.0.1:5000/ 
  3. It will lead you on your browser
  4. It might give a "Potential Security Risk". But click Advanced > Accept Risk and continue. (This is because of the un-certificated login database that we have added)
  5. Login using google. It will lead to the Home page
  6. Type "iphone" and enter
  7. It should give you 10 results from both flipkart and amazon
  8. Apply filters and enjoy.

# Other Info
  - Templates sub-folder has all the html pages
  - Static sub-folder has all the CSS files and images
  - app.py is the main flask file
  - BS4Azn.py is the amazon web scraper
  - BS4fpkrt.py is the flipkart web scraper
