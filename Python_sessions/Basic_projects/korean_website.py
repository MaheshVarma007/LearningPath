from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import time

def scrape_korean_website(url):
    # Headers to make the request look like it's coming from a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return
            
        response_text = response.text
        
        soup = BeautifulSoup(response_text, 'html.parser')
        print(f"Title: {soup.title.string if soup.title else 'No title found'}")

        # Save HTML content
        with open('korean_website.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        print("HTML content saved to korean_website.html")


        translator= Translator()
        # Extract and save paragraph text
        with open('korean_website_english.txt', 'w', encoding='utf-8') as text_file:
            for paragraph in soup.find_all('p'):
                text = paragraph.get_text().replace('\n', '').strip()
                
                if text:
                    try:
                        print(f"Translating: {text}")
                        translated = translator.translate(text, src='ko', dest='en').text
                        print(f"Translated: {translated}")
                    except Exception as e:
                        translated = "[Translation failed]"
                    text_file.write(translated + '\n')
        print("Paragraph text saved to korean_website.txt")

        # Extract and save links
        links = soup.find_all('a')
        with open('korean_links.txt', 'w', encoding='utf-8') as links_file:
            for link in links:
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute URLs
                    if href.startswith('/'):
                        href = url.rstrip('/') + href
                    elif not href.startswith('http'):
                        href = url.rstrip('/') + '/' + href.lstrip('/')
                    links_file.write(href + '\n')
        print("Links saved to korean_links.txt")
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    
    web_url="https://모두의액상.kr"

    scrape_korean_website(web_url)

# This code scrapes a Korean website, extracts the title, paragraphs, and links,
# and saves them to HTML, text, and links files respectively.
# It uses UTF-8 encoding to handle Korean characters properly.
# Make sure to have the necessary libraries installed:
# pip install requests beautifulsoup4
# Also, ensure that the URL is accessible and correct.  