
from worldnews import worldNews 

agency1 = 'reuters'
agency2 = 'olhardigital'
agency3 =  'theguardian' 

news = worldNews()
news.set_agencies(agency1, agency2, agency3)
news.search_news_agencies('good')



