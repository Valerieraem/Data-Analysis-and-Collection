from bs4 import BeautifulSoup
import requests
import pandas 

result = requests.get("https://www.trulia.com/CA/San_Diego/")
print(result.status_code)
#200 works, 404 not working
src = result.content

soup = BeautifulSoup(src, 'html.parser')
#print(soup)
#extract links and then extract the data from the links
#put all together and loop through all results in multiple pages
files = open("output.txt", "w")
files.write(str(soup))
files.close()

result_container = soup.find_all('li', attrs={'data-testid'})
print(len(result_container))

