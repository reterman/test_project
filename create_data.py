from main import *
from Ozone_Market import *
from concurrent.futures import ThreadPoolExecutor

def create_dataset(name):
    name = name.replace(" ", "+")
    print(name)
    url1 = "https://www.ozon.ru/search/?deny_category_prediction=true&text=" + name + "&from_global=true"
    url2 = "https://www.wildberries.ru/catalog/0/search.aspx?search=" + name

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(get_content_page_Ozone, url1),
                   executor.submit(get_content_page_WildBerries, url2)]
        dates = futures[0].result()
        dates.extend(futures[1].result())
        # for data in dates:
        #     print(data)
        return dates
# create_dataset("золотые часы")