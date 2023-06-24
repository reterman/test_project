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
    # for i in range(1,3):
    #     coord = "window.scrollTo(0,"+ str(i*600)+");"
    #     driver.execute_script(coord)
    #     time.sleep(3)
    html = driver.page_source
    # gradual loading of the site data so that you can get all the html code

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
  # print(soup.prettify())
  products = soup.select('[class*=tile-hover-target]')
  dates = []
  i=0
  for product in products[::2]:

      price, rate, name, href, img = None, None, None, None, None
      card = product.parent
      components = card.descendants
      for component in components:

          # attributes
          if component.name == "svg" and component.next_sibling!=None:
              # print(component.next_sibling.text)
              if rate == None:
                  rate = component.next_sibling.text
                  try:
                      rate = float(rate)
                  except ValueError:
                      rate = 0
                  # print(rate)

          # price
          if component.name == "div" and component.get("style") != None and '--ozPriceStrikethroughColor' in component.get("style"):
              price = component.previous_element.text
              # print(price)


          # name
          if component.name == "span" and component.get("class") != None and 'tsBodyL' in component.get("class"):
              name = component.text
              # print(name)
              href = "https://www.ozon.ru"+component.parent.get("href")
              # print(href)

          # image
          if component.name == "img":
              img = component.get("src")
              # print(img)



          # print(img)
      if price == None or name == None or img == None or href == None or rate == None:
          continue
      # in case the card has a class with a different name (do not insert an empty value into the dictionary)

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

  # print(dates)
  return dates
      # print(price, i)
  #     print("-------------")
  # for date in dates:
  #     for ite  in date:
  #         print(ite)

      # print(card)
  #   price = product.parent.find('ins', class_="price__lower-price")
    #   name = product.find('span', class_="product-card__name")
    #   img ="https:" + product.find('img', class_="j-thumbnail").get('src')
    #   href = product.find('a', class_="product-card__link j-card-link j-open-full-product-card").get('href')
    #   rate = product.find('span', class_="address-rate-mini address-rate-mini--sm")
    #   get the necessary data from each card
    #   if price == None or name == None or img == None or href == None or rate == None:
    #       continue
    #   in case the card has a class with a different name (do not insert an empty value into the dictionary)

      # dates[i] = {}
      # dates[i]['price']=price.text.replace(" ", "")
      # dates[i]['name']=name.text.replace(" / ", '')
      # dates[i]['href']=href
      # dates[i]['rate']=rate.text
      # dates[i]['img']=img
  # return dates

# url = "https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=rate&search=золотые+часы"
# url = "https://www.ozon.ru/search/?text=золотые+часы&from_global=true"
# get_content_page(url)
