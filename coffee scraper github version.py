import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from tqdm import tqdm

# this is my own package to use my own headers to make the scrape possible.
import WebscrapingCommon as wc # if you google headers you can find good ones online.

################################################
# make sure you update the save path for the csv file and make your own headers!!!
###############################################

date, coffee_list, cost = [], [], []

def get_data(url):
    headers = wc.headers

    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")
    today = str(dt.date.today())
    coffee_names = soup.find_all('a', {'class' : 'product-item__title'})
    coffee_prices = soup.find_all('span', {'class' : 'product-price--original'})
    for coffee in coffee_names:
        date.append(today)
        coffee_list.append(coffee.text)
    for prices in coffee_prices:
        cost.append(prices.text)
        
print('Beginning scrape')

url= 'https://coffeebeancorral.com/collections/all-green-coffee-beans-collection?page=1'

coffee = requests.get(url)

soup = BeautifulSoup(coffee.text, 'html.parser')

# this finds the last number for the page select on the website
last_page = str(soup.find('ul', {'class' : 'pagination'}).find_all('li', {'class' : 'lap-hide'})[1].text.split()[-1])

# turns it into an integer to be used in the for loop later
max_len = int(last_page)
total_pages = max_len

# get the first page of coffee info
print('There are a total of ' + str(total_pages) + ' pages.')
get_data(url)

# get all other pages for coffee info
for x in tqdm(range(2, max_len + 1)):
    url = 'https://coffeebeancorral.com/collections/all-green-coffee-beans-collection?page=' + str(x)
    get_data(url)
    
print('Converting data')

coffee_list = [coffee.strip() for coffee in coffee_list]
cost = [price.split()[1].strip('\n$') for price in cost]

coffee_df = pd.DataFrame({'Date' : date,
                         'Coffee' : coffee_list,
                         'Cost' : cost})

# print(coffee_df)

print('Saving to csv file')

# put in your own save path
save_path = r"your\save\path.csv"

#Keep this one to append files
coffee_df.to_csv(save_path, mode = 'a', header = False, index = False)

print('Done')