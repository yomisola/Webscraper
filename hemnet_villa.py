from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("/Users/adeyomisola/Desktop/chromedriver")

street = []
location = []
price = []
size = []
number_of_rooms = []
price_per_m = []
features = []
housing_type = []

driver.get("https://www.hemnet.se/bostader?location_ids%5B%5D=18031&item_types%5B%5D=villa")

content = driver.page_source
soup = BeautifulSoup(content, features="lxml")
rows = soup.findAll(name = "li", attrs = {'class': 'normal-results__hit js-normal-list-item'})


for row in rows:
    st_row = row.find("h2", attrs = {'class': 'listing-card__street-address qa-listing-title'})
    loc_row = row.find("span", attrs = {'class': 'listing-card__location-name'})
    attrs_rows = row.findAll("div", attrs={'class': 'listing-card__attribute listing-card__attribute--primary'})
    price_p_m_row = row.find("div", attrs={'class': 'listing-card__attribute listing-card__attribute--secondary listing-card__attribute--square-meter-price'})
    features_row = row.findAll("span", attrs = {'class': 'listing-card__label listing-card__label--feature'})

    street.append(st_row.text.strip())
    location.append(loc_row.text.strip())
    price.append(attrs_rows[0].text.strip())
    size.append(attrs_rows[1].text.strip())
    number_of_rooms.append(attrs_rows[2].text.strip())
        
    if price_p_m_row is not None:
        price_per_m.append(price_p_m_row.text.strip())
    else:
        price_per_m.append("0")
        
    housing_type.append("Apartments")

    feature_concat = ""
    if len(features_row) > 0:
        for feat in features_row:
            feature_concat = feature_concat + ", " + feat.text.strip()
    features.append(feature_concat)


df = pd.DataFrame({'Location':location,'Street':street,'Price':price, 'Size': size, 'Number of rooms': number_of_rooms, 'Price Per msq': price_per_m, 'Features': features}) 
df.to_csv('hemnet_villa.csv', index=False, encoding='utf-8')
    
