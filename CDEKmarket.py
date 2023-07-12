from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver

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
    Open the specified URL in a web driver.  Wait until certain elements are present on the page before proceeding. 
    By.TAG_NAME - The locator strategy to find the element by its tag name. "body" - The tag name of the element to wait for. 
    Once the page has loaded, retrieve the HTML source code of the page.
    """
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".digi-product")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.digi-main-search-title")))
    html = driver.page_source
    return html

"""
Given a URL, retrieve the content page of the CDEK.shopping website and extract information about products. 
@param url - the URL of the content page
@return A list of dictionaries containing information about the products, including price, name, URL, rating, image, and site.
"""
def get_content_page_CDEK(url):
  
  """
  Given a URL, retrieve the HTML content of the webpage. Then, parse the HTML 
  using BeautifulSoup with the 'lxml' parser. Find all the div elements with the class name "digi-product" 
  and store them in the variable "products". Finally, initialize an empty list called "dates" to store 
  the dates extracted from the HTML.
  """
  html = get_HTML(url)
  soup = BeautifulSoup(html, 'lxml')
  products = soup.findAll('div', class_ = "digi-product")
  dates = []

  for i in range(len(products)):
      if i > 7:
          break
      # from each site no more than 8 cards

      """
      Find and extract the price, name, image source, and href link from a product element.
      price - the price of the product
      name - the name of the product
      img - the image source of the product
      href - the href link of the product
      """
      product = products[i]
      price = product.find('span', class_="digi-product-price-num")
      name = product.find('a', class_="digi-product__label")
      img =product.find('img', class_="digi-product__image").get('src')
      href = product.find('a', class_="digi-product__label").get('href')
     # CDEK does not provide product ratings
      rate = 0

      if price == None or name == None or img == None or href == None or rate == None:
          continue
      # if it was not possible to find all the necessary data, then we skip the product

      data = {}
      data['price']=price.text.replace(" ", "").replace('\n',' ').replace('\xa0',' ')
      data['name']=name.text.replace("  ", '').replace('\n','')
      data['href']="https://cdek.shopping"+href
      data['rate']=rate
      data['img']=img
      data['site']="CDEKmarket"
      dates.append(data)
  return dates

