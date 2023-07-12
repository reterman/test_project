from flask import Flask, render_template, request, session
from create_data import *
import secrets
from flask_caching import Cache

"""
Create a Flask application instance named "app". Set the secret key for the application 
to a randomly generated token using the `secrets` module. Create a cache instance 
using the `Cache` class from Flask-Caching and configure it to use the "simple" cache type.
"""
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

"""
This function is a route handler for the root URL ("/"). When a user visits the root URL, 
it sets a session token to a unique value and renders the "home.html" template.
@return The rendered "home.html" template.
"""
@app.route('/')
def home():
    session['token']= 'unique-token'
    return render_template('home.html')


"""
This is a Flask route that handles a GET and POST request to '/scrape'.
@return The rendered "scrape.html" template.
"""
@app.route('/scrape', methods=['GET', 'POST'])
# This function is responsible for handling a POST request to scrape data. It takes the input from a form field named 'search' and performs the following steps.
def scrape():

    """
    It takes a form input named 'search' and performs some actions based on
    the value of 'name'. If 'name' is not None, it checks if a 'token' exists in the session. 
    If it does, it creates a dataset using the 'name' and stores it in the cache with the key 'data'. 
    It then removes the 'token' from the session. If 'token' does not exist in the session, it retrieves 
    the dataset from the cache with the key 'data'. If the dataset is not found in the cache, it creates a new 
    dataset using the 'name' and stores it in the cache. Finally, it renders the 'scrape.html
    """
    if request.method == 'POST':
        name = request.form['search']
        if name != None:
            
            # checking in case the user needs to refresh the page or return to products already found, without reloading the page
            if 'token' in session:
                dates = create_dataset(name)
                cache.set('data', dates )
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


"""
If the current module is being run as the main program, start the Flask application in debug mode.
This allows for easier debugging by providing detailed error messages.
"""
if __name__ == '__main__':
    app.run(debug=True)
