#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 


# In[2]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[3]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[4]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[6]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = bs(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[7]:


slide_elem.find("div", class_='content_title')


# In[8]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[9]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[26]:


# Visit URL
PREFIX = "https://web.archive.org/web20181114023740"
url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[28]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[13]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = bs(html, 'html.parser')


# In[11]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[31]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[12]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[13]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[14]:


df.to_html()


# ### Mars Weather

# In[35]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[15]:


# Parse the data
html = browser.html
weather_soup = bs(html, 'html.parser')


# In[16]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[17]:


# 1. Use browser to visit the URL 
url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

html = browser.html
soup = bs(html, 'html.parser')
soup_links = soup.find_all('div', class_="description")

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
# 3. Write code to retrieve the image urls and titles for each hemisphere.
title_url ={}
for link in soup_links:
    url_hemisphere = 'https://astrogeology.usgs.gov' + link.find('a')['href']
    browser.visit(url_hemisphere)  
    html = browser.html
    soup = bs(html, 'html.parser')
    title = soup.find('h2', class_='title').text
    img_url = soup.find('img', class_='wide-image')['src']
    title_url["title"]= title
    title_url["img_url"]= 'https://astrogeology.usgs.gov' + img_url
    hemisphere_image_urls.append(title_url.copy())

# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)


# In[69]:


# 5. Quit the browser
browser.quit()


# In[ ]:




