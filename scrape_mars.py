# dependensies
import pandas as pd
import time

from splinter import Browser
from bs4 import BeautifulSoup
import requests

#def init_browser():
    

def scrape():    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data = {}

    print("1")
    marsurl = "https://mars.nasa.gov/news/"
    print(marsurl)
    browser.visit(marsurl)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text

    news_p = soup.find('div', class_="rollover_description_inner").text

    print("-"*25)
    print("The latest Mars news is:",news_title)
    print("The summary of this latest news is:",news_p)

    # Add the news title and summary to the dictionary
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

    #JPL Mars Space Images - Featured Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    html = browser.html
    jplsoup = BeautifulSoup(html, 'html.parser')

    image_url = jplsoup.find('a', {'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')
    print("image url :",image_url)

    jpl_logo_href = jplsoup.find_all('div', class_='jpl_logo')
    print(jpl_logo_href)

    # Create BeautifulSoup object; parse with 'html.parser'
    html_page = browser.html
    jpl_soup = BeautifulSoup(html_page, "lxml")

    # Get all the hrefs of the url
    links = []
    for link in jpl_soup.find_all('a'):
        links.append(link.get('href'))
    
    jpl_link = links[1].strip('/')
    #print(jpl_link)

    featured_image_url = "https://"+jpl_link+image_url
    print("mars featured_image_url :")
    print("-"*25)
    print(featured_image_url)

    mars_data["featured_image_url"] = featured_image_url

    #Mars Weather
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)

    html = browser.html
    twittersoup = BeautifulSoup(html, 'html.parser')

    weather = twittersoup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    print("weather TweetTextSize class :",weather)

    mars_weather = weather.text.strip()
    print("mars weather deatils : ",mars_weather)

    mars_data["mars_weather"] = mars_weather

    #Mars Facts
    # Convert the url to a pandas df
    marsfacts_url = "https://space-facts.com/mars/"
    browser.visit(marsfacts_url)

    html = browser.html
    marsfactssoup = BeautifulSoup(html, 'html.parser')

    marsdf = pd.read_html(marsfacts_url)
    marsfacts_df = pd.DataFrame(marsdf[0])
    marsfacts_df.columns = ['mars_data','Data']
    marsdf1 = marsfacts_df.set_index("mars_data")
    print("mars data frame data")
    print("-"*25)
    print(marsdf1)

    # df to HTML table 
    marshtml = marsdf1.to_html(classes='marsdata')
    marstable = marshtml.replace('\n', ' ')
    print("mars df to HTML table ")
    print("-"*25)
    print(marstable)

    mars_data["marstable"] = marstable

    #Mars Hemisperes
    marshemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(marshemispheres_url)

    html = browser.html
    marshemispheresoup = BeautifulSoup(html, 'html.parser')

    #print(marshemispheresoup.prettify())

    images = marshemispheresoup.find('div', class_='collapsible results')
    #print(images.prettify())

    hemispheres_image_urls = []

    for i in range(len(images.find_all("div", class_="item"))):
        time.sleep(5)
        image = browser.find_by_tag('h3')
        image[i].click()
        html = browser.html
        hsoup = BeautifulSoup(html, 'html.parser')
        title = hsoup.find("h2", class_="title").text
        div = hsoup.find("div", class_="downloads")
        for li in div:
                link = div.find('a')
        url = link.attrs['href']
        hemispheres = {
                'title' : title,
                'img_url' : url
            }
        hemispheres_image_urls.append(hemispheres)
        browser.back()

    print("mars hemisphere image url :",hemispheres_image_urls)

    mars_data["hemispheres_image_urls"] = hemispheres_image_urls

    return mars_data

  # Testing 
if __name__ == "__main__":
    scrape()