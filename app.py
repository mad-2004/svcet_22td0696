from flask import Flask, request, redirect, render_template_string
import random
import string
import json
import os

app = Flask(__name__)

# File to store URL mappings
url_mapping_file = "url_mapping.json"

# Function to load the URL mapping from the file
def load_url_mapping():
    if os.path.exists(url_mapping_file):
        with open(url_mapping_file, 'r') as file:
            return json.load(file)
    return {}

# Function to save the URL mapping to the file
def save_url_mapping(mapping):
    with open(url_mapping_file, 'w') as file:
        json.dump(mapping, file)

# Function to generate a random short URL
def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    url_mapping = load_url_mapping()  # Load the URL mapping from the file
    
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url()
        
        # Ensure the short URL doesn't already exist
        while short_url in url_mapping:
            short_url = generate_short_url()
        
        url_mapping[short_url] = long_url
        save_url_mapping(url_mapping)  # Save the updated mapping to the file
        
        return f'Short URL is: <a href="/{short_url}">/{short_url}</a>'
    
    return '''<form method="post">
                Long URL: <input type="text" name="long_url">
                <input type="submit" value="Shorten">
               </form>'''

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url_mapping = load_url_mapping()  # Load the URL mapping from the file
    long_url = url_mapping.get(short_url)
    if long_url:
        return redirect(long_url)
    return "URL not found!"

if __name__ == '__main__':
    app.run(debug=True)
