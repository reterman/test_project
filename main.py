from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def get_HTML(URL):

    service = Service(r".\lib\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--log-level=3')
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    # pre-setting the necessary settings and further connecting them to simulate the operation and loading of the URL page
    driver.get(URL)
    time.sleep(1)
    for i in range(1,3):
        coord = "window.scrollTo(0,"+ str(i*600)+");"
        driver.execute_script(coord)
        time.sleep(3)
    html = driver.page_source
    # gradual loading of the site data so that you can get all the html code

    # with open('pag_2', 'w', encoding='utf-8') as f:
    #     f.write(html)
    # to write the received code to a file (not used)
    return html

def get_content_page(url):
  # with open('page', 'r', encoding='utf-8') as f:
  #       html_file = f.read()
#   to read from an html code file (not used)
  html = get_HTML(url)
#   with bs4 we divide the html code and search for the parts we need by class name
  soup = BeautifulSoup(html, 'html.parser')
  products = soup.findAll('div', class_ = "product-card__wrapper")
  dates = {}
  for i in range(len(products)):
      if i > 10:
          break
    #   from each site no more than 10 cards
      product = products[i]
      price = product.find('ins', class_="price__lower-price")
      name = product.find('span', class_="product-card__name")
      img ="https:" + product.find('img', class_="j-thumbnail").get('src')
      href = product.find('a', class_="product-card__link j-card-link j-open-full-product-card").get('href')
      rate = product.find('span', class_="address-rate-mini address-rate-mini--sm")
    #   get the necessary data from each card
      if price == None or name == None or img == None or href == None or rate == None:
          continue
    #   in case the card has a class with a different name (do not insert an empty value into the dictionary)
      
      dates[i] = {}
      dates[i]['price']=price.text.replace(" ", "")
      dates[i]['name']=name.text.replace(" / ", '')
      dates[i]['href']=href
      dates[i]['rate']=rate.text
      dates[i]['img']=img
  return dates

# url = "https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=rate&search=золотые+часы"
# get_content_page()
