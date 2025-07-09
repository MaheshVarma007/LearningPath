#A program to scrape a webpage and write the data to a csv file
import requests
from bs4 import BeautifulSoup

def scrape_contacts(url):
    response=requests.get(url)
    print(f"Status: {response.status_code}")
    response=response.text
    
    soup=BeautifulSoup(response, 'html.parser')
    #print(soup.prettify())
    print(f"Title: {soup.title.string}")

    file= open('stability.html', 'w')
    file.write(soup.prettify())
    file.close()

    # Save all the text content to a csv file without spaces or newlines
    # This will create a CSV file with the text content of the webpage
    with open('stability.pdf', 'w') as pdf_file:
        for paragraph in soup.find_all('p'):
            text = paragraph.get_text().replace('\n', '')
            pdf_file.write(text + '\n')
            #pdf_file.close()
    print("Data has been written to stability.pdf")

    # i want to extract all the links from the webpage
    links = soup.find_all('a')
    with open('links.txt', 'w') as links_file:
        for link in links:
            href = link.get('href')
            if href:
                links_file.write(href + '\n')
    print("Links have been written to links.txt")

if __name__ == "__main__":
    url = "https://stability.ai"  # Replace with the actual URL
    scrape_contacts(url)