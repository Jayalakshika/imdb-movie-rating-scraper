from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

def scrape_imdb_top250():
    options = webdriver.ChromeOptions()

    # Make Selenium look like a normal user
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36")

    # DO NOT USE HEADLESS (IMDB blocks it)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.imdb.com/chart/top/"
    driver.get(url)
    time.sleep(4)

    # Scroll to load full list
    driver.execute_script("window.scrollTo(0, 300);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    # Correct selector for 2025 IMDb website
    movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

    print("Movies found:", len(movies))  # DEBUG

    movie_list = []

    for index, movie in enumerate(movies, start=1):
        try:
            title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
        except:
            title = "N/A"

        try:
            year = movie.find_element(By.CSS_SELECTOR, "span.cli-title-metadata-item").text
        except:
            year = "N/A"

        try:
            rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
        except:
            rating = "N/A"

        movie_list.append({
            "Rank": index,
            "Title": title,
            "Year": year,
            "IMDb Rating": rating
        })

    driver.quit()

    print("Total scraped:", len(movie_list))

    df = pd.DataFrame(movie_list)
    df.to_csv("imdb_top250.csv", index=False, encoding="utf-8")

    print("CSV saved at:", os.path.abspath("imdb_top250.csv"))


