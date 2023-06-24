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
    time.sleep(3)
    # gradual loading of the site data so that you can get all the html code
    html = driver.page_source
    # with open('pag_2', 'w', encoding='utf-8') as f:
    #     f.write(html)
    # to write the received code to a file (not used)
    return html

def get_content_page_Ozone(url):
  # with open('page', 'r', encoding='utf-8') as f:
  #       html_file = f.read()
#   to read from an html code file (not used)
  html = get_HTML(url)
#   with bs4 we divide the html code and search for the parts we need by class name
  soup = BeautifulSoup(html, 'html.parser')
  products = soup.select('[class*=tile-hover-target]')
  dates = []
  for product in products[::2]:
      price, rate, name, href, img = None, None, None, None, None
      card = product.parent
      components = card.descendants
      for component in components:
          if component.name == "svg" and component.next_sibling!=None:
              if rate == None:
                  rate = component.next_sibling.text
                  try:
                      rate = float(rate)
                  except ValueError:
                      rate = 0
          # checking the correctness of the rating value

          # price
          if component.name == "div" and component.get("style") != None and '--ozPriceStrikethroughColor' in component.get("style"):
              price = component.previous_element.text


          # name
          if component.name == "span" and component.get("class") != None and 'tsBodyL' in component.get("class"):
              name = component.text
              href = "https://www.ozon.ru"+component.parent.get("href")

          # image
          if component.name == "img":
              img = component.get("src")



      if price == None or name == None or img == None or href == None or rate == None:
          continue
      #if it was not possible to find all the necessary data about the product

      data = {}
      data['price'] = price
      data['name'] = name
      data['href'] = href
      data['rate'] = rate
      data['img'] = img
      data['site']="Ozon"
      dates.append(data)
      if len(dates) > 10 :
          break

  return dates

# url = "https://www.ozon.ru/search/?text=золотые+часы&from_global=true"
# get_content_page(url)
