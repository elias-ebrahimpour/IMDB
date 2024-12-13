from bs4 import BeautifulSoup
import requests

# Function to fetch user reviews from IMDb


def get_imdb_reviews(imdb_id, proxy_url="socks5://127.0.0.1:2080"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    url = f"https://www.imdb.com/title/{imdb_id}/reviews/"

    # Configure the proxy if provided
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    } if proxy_url else None

    # Make the request
    response = requests.get(url, headers=headers, proxies=proxies)
    if 200 <= response.status_code < 300:
        soup = BeautifulSoup(response.text, "html.parser")
        reviews = soup.find_all("div", class_="ipc-html-content-inner-div")
        # Extract and format up to 5 reviews
        extracted_reviews = [review.get_text(
            strip=True) for review in reviews[:5]]
        return extracted_reviews
    return ["Error fetching reviews."]
