from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.imdb.com/chart/top/")
print(driver.page_source[:1000])  # print first 1000 chars of HTML
driver.quit()
