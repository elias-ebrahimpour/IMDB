from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Function to fetch user reviews from IMDb
def get_imdb_reviews(imdb_id, comments_count=40):
    """
    Fetches all comments from an IMDb movie reviews page.

    Args:
        imdb_id (str): The IMDb ID of the movie (e.g., "tt0253474").

    Returns:
        list: A list of comments extracted from the reviews page.
    """
    url = f"https://www.imdb.com/title/{imdb_id}/reviews/?sort=submission_date%2Cdesc"
    comments = []

    # Configure headless mode for server execution
    chrome_options = Options()

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the IMDb reviews page
        driver.get(url)

        # Click the button inside the span with class "chained-see-more-button"
        try:
            wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
            chained_see_more_span = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.chained-see-more-button"))
            )
            button = chained_see_more_span.find_element(By.TAG_NAME, "button")
            button.click()

            # Wait for new comments to load (e.g., wait for a new element or an updated count of comments)
                        # Wait until the number of comments increases
            wait.until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.ipc-html-content-inner-div")) > comments_count
            )
        except Exception as e:
            print("Chained 'see more' button not found or clickable:", e)

         # Fetch the updated page source
        page_source = driver.page_source

        # Parse the updated content with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        review_elements = soup.find_all("div", class_="ipc-html-content-inner-div")

        for review in review_elements:
            comments.append(review.get_text(strip=True))

    finally:
        # Ensure the browser is closed
        driver.quit()

    return comments


# def get_imdb_reviews(imdb_id, proxy_url="socks5://127.0.0.1:2080"):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#     }
#     url = f"https://www.imdb.com/title/{imdb_id}/reviews/"

#     # Configure the proxy if provided
#     proxies = {
#         "http": proxy_url,
#         "https": proxy_url,
#     } if proxy_url else None

#     # Make the request
#     response = requests.get(url, headers=headers, proxies=proxies)
#     if 200 <= response.status_code < 300:
#         soup = BeautifulSoup(response.text, "html.parser")
#         reviews = soup.find_all("div", class_="ipc-html-content-inner-div")
#         # Extract and format up to 5 reviews
#         extracted_reviews = [review.get_text(
#             strip=True) for review in reviews[:5]]
#         return extracted_reviews
#     return ["Error fetching reviews."]
