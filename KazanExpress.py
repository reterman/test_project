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
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    # pre-setting the necessary settings and further connecting them to simulate the operation and loading of the URL page
    driver.get(URL)
    time.sleep(3)
    # for i in range(1,3):
    #     coord = "window.scrollTo(0,"+ str(i*600)+");"
    #     driver.execute_script(coord)
    #     time.sleep(3)
    # gradual loading of the site data so that you can get all the html code
    html = driver.page_source


    # with open('pag_2', 'w', encoding='utf-8') as f:
    #     f.write(html)
    # to write the received code to a file (not used)
    return html

def get_content_page_KazanExpress(url):
  # with open('page', 'r', encoding='utf-8') as f:
  #       html_file = f.read()
#   to read from an html code file (not used)
  html = get_HTML(url)
  #with bs4 we divide the html code and search for the parts we need by class name
  soup = BeautifulSoup(html, 'lxml')
  products = soup.select('div[class^="col-mbs-12 col-mbm-6 col-xs-4 col-md-3 product-card"]')
  dates = []
  for i in range(len(products)):
      if i > 10:
          break

      #from each site no more than 10 cards
      product = products[i]
      price = product.find('span', class_="currency product-card-price slightly medium")
      name = product.find('a', class_="subtitle-item")
      img = product.find('img', class_="main-card-icon-and-classname-collision-made-to-minimum").get('src')
      href ="https://kazanexpress.ru"+ product.find('a', class_="subtitle-item").get('href')
      rate = product.find('span', attrs={'data-test-id': 'text__rating'})
      #get the necessary data from each card
      # if price == None or name == None or img == None or href == None or rate == None:
      #     continue
      #if it was not possible to find all the necessary data about the product
      try:
          rate = float(rate.text)
      except Exception:
          rate = 0
      # checking the correctness of the rating value

      data = {}
      data['price']=price.text.replace(" ", "")
      data['name']=name.text.replace("  ", '').replace('\n', '')
      data['href']=href
      data['rate']=rate
      data['img']=img
      data['site']="KazanExpress"
      dates.append(data)
  return dates

# url = "https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=rate&search=золотые+часы"
# get_content_page()
# get_HTML("https://kazanexpress.ru/search?query=золотые%20часы")
# get_content_page_WildBerries("https://kazanexpress.ru/search?query=золотые%20часы")