from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import re
import time

# Set up Selenium with Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: runs in headless mode

# Initialize the WebDriver with the correct path to ChromeDriver
service = Service(executable_path="chromedriver.exe")  # Ensure correct path
driver = webdriver.Chrome(service=service, options=chrome_options)

# URLs to scrape
urls = [
    "https://www.eventbrite.ca/d/canada--kingston/free--business--events/?page=1",
    "https://www.eventbrite.ca/d/canada--kingston/free--events/?subcategories=1001&page=1"
]

# Set to track unique event names
unique_event_titles = set()

# CSS selector to find sections with Kingston, ON
css_selector = 'section.event-card-actions.DiscoverHorizontalEventCard-module__actions___3DGie[data-event-location="Kingston, ON"]'

# Iterate through each URL to scrape event titles
for url in urls:
    driver.get(url)
    time.sleep(5)  # Allow time for content to load

    # Find elements using the CSS selector
    matching_elements = driver.find_elements(By.CSS_SELECTOR, css_selector)

    if matching_elements:
        for element in matching_elements:
            # Extract event title
            outer_html = element.get_attribute("outerHTML")
            match = re.search(r"Save this event: ([a-zA-Z ]+)", outer_html)

            if match:
                event_name = match.group(1).strip()  # Extract and clean whitespace
                # Check for duplicates using the set
                if event_name not in unique_event_titles:
                    unique_event_titles.add(event_name)  # Add to set if unique
    else:
        print(f"No sections with Kingston, ON found at {url}.")

# Convert set to list of dictionaries with a "title" key
event_names = [{"title": title} for title in unique_event_titles]

# Save event names to a JSON file in the desired format
with open("event_names.json", "w") as f:
    json.dump(event_names, f, indent=2)  # Proper JSON format with indentation

print("Event names saved to event_names.json.")

# Close the browser
driver.quit()
