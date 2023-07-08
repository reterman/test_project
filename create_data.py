from WildBerries import *
from Ozone_Market import *
from KazanExpress import *
from CDEKmarket import *
from concurrent.futures import ThreadPoolExecutor

def create_dataset(name):
    name1 = name.replace(" ", "+")
    name2 = name.replace(' ', '%20')
    print(name)
    url1 = "https://www.ozon.ru/search/?deny_category_prediction=true&text=" + name1 + "&from_global=true"
    url2 = "https://www.wildberries.ru/catalog/0/search.aspx?search=" + name1
    url3 = "https://kazanexpress.ru/search?query=" + name1 + "&needsCorrection=1"
    url4 = "https://cdek.shopping/?digiSearch=true&term=" + name2 + "&params=%7Csort%3DDEFAULT"
    # launch 4 scrapers and combine the received data
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
# create_dataset("золотые часы")