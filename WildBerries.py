from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
import time

'''
Open a Chrome browser using the ChromeDriver and navigate to the specified URL.
@param URL - the URL of the webpage to retrieve HTML from
@return The HTML source code of the webpage
'''
def get_HTML(URL):

    """
    Create a new instance of the `Service` class, providing the path to the ChromeDriver executable as an argument. 
    Create a Chrome webdriver instance with specific options.
    """
    service = Service(r".\lib\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--log-level=3')
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    """
    Open the specified URL in a web driver. Wait for the presence of the body tag and the CSS selector 
    ".product-card__wrapper" on the web page using the provided driver and a timeout of 10 seconds. 
    Wait for the product card wrapper element to be present on the page. 
    Scroll the window to a specific coordinate in increments of 600 pixels. 
    Pause for 0.5 seconds between each scroll.
    """
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card__wrapper")))
    for i in range(1,2):
        coord = "window.scrollTo(0,"+ str(i*600)+");"
        driver.execute_script(coord)
        time.sleep(0.5)
    html = driver.page_source
    return html

""" 
Given a URL, retrieve the content page of the WildBerries website and extract information about products. 
@param url - the URL of the content page
@return A list of dictionaries containing information about the products, including price, name, URL, rating, image, 
        and site.
"""
def get_content_page_WildBerries(url):
  
  """
  Given a URL, retrieve the HTML content of the page and parse it using BeautifulSoup. 
  Find all the div elements with the class "product-card__wrapper" and store them in the variable "products". 
  Initialize an empty list called "dates" to store the dates.
  """
  html = get_HTML(url)
  soup = BeautifulSoup(html, 'lxml')
  products = soup.findAll('div', class_ = "product-card__wrapper")
  dates = []

  for i in range(len(products)):
      if i > 10:
          break
      #from each site no more than 10 cards

      """
      Find and extract specific information from a product element on a webpage.
      product - the product element
      price - the lower price of the product
      name - the name of the product
      img - the URL of the product image
      href - the URL of the product page
      rate - the rating of the product
      """
      product = products[i]
      price = product.find('ins', class_="price__lower-price")
      name = product.find('span', class_="product-card__name")
      img ="https:" + product.find('img', class_="j-thumbnail").get('src')
      href = product.find('a', class_="product-card__link j-card-link j-open-full-product-card").get('href')
      rate = product.find('span', class_="address-rate-mini address-rate-mini--sm")


      if price == None or name == None or img == None or href == None or rate == None:
          continue
      # if it was not possible to find all the necessary data, then we skip the product
      
      try:
          rate = float(rate.text)
      except ValueError:
          rate = 0
      # checking the correctness of the rating value

      data = {}
      data['price']=price.text.replace(" ", "")
      data['name']=name.text.replace(" / ", '')
      data['href']=href
      data['rate']=rate
      data['img']=img
      data['site']="WildBerries"
      dates.append(data)
  return dates
