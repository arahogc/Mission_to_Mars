#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import dependecies 
from splinter import Browser
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import datetime as dt 


# In[2]:


def scrape_all(): 
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    #run all scraping functions and store results in a dictionary 
    data = {
        "news_title": news_title, 
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser), 
        "facts": mars_facts(), 
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data


# In[4]:


def mars_news(browser): 
    #Scrape mars news 
    #visit the mars news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #option delay for lading the page 
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #add try/execpt for the error handling 
    try: 
        slide_elem= news_soup.select_one("ul.item_list li.slide")
        #Use the parent element to find the first 'a' tag and save it as a 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        #Use the parent element to find the paragraph text 
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
            return None, None 

    return news_title, news_p


# In[14]:


def featured_image(browser):
    #Visit Url 
    try: 
        PREFIX = "https://web.archive.org/web20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1]/replace('"),',"")
        return 
        f'{PREFIX}_if/{article_background}'
    except: 
        return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'


# In[16]:


def mars_facts():
    #Add try/except for the error handling 
    try: 
        #Use 'read_html' to scrape the facts into a datframe 
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException: 
        return None 

        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)
        #Convert dataframe into HTML format, add bootstrap 
        return df.to_html(classes="table table-striped")
    
    if __name__ == "__main__":
        #if running as script, as print scraped data 
        print(scrape_all())


# In[ ]:




