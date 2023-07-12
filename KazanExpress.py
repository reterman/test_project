from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver

"""
Open a Chrome browser using the ChromeDriver and navigate to the specified URL.
@param URL - the URL of the webpage to retrieve HTML from
@return The HTML source code of the webpage
"""
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
    Open the specified URL in a web browser using Selenium WebDriver. Wait for the page to load by waiting 
    for the presence of the `<body>` tag and the `.subtitle-item` CSS selector. Once the page has loaded, 
    retrieve the HTML source code of the page.
    """
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".subtitle-item")))
    html = driver.page_source
    return html

"""
Given a URL, retrieve the content page of the KazanExpress website and extract information about products. 
@param url - the URL of the content page
@return A list of dictionaries containing information about the products, including price, 
        name, URL, rating, image, and site.
"""
def get_content_page_KazanExpress(url):

  """
  Retrieve the HTML content from a given URL and parse it using BeautifulSoup with the 'lxml' parser. Then, select all
  the div elements with a class attribute that starts with "col-mbs-12 col-mbm-6 col-xs-4 col-md-3 product-card"
  and store them in the variable "products".
  """
  html = get_HTML(url)
  soup = BeautifulSoup(html, 'lxml')
  products = soup.select('div[class^="col-mbs-12 col-mbm-6 col-xs-4 col-md-3 product-card"]')

  dates = []
  for i in range(len(products)):
      if i > 10:
          break
      #from each site no more than 10 cards

      """
      This code snippet extracts information from a product element on a website.
      - `product` is the current product element.
      - `price` is the price of the product, found by searching for a span element with the class "currency product-card-price slightly medium".
      - `name` is the name of the product, found by searching for an anchor element with the class "subtitle-item".
      - `img` is the source URL of the product image, found by searching for an image element with the class "main-card-icon-and-classname-collision-made-to-minimum" and retrieving the 'src' attribute.
      - `href` is the URL of the product, constructed by appending the href attribute of an anchor element with the class "subtitle-item"
      """
      product = products[i]
      price = product.find('span', class_="currency product-card-price slightly medium")
      name = product.find('a', class_="subtitle-item")
      img = product.find('img', class_="main-card-icon-and-classname-collision-made-to-minimum").get('src')
      href ="https://kazanexpress.ru"+ product.find('a', class_="subtitle-item").get('href')
      rate = product.find('span', attrs={'data-test-id': 'text__rating'})


      if price == None or name == None or img == None or href == None or rate == None:
          continue
      # if it was not possible to find all the necessary data, then we skip the product
      
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

