from flask import Flask, render_template, request, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

app = Flask(__name__)

def mirror_page(url):
    # Set up Scraper API base URL
    api_url = 'http://api.scraperapi.com/?api_key=a482b31890cecb286368632fa8cbac74&url='

    # Concatenate the API URL and the requested URL
    full_url = api_url + url

    # Send a GET request to Scraper API
    response = requests.get(full_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the HTML content from the response
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Modify href links to redirect to the mirrored website
        base_url = request.base_url
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.startswith('#'):
                link['href'] = f"{base_url}?url={urljoin(url, href)}"

        # Modify src attributes to serve local resources
        for tag in soup.find_all(src=True):
            src = tag['src']
            if not re.match(r'^https?://', src):
                tag['src'] = urljoin(url, src)

        # Modify href attributes to serve local CSS files
        for tag in soup.find_all('link', {'rel': 'stylesheet'}):
            href = tag.get('href')
            if href and not href.startswith('#'):
                tag['href'] = urljoin(url, href)

        # Return the modified HTML content
        return str(soup)

    return f"Error occurred: HTTP Error {response.status_code}: {response.reason}"

@app.route('/')
def mirror_website():
    # Get the requested URL from the query parameters
    requested_url = request.args.get('url', 'https://cybervidyapeeth.in')
    # Mirror the requested page
    mirrored_page = mirror_page(requested_url)

    # Render the mirrored page
    return Response(mirrored_page, mimetype='text/html')

if __name__ == '__main__':
    app.run()

