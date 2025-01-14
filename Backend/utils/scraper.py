import re
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Import the improved OpenAI helper
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
    Attempt to fix minor syntax issues, including '++' usage.
    """
    if not selector:
        return selector

    # Fix consecutive plus signs -> single '+'
    while '++' in selector:
        selector = selector.replace('++', '+')

    return selector


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


def parse_current_page_reviews(html_content, css_selectors, url=None):
    """
    Parse reviews from the current page using identified CSS selectors.
    Expects the following keys from OpenAI:
      - review_container
      - title
      - body
      - rating
      - reviewer_name
    """
    reviews = []
    soup = BeautifulSoup(html_content, "html.parser")

    container_sel = sanitize_css_selector(css_selectors.get("review_container") or "")
    title_sel = sanitize_css_selector(css_selectors.get("title") or "")
    body_sel = sanitize_css_selector(css_selectors.get("body") or "")
    rating_sel = sanitize_css_selector(css_selectors.get("rating") or "")
    reviewer_sel = sanitize_css_selector(css_selectors.get("reviewer_name") or "")

    if not container_sel.strip():
        print("OpenAI provided an empty container selector. Skipping page.")
        return reviews

    try:
        review_elements = soup.select(container_sel)
    except Exception as e:
        print(f"Invalid container selector '{container_sel}': {e}")
        return reviews

    for element in review_elements:
        title_elem = safe_select_one(element, title_sel)
        body_elem = safe_select_one(element, body_sel)
        rating_elem = safe_select_one(element, rating_sel)
        reviewer_elem = safe_select_one(element, reviewer_sel)

        title = title_elem.get_text(strip=True) if title_elem else None
        body = body_elem.get_text(strip=True) if body_elem else None
        rating = rating_elem.get_text(strip=True) if rating_elem else None
        reviewer = reviewer_elem.get_text(strip=True) if reviewer_elem else None

        # Skip if all are empty
        if not (title or body or rating or reviewer):
            continue

        reviews.append({
            "title": title,
            "body": body,
            "rating": rating,
            "reviewer": reviewer
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
        # If the text includes 'prev' or 'previous', skip it
        if 'prev' in text:
            continue
        # Otherwise, assume this is our next button candidate
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
            # 1. Get the current page's HTML
            html_content = driver.page_source

            # 2. Identify CSS selectors via OpenAI
            css_selectors = identify_css_selectors_from_html(html_content)
            if not css_selectors:
                print("Failed to identify CSS selectors using OpenAI.")
                break

            print("CSS Selectors from OpenAI:", css_selectors)

            # 3. Parse the current page for reviews
            page_reviews = parse_current_page_reviews(html_content, css_selectors, url=url)
            all_reviews.extend(page_reviews)
            print(f"Scraped {len(page_reviews)} reviews on this page. Total so far: {len(all_reviews)}")

            # 4. Handle pagination after scraping the current page
            next_button_sel = sanitize_css_selector(css_selectors.get("next_button") or "")
            if not next_button_sel.strip():
                print("No valid 'next_button' selector. Stopping pagination.")
                break

            soup = BeautifulSoup(html_content, "html.parser")

            try:
                # Instead of a single safe_select_one, we call our custom function
                next_button_element = get_actual_next_button(soup, next_button_sel)
            except Exception as e:
                print(f"Error with next button selector '{next_button_sel}': {e}")
                failed_pages_count += 1
                if failed_pages_count >= max_failed_pages:
                    print("Too many invalid selectors. Stopping.")
                break

            if not next_button_element:
                print("No next button found (or it's a 'previous' button). Stopping pagination.")
                break

            # 5. Attempt to either follow href or click the next button
            next_href = next_button_element.get("href")
            if next_href:
                next_href = next_href.strip()
                if not next_href:
                    print("Next href is empty. Stopping pagination.")
                    break

                next_url = urljoin(url, next_href)
                print(f"Navigating to next page: {next_url}")
                try:
                    driver.get(next_url)
                    time.sleep(3)
                except Exception as e:
                    print(f"Failed to load {next_url}: {e}")
                    failed_pages_count += 1
                    if failed_pages_count >= max_failed_pages:
                        print("Max failed pages limit reached.")
                        break
                    continue

            else:
                # If there's no href, try to click directly
                print("No 'href' found. Attempting to click the element.")
                try:
                    driver.execute_script("arguments[0].click();", next_button_element)
                    time.sleep(3)
                except Exception as e:
                    print(f"Could not click next button: {e}")
                    failed_pages_count += 1
                    if failed_pages_count >= max_failed_pages:
                        print("Max failed pages limit reached.")
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
