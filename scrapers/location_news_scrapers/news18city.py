import aiohttp
import asyncio
import difflib
from datetime import datetime
from bs4 import BeautifulSoup

# URL of the website
BASE_URL = "https://www.news18.com/cities/"

# List of predefined city news pages
CITIES = [
    "mumbai-news", "new-delhi-news", "bengaluru-news", "hyderabad-news",
    "chennai-news", "ahmedabad-news", "pune-news", "noida-news",
    "gurgaon-news", "kolkata-news", "jaipur-news", "lucknow-news",
    "patna-news", "kanpur-news"
]

def get_best_matching_city(user_city: str) -> str:
    """Finds the best match for the user-provided city name."""
    formatted_city = user_city[0].lower().replace(" ", "-") + "-news"
    match = difflib.get_close_matches(formatted_city, CITIES, n=1, cutoff=0.6)
    return match[0] if match else None

async def news18_cities_scraper(base_url: str = BASE_URL, max_articles: int = 5, location: list = ["delhi"]) -> list:
    """Scrapes news articles for a specified city using fuzzy matching."""
    async with aiohttp.ClientSession() as session:
        extracted_links = []
        headers = {"User-Agent": "Mozilla/5.0"}

        # Get the best-matching city name
        matched_city = get_best_matching_city(location)
        if not matched_city:
            print(f"No matching city found for '{location}'. Skipping scraping.")
            return []

        # Construct the city news URL
        url = f"{base_url}{matched_city}"
        
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"Failed to fetch data for {matched_city} (HTTP {response.status})")
                    return []
                
                # Parse the HTML
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Find all <li> elements with the given class
                list_items = soup.find_all("li", class_="jsx-bdfb1b623b8585e8")

                # Extract article links
                city_urls = []
                for item in list_items:
                    link_tag = item.find("a")
                    link = link_tag["href"] if link_tag else None
                    if link and link.startswith("/"):
                        link = f"https://www.news18.com{link}"
                    if link:
                        city_urls.append(link)

                # Store only up to `max_articles` unique links
                extracted_links = list(set(city_urls[:min(2 * max_articles, len(city_urls))]))
                
            news = []
            print("Searching for location based news on News18...")
            
            ctr = 0
            for link in extracted_links:
                try:
                    async with session.get(link) as article_response:
                        if article_response.status != 200:
                            print(f"Failed to fetch article {link} (HTTP {article_response.status})")
                            continue
                            
                        article_html = await article_response.text()
                        soup = BeautifulSoup(article_html, 'html.parser')

                        h2_tag = soup.find('h2', id=lambda x: x and x.startswith('asubttl'))
                        h2_text = h2_tag.get_text() if h2_tag else 'No title found'

                        first_published = soup.find('ul', class_='fp')
                        date_time = first_published.get_text(strip=True) if first_published else None
                        if date_time:
                            dt = date_time.replace("First Published:", "").replace(",", "").replace("IST", "").strip()
                            date_time = datetime.strptime(dt, "%B %d %Y %H:%M")
                        else:
                            date_time = "No date found"

                        story_paras = soup.find_all('p', class_=lambda x: x and x.startswith('story_para_'))
                        story_texts = [para.get_text() for para in story_paras]
                        if len(story_texts) == 0:
                            continue
                        article_text = ' '.join(story_texts)

                        location = matched_city.split('-')[0]

                        news.append({"title": h2_text, "date_time": date_time, "content": article_text, "location": location})
                        ctr += 1
                        if ctr >= max_articles:
                            break
                        
                except Exception as e:
                    print(f"Error processing article {link}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error: {e}")
            return []

    print("Scraping complete. Total articles scraped:", len(news))
    return news