from selenium import webdriver                    # Import module 
from selenium.webdriver.common.keys import Keys   # For keyboard keys 
from selenium.webdriver.chrome.service import Service # Start and stop browser service
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs               # parse this html
import time     # Waiting function for page to load
import pandas as pd
import pymongo
from selenium.webdriver.common.by import By


mars_dict = {}
def init_driver():
    # Locate Driver in system
    Path = "C:\SeleniumDrivers\chromedriver.exe"
    service = Service(Path)
    service.start()
    driver = webdriver.Remote(service.service_url)
    driver.implicitly_wait(40) 
    return driver

def scrape_news(): 
    news = "https://mars.nasa.gov/news/"
    driver = init_driver()
    # Retrieve the latest news title
    driver.get(news)
    title_elements = driver.find_elements_by_class_name("content_title")
    title_htmls = [title_element.get_attribute("innerHTML") for title_element in title_elements]
    title_html = title_htmls[1]
    news_soup = bs(title_html, 'lxml')
    title = news_soup.get_text()
    
    teaser_element = driver.find_element_by_class_name("article_teaser_body")
    teaser_html = teaser_element.get_attribute("innerHTML")
    mars_dict['title'] = title
    mars_dict['summary'] = teaser_html 
    driver.quit()
    return mars_dict

def scrape_featured():
    featured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    driver = init_driver()
    driver.get(featured)
    featured_page_url_element = driver.find_element_by_xpath("//*[@id='full_image']")
    featured_page_url_element.click()
    featured_link_element = driver.find_element_by_link_text('more info')
    featured_link_element.click()
    featured_image_elements = driver.find_elements_by_class_name('main_image')
    featured_image_links = [featured_image_element.get_attribute("src") for featured_image_element in featured_image_elements]
    featured_image_link = featured_image_links[0]
    mars_dict['featured_image'] = featured_image_link
    driver.quit()
    return mars_dict
    
def scrape_table():
    facts = "https://space-facts.com/mars/"
    tables = pd.read_html(facts)
    facts_df = tables[0]
    facts_df.columns = ["Mars Attributes", "Data"]
    fact_html = facts_df.to_html()
    mars_dict['fact_table'] = str(fact_html)
    return mars_dict

def scrape_hemisphere():
    hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemi_dict = {} 
    driver = init_driver()
    driver.get(hemisphere); # Add Urls Here!
    hemisphere_elements = driver.find_elements_by_tag_name('h3')
    hemisphere_elements[0].click()
    hemi_links = driver.find_elements_by_class_name('wide-image')
    cerb_links = [cerb_img.get_attribute("src") for cerb_img in hemi_links]
    cerb_link = cerb_links[0]
    driver.back()
    driver.refresh()
    
    hemisphere_elements = driver.find_elements_by_tag_name('h3')
    hemisphere_elements[1].click()
    hemi2_links = driver.find_elements_by_class_name('wide-image')
    schi_links = [schi_img.get_attribute("src") for schi_img in hemi2_links]
    schi_link = schi_links[0]
    driver.back()
    driver.refresh()
    
    hemisphere_elements = driver.find_elements_by_tag_name('h3')
    hemisphere_elements[2].click()
    hemi3_links = driver.find_elements_by_class_name('wide-image')
    syrt_links = [schi_img.get_attribute("src") for schi_img in hemi3_links]
    syrt_link = syrt_links[0]
    driver.back()
    driver.refresh()
    
    hemisphere_elements = driver.find_elements_by_tag_name('h3')
    hemisphere_elements[3].click()
    hemi4_links = driver.find_elements_by_class_name('wide-image')
    vall_links = [schi_img.get_attribute("src") for schi_img in hemi4_links]
    vall_link = vall_links[0]
    driver.back()
    driver.refresh() 
    
    hemisphere_elements = driver.find_elements_by_tag_name('h3')
    hemisphere_element_htmls = [hemisphere_element.get_attribute("innerHTML") for hemisphere_element in hemisphere_elements]
    hemi_image = [cerb_link, schi_link, syrt_link,  vall_link]
    hemi_dict['title'] = hemisphere_element_htmls
    hemi_dict['img_url'] = hemi_image  
    hemi_list = [hemi_dict]
    mars_dict['hemisphere_images'] = hemi_list
    driver.quit()
    return mars_dict

def run():  
    scrape_news()
    time.sleep(5)
    scrape_featured() 
    time.sleep(5)
    scrape_table()
    time.sleep(5)
    scrape_hemisphere()
    time.sleep(5)
    return mars_dict






        