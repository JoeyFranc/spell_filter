import sys
import os
import filter
from flask import Flask, request, render_template, redirect

# Init app
app = Flask(__name__)


PATH = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = '/templates/index.html'

f = filter.Filter('static/spells.json')

def get_inquiry(inquiry_form):
# Read the inquiry form

    # Add each entry to the inquiry
    inq = {}
    for field in inquiry_form:
        # If key exists, append entry
        if field in inq:
            inq[ field ] += [ inquiry_form[field] ]
        else:  # create new entry
            inq[ field ] = [ inquiry_form[field] ]
    return inq

def inquire(inquiry):
# Perform a filter as instructed

    f.filter(inquiry)

def read_cookies(cookies):
    # Maintain display from last session if applicable
        
    # Init the cookie
    cookie = cookies['display']
    cook_values = cookie.split(';')
    cookie = {}
    for val in cook_values:
        key_val_pair = val.split('=')
        cookie[key_val_pair[0]] = key_val_pair[1]
    
    # Update the display
    f.query_by_name(cookie['display'])

def handle(request):
# Handle a request
    
    inquiry = get_inquiry(request.form)
    if 'append' in inquiry: read_cookies(request.cookies)
    inquire(inquiry)

# The index
@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def index():

    # Always init to empty display
    f.display = []

    try:
        # Do a query before rendering page if applicable
        if request.method == 'POST':
            handle(request)

        # Render the page
        return render_template('index.html', show=str, display=f.display)

    # If error occurs, go to error page
    except:
        return redirect('error', code=303)

@app.route('/error')
def error():

    return 'THERE WAS AN ERROR D:'

if __name__ == '__main__':
    app.run()
