import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import urllib.parse

driver = webdriver.Edge()
response = driver.get("https://www.trulia.com/CA/San_Diego/")
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="search-result-list-container"]')))
print(response)
#should have a window pop up.

soup = BeautifulSoup(driver.page_source, 'html.parser')

result_container = soup.find_all('li', {'class':'sc-fc01d244-0'})
len(result_container)

results_update = []

for results in result_container: 
    if results.has_attr('data-testid'):
        results_update.append(results)

len(results_update)

url_1 = 'https://www.trulia.com'
url_2 = []
count = 0
#loop through the results in the results_update list for item
for item in results_update:
    for link in item.find_all('div', {'data-testid':'property-card-details'}):
        #print(link.find('a').get('href'))
        url_2.append(link.find('a').get('href'))
        #loop through the results_update and find all the divs with the 
        #attribute of property card details 
        #then get the 'a' link and add to url_2 list

print(url_2)
#checking if we got some links
len(url_2)

url_joined = []

for link_2 in url_2: 
    url_joined.append(urllib.parse.urljoin(url_1, link_2))
    
url_joined

first_link = url_joined[0]
print(first_link)

#get request using a new driver and creating soup object
driver2 = webdriver.Edge()
response = driver2.get(first_link)
print(response)

soup2 = BeautifulSoup(driver2.page_source, 'html.parser')
soup2.find('span',{'data-testid':'home-details-summary-headline'}).get_text()
soup2.find('li', {'data-testid':'bed'}).get_text()
soup2.find('li', {'data-testid':'bath'}).get_text()
soup2.find('li', {'data-testid':'floor'}).get_text()
soup2.find('div', string = 'Year Built').findNext('div').findNext('div').get_text()
soup2.find('div', string = 'Parking').findNext('div').findNext('div').get_text()
soup2.find('h3', {'data-testid':'on-market-price-details'}).get_text()

# create lists with data 
address = []
bedrooms = []
bathrooms = []
area = []
year_built = []
parking = []
price = []

#loop through all joined links
for link in url_joined:
    #start new driver with link
    driver3 = webdriver.Edge()
    response = driver3.get(link)
    
    #create soup object
    soup3 = BeautifulSoup(driver3.page_source, 'html.parser')
    
    try:
        address.append(soup3.find('span',{'data-testid':'home-details-summary-headline'}).get_text())
    except:
        address.append('')
    
    try:
        bedrooms.append(soup3.find('li', {'data-testid':'bed'}).get_text())
    except:
        bedrooms.append('')
    
    try:
        bathrooms.append(soup3.find('li', {'data-testid':'bath'}).get_text())
    except:
        bathrooms.append('')
    
    try:
        area.append(soup3.find('li', {'data-testid':'floor'}).get_text())
    except: 
        area.append('')
    
    try:
        year_built.append(soup3.find('div', string = 'Year Built').findNext('div').findNext('div').get_text())
    except: 
        year_built.append('')
        
    try:
        parking.append(soup3.find('div', string = 'Parking').findNext('div').findNext('div').get_text())
    except:
        parking.append('')
    
    try:
        price.append(soup3.find('h3', {'data-testid':'on-market-price-details'}).get_text())
    except:
        price.append('')
        
    output = {'Address':address, 'Bedrooms':bedrooms, 'Bathrooms':bathrooms, 'Area':area, 
             'Year Built':year_built, 'Parking':parking, 'Price':price}
    
    #closing the driver at the end
    driver3.close()

#show output 
output

#putting output in a DataFrame
df = pd.DataFrame(output)
df

url_1 = 'https://www.trulia.com'
url_joined = []

for i in range(1,26):
    #https://www.trulia.com/CA/San_Diego/2_p/
    website = 'https://www.trulia.com/CA/San_Diego/' + str(i) + '_p/'
    
    #request
    driver4 = webdriver.Edge()
    response = driver4.get(website)
    WebDriverWait(driver4, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="search-result-list-container"]')))
    driver4.maximize_window()
    time.sleep(10) 

    #create soup object
    soup4 = BeautifulSoup(driver4.page_source, 'html.parser')
    
    #result container 
    result_container = soup4.find_all('li', {'class':'sc-fc01d244-0'})
    len(result_container)
    
    results_update = []

    for results in result_container: 
        if results.has_attr('data-testid'):
            results_update.append(results)
    
    #relative url
    relative_url = []
    #loop through the results in the results_update list for item
    for item in results_update:
        for link in item.find_all('div', {'data-testid':'property-card-details'}):
            relative_url.append(link.find('a').get('href'))
    len(relative_url)
    #joining urls
    for link_2 in relative_url: 
        url_joined.append(urllib.parse.urljoin(url_1, link_2))
    
len(url_joined)

# create lists with data 
address = []
bedrooms = []
bathrooms = []
area = []
year_built = []
parking = []
price = []


for link in url_joined:
    driver3 = webdriver.Edge()
    response = driver3.get(link)
    #create soup object
    soup3 = BeautifulSoup(driver3.page_source, 'html.parser')
    
    try:
        address.append(soup3.find('span',{'data-testid':'home-details-summary-headline'}).get_text())
    except:
        address.append('')
        
    try:
        bedrooms.append(soup3.find('li', {'data-testid':'bed'}).get_text())
    except:
        bedrooms.append('')
    
    try:
        bathrooms.append(soup3.find('li', {'data-testid':'bath'}).get_text())
    except:
        bathrooms.append('')
    
    try:
        area.append(soup3.find('li', {'data-testid':'floor'}).get_text())
    except: 
        area.append('')
    
    try:
        year_built.append(soup3.find('div', string = 'Year Built').findNext('div').findNext('div').get_text())
    except: 
        year_built.append('')
        
    try:
        parking.append(soup3.find('div', string = 'Parking').findNext('div').findNext('div').get_text())
    except:
        parking.append('')
    
    try:
        price.append(soup3.find('h3', {'data-testid':'on-market-price-details'}).get_text())
    except:
        price.append('')
        
    output = {'Address':address, 'Bedrooms':bedrooms, 'Bathrooms':bathrooms, 'Area':area, 
             'Year Built':year_built, 'Parking':parking, 'Price':price}
    
    #closing the driver at the end
    driver3.close()

#putting output in a DataFrame
df = pd.DataFrame(output)
df
df.to_csv('SanDiego_Data', encoding='utf-8', index=False)
