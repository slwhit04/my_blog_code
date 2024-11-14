from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the website
driver.get("https://www.akc.org/dog-breeds/")

# Function to close overlay if it appears
def close_overlay():
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_button.click()
        time.sleep(1)  # Brief wait to ensure overlay closes
    except:
        driver.execute_script("document.getElementById('onetrust-policy').style.display = 'none';")

# Close any overlay that might block elements
close_overlay()

# List to store data for each breed
breed_data = []

# Loop through all breed links
try:
    while True:
        # Re-find all breed links on the main page to prevent stale element issues
        breed_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.breed-type-card a"))
        )

        # Loop over each breed link and fetch data
        for i in range(len(breed_links)):
            try:
                # Refresh breed links each time to avoid stale elements after navigation
                breed_links = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.breed-type-card a"))
                )

                # Click breed link with JavaScript to avoid interception
                driver.execute_script("arguments[0].click();", breed_links[i])

                # Wait and scrape breed information
                breed_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                ).text

                # Gather data points
                data = {'Breed': breed_name}

                try:
                    data['Breed Group'] = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[1]/div[1]/div[2]/a").text
                except:
                    data['Breed Group'] = 'Not found'

                try:
                    data['Height'] = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div[2]/div[1]/div/p").text
                except:
                    data['Height'] = 'Not found'

                try:
                    data['Weight'] = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div[2]/div[2]/div/p").text
                except:
                    data['Weight'] = 'Not found'

                try:
                    data['Life Expectancy'] = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div[2]/div[3]/div/p").text
                except:
                    data['Life Expectancy'] = 'Not found'

                # Add this breed's data to the list
                breed_data.append(data)
                print(data)

                # Go back to the list of breeds
                driver.back()
                time.sleep(1)

            except IndexError:
                # Handle case where breed_links[i] is out of range
                print(f"Index out of range for breed index {i}. Refreshing breed links.")
                breed_links = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.breed-type-card a"))
                )
                continue  # Retry with refreshed breed_links list

        # Check if there is a "Load More" button to click
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='load-more-btn']"))
            )
            load_more_button.click()
            time.sleep(2)  # Wait for new breeds to load
        except:
            # Break the loop if the "Load More" button is not found (end of pages)
            break

finally:
    # Close the browser
    driver.quit()

# Save data to CSV
breed_df = pd.DataFrame(breed_data)
breed_df.to_csv("breed_data.csv", index=False)

print("Data saved to breed_data.csv")
