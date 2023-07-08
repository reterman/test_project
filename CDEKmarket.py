from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
    # using the method of explicit loading of the product page
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".digi-product")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.digi-main-search-title")))
    html = driver.page_source

    # with open('pag_2', 'w', encoding='utf-8') as f:
    #     f.write(html)
    # to write the received code to a file (not used)
    return html

def get_content_page_CDEK(url):
  # with open('page', 'r', encoding='utf-8') as f:
  #       html_file = f.read()
  # to read from an html code file (not used)
  html = get_HTML(url)
  # with bs4 we divide the html code and search for the parts we need by class name
  soup = BeautifulSoup(html, 'lxml')
  products = soup.findAll('div', class_ = "digi-product")
  dates = []
  for i in range(len(products)):
      if i > 7:
          break
      # from each site no more than 8 cards
      product = products[i]
      price = product.find('span', class_="digi-product-price-num")
      name = product.find('a', class_="digi-product__label")
      img =product.find('img', class_="digi-product__image").get('src')
      href = product.find('a', class_="digi-product__label").get('href')
      rate = 0
      # get the necessary data from each card
      if price == None or name == None or img == None or href == None or rate == None:
          continue
      #if it was not possible to find all the necessary data about the product

      data = {}
      data['price']=price.text.replace(" ", "").replace('\n',' ').replace('\xa0',' ')
      data['name']=name.text.replace("  ", '').replace('\n','')
      data['href']="https://cdek.shopping"+href
      data['rate']=rate
      data['img']=img
      data['site']="CDEKmarket"
      dates.append(data)
  return dates

# url = "https://cdek.shopping/?digiSearch=true&term=электронные%20золотые%20часы&params=%7Csort%3DDEFAULT"
# get_content_page_CDEK(url)
