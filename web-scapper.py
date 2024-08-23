import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import time
from pymongo import MongoClient

def get_links(domain, url):
    """
    Fetch all links on a given webpage that belong to the same domain, excluding bookmarks.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urldefrag(urljoin(url, href))[0]  # Remove bookmarks
        if urlparse(full_url).netloc == domain:
            links.add(full_url)
    return links

def get_text_from_link(url):
    """
    Fetch the text content from a given webpage.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def scrape_links(domain, url, depth, max_depth, visited, db):
    """
    Recursively scrape links up to a specified depth and store the text in MongoDB if not already present.
    """
    if depth > max_depth or url in visited:
        return

    visited.add(url)
    print(f"scaping {url}")
    links = get_links(domain, url)
    text = get_text_from_link(url)

    if not db.scraped_data.find_one({"url": url}):
        db.scraped_data.insert_one({"url": url, "text": text})

    for link in links:
        time.sleep(0.1)  # Wait for 100ms between requests
        scrape_links(domain, link, depth + 1, max_depth, visited, db)

def main(base_url, max_depth, mongo_uri, mongo_db):
    """
    Main function to scrape links and text recursively and save them to MongoDB.
    """
    domain = urlparse(base_url).netloc
    visited = set()
    
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[mongo_db]

    scrape_links(domain, base_url, 0, max_depth, visited, db)

    client.close()

# Example usage
base_url = 'https://www.toronto.ca/'
max_depth = 5  # Set the desired recursion depth
mongo_uri = 'mongodb://localhost:27017/'  # Replace with your MongoDB URI
mongo_db = 'web_scraper'  # Replace with your MongoDB database name

main(base_url, max_depth, mongo_uri, mongo_db)
