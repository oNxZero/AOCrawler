import os
import requests
import hashlib
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import time
from colorama import Fore, Style

# Global counters for statistics
total_downloaded_urls = 0
total_skipped_urls = 0

# Function to read config from a .txt


def read_config(config_path):
    config = {}
    with open(config_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config


# Function to read URLs from url.txt


def read_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

# Function to ensure the directory exists


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download images and save them if not duplicate


def download_image(url, folder_path, seen_hashes):
    global total_downloaded_urls, total_skipped_urls  # Access global statistics counters

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        img = Image.open(BytesIO(response.content))
        img_hash = hashlib.md5(response.content).hexdigest()

        if img_hash not in seen_hashes:
            seen_hashes.add(img_hash)
            img_format = img.format.lower()
            img_filename = os.path.join(folder_path, f"{img_hash}.{img_format}")
            img.save(img_filename)
            print(f"{Fore.GREEN}Downloaded: {img_filename}{Fore.RESET}")
            total_downloaded_urls += 1
        else:
            print(f"{Fore.YELLOW}Duplicate found, skipping: {url}{Fore.RESET}")
            total_skipped_urls += 1
    except requests.exceptions.RequestException as req_err:
        print(f"{Fore.RED}Request failed for {url}: {req_err}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Failed to download {url}: {e}{Fore.RESET}")

# URL validation function


def is_valid_url(url):
    url_regex = re.compile(
        r'^(https?://)?(www\.)?albiononline\.com/characterbuilder/solo-builds/view/[0-9]+$', re.IGNORECASE)
    return re.match(url_regex, url)

# Web crawler to extract lazy-loaded images


def crawl_and_download_images(url, base_folder_path):
    # Read configuration
    config = read_config(os.path.join(base_folder_path, 'config.txt'))
    chrome_driver_path = os.path.join(base_folder_path, config['CHROME_DRIVER_PATH'])

    # Set dynamic folder name based on the last segment of the URL ex. ./view/*5345*
    dynamic_folder_name = url.split('/')[-1]
    output_folder = os.path.join(base_folder_path, 'Images',
                                 dynamic_folder_name)  # Save to Images/{dynamic_folder_name}

    # Set up Chrome options
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Uncomment if you want headless mode
    chrome_options.add_argument("--disable-gpu")

    # Launch Selenium with ChromeDriver
    print(f"{Fore.YELLOW}Launching the browser...{Fore.RESET}")
    browser = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    # Load the page
    try:
        print(f"{Fore.YELLOW}Loading the page...{Fore.RESET}")
        browser.get(url)

        WebDriverWait(browser, 20).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "items-browser__abilities-main-image"))
        )

        print(f"{Fore.YELLOW}Page loaded, scrolling to load images...{Fore.RESET}")
        # Scroll to the bottom of the page to load images
        for i in range(5):  # Increase range if it doesn't load
            print(f"{Fore.YELLOW}Scrolling... ({i + 1}/5){Fore.RESET}")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        print(f"{Fore.GREEN}Page is ready for processing.{Fore.RESET}")
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        image_tags = soup.find_all('img')

        # Debugging output for image tags
        print(f"{Fore.GREEN}Found {len(image_tags)} image tags on the page.{Fore.RESET}")

        if not image_tags:
            print(f"{Fore.RED}No image tags found on the page.{Fore.RESET}")
            return

        # Ensure output folder exists
        ensure_directory(output_folder)

        # Track image hashes
        seen_hashes = set()

        for img_tag in image_tags:
            img_url = img_tag.get('src')

            if img_url and img_url.startswith("https://render.albiononline.com"):
                if "v1/item" in img_url:
                    folder_path = os.path.join(output_folder, "Build")
                    ensure_directory(folder_path)
                    print(f"{Fore.CYAN}Processing item image: {img_url}{Fore.RESET}")
                    download_image(img_url, folder_path, seen_hashes)
                elif "v1/spell" in img_url:
                    folder_path = os.path.join(output_folder, "Abilities")
                    ensure_directory(folder_path)
                    print(f"{Fore.CYAN}Processing spell image: {img_url}{Fore.RESET}")
                    download_image(img_url, folder_path, seen_hashes)
                else:
                    print(f"{Fore.RED}No valid URL found for an image tag: {img_url}{Fore.RESET}")
            else:
                pass
                # print(f"{Fore.RED}Skipping invalid image URL: {img_url}{Fore.RESET}")

        print(f"{Fore.GREEN}Processing complete for {url}!{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.RED}An error occurred while processing the page: {e}{Fore.RESET}")
    finally:
        print(f"{Fore.YELLOW}Closing the browser...{Fore.RESET}")
        browser.quit()


if __name__ == "__main__":
    base_folder_path = os.getcwd()  # Use current directory

    # Read the URLs from url.txt
    urls = read_urls_from_file(os.path.join(base_folder_path, 'url.txt'))

    # Initialize statistics counters
    if urls:
        print(f"{Fore.GREEN}Found {len(urls)} URLs to process.{Fore.RESET}")
        for website_url in urls:
            if is_valid_url(website_url):
                print(f"{Fore.GREEN}Starting the crawler for URL: {website_url}{Fore.RESET}")
                crawl_and_download_images(website_url, base_folder_path)

    # Final statistics after all URLs have been processed
        print(f"{Fore.GREEN}Successfully Downloaded {total_downloaded_urls} Images{Fore.RESET}")
        print(f"{Fore.GREEN}Skipped {total_skipped_urls} Images{Fore.RESET}")

    # Check if no URLs were found
    if not urls:
        print(f"{Fore.RED}No valid URLs found in url.txt.{Fore.RESET}")
