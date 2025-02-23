import time
import requests
from bs4 import BeautifulSoup


# URL of the website (Replace with the actual URL)
base_url = "https://www.news18.com/cities/"

def news18_cities_scraper(base_url: str, max_articles: int = 2):
    cities = ["mumbai-news", "new-delhi-news", "bengaluru-news", "hyderabad-news", "chennai-news", "ahmedabad-news", "pune-news", "noida-news", "gurgaon-news", "kolkata-news", "jaipur-news", "lucknow-news", "patna-news", "kanpur-news"]
    extracted_links = []
    headers = {"User-Agent": "Mozilla/5.0"}
    # Send a request to the website
    for city in cities:
        url = f"{base_url}{city}"
        
        response = requests.get(url, headers=headers)

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <li> elements with the given class
        list_items = soup.find_all("li", class_="jsx-bdfb1b623b8585e8")
        city_urls = []
        # Extract and print the text content and links
        for item in list_items:
            link_tag = item.find("a")  # Find the <a> tag
            link = link_tag["href"] if link_tag else "No link"  # Get the href attribute if available
            if link.startswith("/"):
                link = f"https://www.news18.com{link}"
            city_urls.append(link)

        extracted_links += city_urls[:min(max_articles, len(city_urls))]
        
    news = []
    for link in extracted_links:
        response = requests.get(link)

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the <h2> tag content
        h2_tag = soup.find('h2', id=lambda x: x and x.startswith('asubttl'))
        h2_text = h2_tag.get_text() if h2_tag else 'No <h2> tag found'

        # Extract all text content from story_para_ classes
        story_paras = soup.find_all('p', class_=lambda x: x and x.startswith('story_para_'))
        story_texts = [para.get_text() for para in story_paras]
        article_text = ' '.join(story_texts)

        # Extract the "First Published" date and time
        first_published = soup.find('ul', class_='fp')
        first_published_text = first_published.get_text(strip=True) if first_published else 'No First Published date found'

        news.append({"title": h2_text, "date_time": first_published_text, "content": article_text})

    return news