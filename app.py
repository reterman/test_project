from flask import Flask, render_template, request
import requests
from main import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
# A rendering of the home page, where the field for entering product information will be located

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        name = request.form['search']
        if name != None:
            name = name.replace(" ", "+")
            print(name)
            # url = "https://www.wildberries.ru/catalog/0/search.aspx?search="+ name
            url = "https://www.ozon.ru/search/?text="+name+"&from_global=true"
            dates = get_content_page(url)
        # In the case of rendering a page without getting product data
        return render_template('scrape.html', dates=dates)
    else:
        return render_template('scrape.html')
# Render of the second page, which will display product cards

if __name__ == '__main__':
    app.run(debug=True)