import requests
from bs4 import BeautifulSoup



def scrape_w3(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Print the title of the page
        print("Title of the page:", soup.title.string if soup.title else "No title found")
        
        # Find all paragraph tags and print their text
        paragraphs = soup.find_all('p')
        for i, p in enumerate(paragraphs, start=1):
            print(f"Paragraph {i}: {p.get_text()}")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    url = "https://www.w3schools.com"
    scrape_w3(url)