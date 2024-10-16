from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Open Google Homepage
    driver.get("https://www.google.com")

    # Check if title contains 'Google'
    assert "Google" in driver.title

    # Find the search box and type a query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium Python" + Keys.RETURN)

    # Wait for results to load
    time.sleep(3)

    # Check if results are displayed
    results = driver.find_elements(By.CSS_SELECTOR, "div.g")
    assert len(results) > 0

    print("Test Passed: Search results are displayed")

except Exception as e:
    print(f"Test Failed: {e}")

finally:
    # Close the browser
    driver.quit()
