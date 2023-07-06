import requests
from bs4 import BeautifulSoup

# Define the URL you want to browse anonymously
url = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent/'

# Set up Scraper API base URL
api_url = 'http://api.scraperapi.com/?api_key=a482b31890cecb286368632fa8cbac74&url='

# Concatenate the API URL and the target URL
full_url = api_url + url

# Send a GET request to Scraper API
response = requests.get(full_url)

# Check if the request was successful
if response.status_code == 200:
    # Get the HTML content from the response
    html_content = response.text

    # Print the HTML content
    print(html_content)

else:
    print(f"Error occurred: HTTP Error {response.status_code}: {response.reason}")

