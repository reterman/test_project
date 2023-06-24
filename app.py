from flask import Flask, render_template, request, session
import requests
from Ozone_Market import *
from concurrent.futures import ThreadPoolExecutor
from main import *
from create_data import *
import secrets
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def home():
    session['token']= 'unique-token'
    return render_template('home.html')


# A rendering of the home page, where the field for entering product information will be located

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        name = request.form['search']
        if name != None:
            # checking in case the user needs to refresh the page or return to products already found, without reloading the page
            if 'token' in session:
                dates = create_dataset(name)
                cache.set('data', dates)
                session.pop('token', None)
            else:
                dates = cache.get('data')
                if dates == None:
                    dates = create_dataset(name)
                cache.set('data', dates)

        # In the case of rendering a page without getting product data
        return render_template('scrape.html', dates = dates)
    else:
        return render_template('scrape.html')


# Render of the second page, which will display product cards

if __name__ == '__main__':
    app.run(debug=True)
