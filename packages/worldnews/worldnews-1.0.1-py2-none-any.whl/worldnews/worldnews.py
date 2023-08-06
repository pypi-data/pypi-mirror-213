#!/usr/bin/python 
# -*- coding: utf-8 -*-

import requests 
from bs4 import BeautifulSoup

if __name__ == "__main__":
    print "This module should be imported."
    exit()

class worldNews:

    """ here comes the main class """

    def __init__(self):
    
        self.load_urls()
        self.headers = {'Content-Type': 'text/html'}
        self.load_extractors()
        self.load_agencies()
    
    def set_agency(self, agency):

        """ Setting news agency """
        
        self.agency = agency
        self.agency_news = []
        
        country = self.check_agency_name(agency)
        if country != None:
            self.load_news(agency)
        else:
            return None

    def set_agencies(self, agency1='uol', agency2='g1', agency3='r7'):
         
         self.agency1 = agency1 
         self.agency2 = agency2 
         self.agency3 = agency3

         self.agency1_news = []
         self.agency2_news = []
         self.agency3_news = []

         country1 = self.check_agency_name(agency1) 
         country2 = self.check_agency_name(agency2)
         country3 = self.check_agency_name(agency3)

         if country1 and country2 and country3 != None:
            self.load_m_news()
         else:
            return None
 
    def load_agencies(self): 
            
        """ Loading some news agencies """
        
        self.br_agencies = ['uol', 'g1', 'estadao', 'r7',
                            'veja', 'elpais', 'cartacapital', 
                            'cnnbrasil', 'terra', 'ig', 'olhardigital', 
                            'exame', 'ge']

        self.us_agencies = ['skynews', 'cnn', 'nbc', 
                            'cbs, abc, nyt', 'wp', 'foxnews', 'wsj']

        self.uk_agencies = ['bbc','theguardian', 'reuters', 'euronews']  
        self.agencies = {'br':self.br_agencies, 
                         'us':self.us_agencies, 'uk':self.uk_agencies}

    def check_agency_name(self, agency_name):

        """ Checking if agency exists """

        for country in self.agencies:
            if agency_name in self.agencies[country]:
                return country
        return None

    def load_urls(self):

        """ List of available agencies urls """

        self.agency_url = {'uol':'https://www.uol.com.br', 
                            'g1':'https://globo.com/', 
                            'r7':'https://www.r7.com',
                            'ge':'https://ge.globo.com/', 
                            'estadao': 'https://www.estadao.com.br', 
                            'veja': 'https://veja.abril.com.br', 
                            'elpais': 'https://elpais.com/america/', 
                            'cartacapital': 'https://www.cartacapital.com.br/mais-recentes/', 
                            'cnnbrasil': 'https://www.cnnbrasil.com.br/', 
                            'terra': 'https://www.terra.com.br/noticias/', 
                            'bbc': 'https://www.bbc.com/portuguese/topics/cz74k717pw5t',
                            'ig': 'https://odia.ig.com.br/', 
                            'olhardigital': 'https://olhardigital.com.br/', 
                            'exame': 'https://exame.com/ultimas-noticias/', 
                            'theguardian': 'https://www.theguardian.com/international', 
                            'skynews': 'https://news.sky.com/world', 
                            'cnn': 'https://edition.cnn.com/', 
                            'nbc': 'https://www.nbcnews.com/world', 
                            'reuters': 'https://www.reuters.com/', 
                            'cbs': 'https://www.cbsnews.com/world/', 
                            'nyt': 'https://www.nytimes.com/international/section/world', 
                            'euronews': 'https://www.euronews.com/news/international', 
                            'wp': 'https://www.washingtonpost.com/', 
                            'foxnews': 'https://www.foxnews.com/', 
                            'abc': 'https://www.abc.net.au/news/world', 
                            'wsj': 'https://www.wsj.com/news/world?mod=nav_top_section'}

    def load_extractors(self):
        
        """ Loading search scheme """

        self.agency_extractors = {'uol':'headlineHorizontalAvatar__content__title', 
                                  'ge': 'feed-post-body-title gui-color-primary gui-color-hover',
                                  'g1': 'post__title', 
                                  'r7': 'widget-8x1-c__title', 
                                  'estadao':'headline', 
                                  'veja': 'title', 
                                  'elpais': 'c_d', 
                                  'cartacapital': 'l-list__text', 
                                  'cnnbrasil': 'home__title', 
                                  'terra': 'card-news__text--title main-url card-news__url', 
                                  'bbc':'promo-text', 
                                  'ig': 'title', 
                                  'olhardigital': 'cardV2-title', 
                                  'exame': 'touch-area', 
                                  'theguardian': 'u-faux-block-link__overlay js-headline-text', 
                                  'skynews': 'sdc-site-tile__headline', 
                                  'cnn': 'container__text container_lead-plus-headlines__text', 
                                  'nbc': 'wide-tease-item__headline', 
                                  'reuters': 'text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_5_and_half__3YluN heading__base__2T28j heading_5_half media-story-card__heading__eqhp9',
                                  'cbs': 'item__hed', 
                                  'nyt': 'css-14g652u e1y0a3kv0', 
                                  'euronews': 'm-object__title__link', 
                                  'wp': 'card-left card-text no-bottom', 
                                  'foxnews': 'title', 
                                  'abc': 'CardLayout_content__bev76', 
                                  'wsj': 'WSJTheme--headline--7VCzo7Ay'}
    
    def load_news(self, agency):
        
        """ Retrieving the news """
        
        url = self.agency_url[agency]
        headers = self.headers 
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")

        for item in soup.find_all(attrs={'class': self.agency_extractors[agency]}):
            self.agency_news.append(item.text.strip())
    
    def load_m_news(self):

        """ Loads multiple news sources """
    
        url1 = self.agency_url[self.agency1]
        url2 = self.agency_url[self.agency2]
        url3 = self.agency_url[self.agency3]

        headers = self.headers
        
        html1 = requests.get(url1, headers=headers)
        html2 = requests.get(url2, headers=headers)
        html3 = requests.get(url3, headers=headers)

        soup1 = BeautifulSoup(html1.text, "html.parser")
        soup2 = BeautifulSoup(html2.text, "html.parser")
        soup3 = BeautifulSoup(html3.text, "html.parser")
        
        for item in soup1.find_all(attrs={'class': self.agency_extractors[self.agency1]}):
            self.agency1_news.append(item.text.strip())

        for item2 in soup2.find_all(attrs={'class': self.agency_extractors[self.agency2]}):
            self.agency2_news.append(item2.text.strip())

        for item3 in soup3.find_all(attrs={'class': self.agency_extractors[self.agency3]}):
            self.agency3_news.append(item3.text.strip())
    
    def display_news(self, qnt=10, save=False):
       
        """ Displaying news results """
       
        i = 0
        for item in self.agency_news:
            if i == qnt:
                break
            result = "["+self.agency+"] "+item
            result = result.encode('utf-8').strip()
            print result
            i = i + 1
            if save == True:
                with open(self.agency+".txt", 'a') as fd:
                    fd.write(result)
                    fd.write("\n")
    
    def search_news(self, search_term, save=False):
    
        """ Search for specific keyword"""
    
        for item in self.agency_news:
            if search_term in item:
                result = "["+self.agency+"] "+item
                result = result.encode('utf-8').strip()
                print result
                if save == True:
                     with open(self.agency+".txt", 'a') as fd:
                        fd.write(result)
                        fd.write("\n")

    def search_news_agencies(self, search_term, save=False):

        """ Search search_term through agencies """

        for item in self.agency1_news:
            item = item.lower()

            if search_term in item:
                result = "["+self.agency1+"] "+item
                result = result.encode('utf-8').strip()
                print result
                if save == True:
                     with open(self.agency1+".txt", 'a') as fd:
                        fd.write(result)
                        fd.write("\n")

        for item in self.agency2_news:
            item = item.lower()

            if search_term in item:
                result = "["+self.agency2+"] "+item
                result = result.encode('utf-8').strip()
                print result
                if save == True:
                     with open(self.agency2+".txt", 'a') as fd:
                        fd.write(result)
                        fd.write("\n")
        
        for item in self.agency3_news:
            item = item.lower()
            
            if search_term in item:
                result = "["+self.agency3+"] "+item
                result = result.encode('utf-8').strip()
                print result
                if save == True:
                     with open(self.agency3+".txt", 'a') as fd:
                        fd.write(result)
                        fd.write("\n")




                        



            
                

            
        
    
            



        


