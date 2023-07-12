from WildBerries import *
from Ozone_Market import *
from KazanExpress import *
from CDEKmarket import *
from concurrent.futures import ThreadPoolExecutor

"""
Create a dataset by scraping data from multiple websites based on the given name.
@param name - the name of the product to search for
@return A list of data collected from different websites
"""
def create_dataset(name):
    """
    Replace any spaces in the given name with the appropriate characters for URL encoding.
    Then, generate four URLs using the modified name.
    """
    name1 = name.replace(" ", "+")
    name2 = name.replace(' ', '%20')
    print(name)
    url1 = "https://www.ozon.ru/search/?deny_category_prediction=true&text=" + name1 + "&from_global=true"
    url2 = "https://www.wildberries.ru/catalog/0/search.aspx?search=" + name1
    url3 = "https://kazanexpress.ru/search?query=" + name1 + "&needsCorrection=1"
    url4 = "https://cdek.shopping/?digiSearch=true&term=" + name2 + "&params=%7Csort%3DDEFAULT"

    """
    Create a ThreadPoolExecutor with a maximum of 4 workers. Submit four tasks to the executor, 
    each calling a function with a different URL as an argument. Store the resulting futures in a list. 
    Retrieve the results from the futures and append them to a list called "dates". Finally, return the "dates" list.
    """
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(get_content_page_Ozone, url1),
                   executor.submit(get_content_page_WildBerries, url2),
                   executor.submit(get_content_page_KazanExpress, url3),
                   executor.submit(get_content_page_CDEK, url4)]
        dates = futures[0].result()
        dates.extend(futures[1].result())
        dates.extend(futures[2].result())
        dates.extend(futures[3].result())
        return dates
