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
    Open the specified URL in a web browser using Selenium WebDriver. Wait for the page to load by waiting for the presence of the 
    `<body>`, `<footer>`, and `<span>` elements. Then, wait for the presence of an element with a CSS selector containing the 
    class "tile-hover-target". Finally, pause the execution for 2 seconds.
    """
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "span")))
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='tile-hover-target']")))
    time.sleep(2)
    html = driver.page_source 
    return html


"""
Given a URL, retrieve the content page of the Ozone website and extract information about products. 
@param url - the URL of the content page
@return A list of dictionaries containing information about the products, including price, name, URL, rating, image, and site.
"""
def get_content_page_Ozone(url):
  
  """
  Given a URL, retrieve the HTML content of the page and parse it using BeautifulSoup. 
  Find all elements with a class attribute containing "tile-hover-target" and store them 
  in the "products" variable. Initialize an empty list called "dates" to store the dates extracted from the HTML.
  """
  html = get_HTML(url)
  soup = BeautifulSoup(html, 'lxml')
  products = soup.select('[class*=tile-hover-target]')
  dates = []


  for product in products[::2]:
      
      price, rate, name, href, img = None, None, None, None, None
      card = product.parent
      components = card.descendants

      for component in components:
          
          """
          Check if the current component has the name "svg" and if 
          it has a next sibling. If both conditions are true, check if the rate 
          variable is None. If it is, assign the text value of the next sibling to the rate variable. 
          Then, try to convert the rate variable to a float. If it is not a valid float, assign 0 to the rate variable.
          """
          # rate
          if component.name == "svg" and component.next_sibling!=None:
              if rate == None:
                  rate = component.next_sibling.text
                  try:
                      rate = float(rate)
                  except ValueError:
                      rate = 0

          """
          Check if a given HTML component is a "div" element and has a "style" attribute. If the "style" 
          attribute contains the string "--ozPriceStrikethroughColor", extract the text of the previous 
          sibling element as the price.
          """
          # price
          if component.name == "div" and component.get("style") != None and '--ozPriceStrikethroughColor' in component.get("style"):
              price = component.previous_element.text

          """
          Check if the given component has the name "span" and a non-empty "class" attribute that contains the string "ts".
          If both conditions are met, extract the text content of the component and the value of the "href" attribute of its 
          parent's parent element.
          """
          # name
          if component.name == "span" and component.get("class") != None and 'ts' in str(component.get("class")):
              name = component.text
              href = component.parent.parent.get("href")

          """
          If the component's name is "img", get the value of the "src" attribute.
          """
          # image
          if component.name == "img":
              img = component.get("src")


      if price == None or name == None or img == None or href == None or rate == None:
          continue
      # if it was not possible to find all the necessary data, then we skip the product

      data = {}
      data['price'] = price
      data['name'] = name
      data['href'] = "https://www.ozon.ru"+href
      data['rate'] = rate
      data['img'] = img
      data['site']="Ozon"
      dates.append(data)
      if len(dates) > 10 :
          break
  return dates

