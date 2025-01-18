import re
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.openai_helper import identify_css_selectors_from_html


def configure_driver():
    """
    Configure and return a headless Selenium WebDriver.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def sanitize_css_selector(selector: str) -> str:
    """
    Attempt to fix minor syntax issues, including '++' usage, and handle NoneType.
    """
    if not selector or not isinstance(selector, str):  # Check for None or invalid type
        return ""

    # Fix consecutive plus signs -> single '+'
    while '++' in selector:
        selector = selector.replace('++', '+')

    return selector.strip()


def safe_select_one(soup: BeautifulSoup, selector: str):
    """
    Safely run soup.select_one(selector), avoiding errors if selector is empty or invalid.
    """
    if not selector or not selector.strip():
        return None
    try:
        return soup.select_one(selector)
    except Exception as e:
        print(f"Selector error with '{selector}': {e}")
        return None


def parse_reviews(html_content, css_selectors, driver=None):
    """
    Parse reviews from the current page using identified CSS selectors.
    Handles "Read More" links to extract the full review text.
    """
    reviews = []
    soup = BeautifulSoup(html_content, "html.parser")

    container_sel = sanitize_css_selector(css_selectors.get("review_container"))
    title_sel = sanitize_css_selector(css_selectors.get("title"))
    body_sel = sanitize_css_selector(css_selectors.get("body"))
    rating_sel = sanitize_css_selector(css_selectors.get("rating"))
    reviewer_sel = sanitize_css_selector(css_selectors.get("reviewer_name"))
    read_more_sel = sanitize_css_selector(css_selectors.get("read_more_button"))

    if not container_sel:
        print("Empty container selector. Skipping page.")
        return reviews

    try:
        review_elements = soup.select(container_sel)
    except Exception as e:
        print(f"Error selecting review containers: {e}")
        return reviews

    for index, element in enumerate(review_elements):
        # Handle "Read More" button if a selector is provided and driver is available
        if driver and read_more_sel:
            try:
                # Find the "Read More" button for the current review
                read_more_button = element.select_one(read_more_sel)
                if read_more_button:
                    # Scroll to the element and click
                    driver.execute_script("arguments[0].scrollIntoView();", read_more_button)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", read_more_button)
                    time.sleep(1)

                    # Update the soup with the expanded review content
                    html_content = driver.page_source
                    soup = BeautifulSoup(html_content, "html.parser")
                    element = soup.select(container_sel)[index]  # Re-fetch the specific review container
            except Exception as e:
                print(f"Failed to click 'Read More' for review {index}: {e}")

        # Extract review details with safe checks for None
        title_elem = safe_select_one(element, title_sel)
        body_elem = safe_select_one(element, body_sel)
        rating_elem = safe_select_one(element, rating_sel)
        reviewer_elem = safe_select_one(element, reviewer_sel)

        title = title_elem.get_text(strip=True) if title_elem else None
        body = body_elem.get_text(strip=True) if body_elem else None
        rating = rating_elem.get_text(strip=True) if rating_elem else None
        reviewer = reviewer_elem.get_text(strip=True) if reviewer_elem else None

        # Log missing elements for debugging
        if not title_elem:
            print(f"Missing title for review at index {index}")
        if not body_elem:
            print(f"Missing body for review at index {index}")
        if not rating_elem:
            print(f"Missing rating for review at index {index}")
        if not reviewer_elem:
            print(f"Missing reviewer for review at index {index}")

        # Skip empty reviews
        if not (title or body or rating or reviewer):
            continue

        reviews.append({
            "title": title,
            "body": body,
            "rating": rating,
            "reviewer": reviewer,
        })

    return reviews

def get_actual_next_button(soup, next_button_sel):
    """
    Return the correct 'next' button when the site uses the same selector
    for both 'previous' and 'next'. This filters out buttons/text that contain 'prev'.
    """
    candidates = soup.select(next_button_sel)
    for cand in candidates:
        text = cand.get_text(strip=True).lower()
        if 'prev' in text:
            continue
        return cand

    return None  # No valid next button found


def extract_reviews(url):
    """
    Main function to scrape reviews from a given URL using Selenium + OpenAI for dynamic CSS selectors.
    """
    driver = configure_driver()
    all_reviews = []
    max_failed_pages = 3
    failed_pages_count = 0

    try:
        driver.get(url)
        time.sleep(3)

        while True:
            html_content = driver.page_source

            css_selectors = identify_css_selectors_from_html(html_content)
            if not css_selectors:
                print("Failed to identify CSS selectors using OpenAI.")
                break

            print("CSS Selectors from OpenAI:", css_selectors)

            page_reviews = parse_reviews(html_content, css_selectors, driver)
            all_reviews.extend(page_reviews)
            print(f"Scraped {len(page_reviews)} reviews on this page. Total so far: {len(all_reviews)}")

            next_button_sel = sanitize_css_selector(css_selectors.get("next_button"))
            if not next_button_sel:
                print("No valid 'next_button' selector. Stopping pagination.")
                break

            soup = BeautifulSoup(html_content, "html.parser")
            next_button_element = get_actual_next_button(soup, next_button_sel)

            if not next_button_element:
                print("No valid next button found. Stopping pagination.")
                break

            next_href = next_button_element.get("href")
            if next_href:
                next_url = urljoin(url, next_href.strip())
                print(f"Navigating to next page: {next_url}")
                try:
                    driver.get(next_url)
                    time.sleep(3)
                except Exception as e:
                    print(f"Failed to load {next_url}: {e}")
                    failed_pages_count += 1
                    if failed_pages_count >= max_failed_pages:
                        break
                    continue
            else:
                try:
                    driver.execute_script("arguments[0].click();", next_button_element)
                    time.sleep(3)
                except Exception as e:
                    print(f"Failed to click next button: {e}")
                    failed_pages_count += 1
                    if failed_pages_count >= max_failed_pages:
                        break
                    continue

            failed_pages_count = 0

        return {
            "reviews_count": len(all_reviews),
            "reviews": all_reviews
        }

    except Exception as e:
        print(f"Error extracting reviews: {e}")
        return {
            "reviews_count": len(all_reviews),
            "reviews": all_reviews,
            "error": str(e)
        }
    finally:
        driver.quit()

