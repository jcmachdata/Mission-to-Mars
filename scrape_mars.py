#dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd


#configure splinter
def init_browser():
    executable_path = {'executable_path': 'C:/Users/chamb/Documents/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #define dictionary to hold all of the Mars data
    mars_data = {}

    #define url to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html'
    html = browser.html
    soup = bs(html, 'html.parser')

    #find latest article title
    news_title = soup.find('div', class_="content_title").text
    mars_data['news_title'] = news_title


    #find latest paragraph
    news_p = soup.find('div', class_="rollover_description_inner").text
    mars_data['news_p'] = news_p

    
    #get JPL featured image
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)

    #access full image size
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_img_url = soup.find('img').get('src')
    mars_data['featured_img_url']=featured_img_url




#retrieve Mars weather from twitter account
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)


# In[54]:


html_weather = browser.html
soup = bs(html_weather, "html.parser")


# In[56]:


#get latest tweets
tweets = soup.find_all('div', class_='js-tweet-text-container')

#only get latest tweet that mentions weather-related items
for tweet in tweets: 
    weather_tweet = tweet.find('p').text
    if 'Sol' and 'winds' and 'pressure' in weather_tweet:
        print(weather_tweet)
        break
    else: 
        pass


# In[58]:


#use pandas to scrape tabular data from mars facts site
url = 'https://space-facts.com/mars/'


# In[60]:


tables = pd.read_html(url)


# In[61]:


tables


# In[63]:


#convert to pandas dataframe
df = tables[0]
df.columns = ['Attribute','Value']


# In[64]:


df


# In[127]:


#define main url of site pertaining to the hemispheres of Mars
main_url = 'https://astrogeology.usgs.gov'


# In[151]:


#navigate to page on Mars hemispheres
url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url_hem)
    
html_hemispheres = browser.html
soup = bs(html_hemispheres, 'html.parser')

#create list of hemisphere titles
items = soup.find_all('div', class_='item')


# In[152]:


#create empty list to hold hemisphere title and image url
hemisphere_images = []

#loop over hemispheres and save the titles and image links
for item in items:
    url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hem)
    
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')
    
    title = item.find('h3').text
    
    #navigate to specific hemisphere page
    browser.click_link_by_partial_text(title)
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')
    
    #construct link to hemisphere image
    partial_img_url = soup.find('img', class_='wide-image')['src']
    img_url = main_url + partial_img_url

    #append hemisphere title and image url to list
    hemisphere_images.append({"title":title,"img_url=":img_url})


# In[153]:


print(hemisphere_images)


# In[ ]:




