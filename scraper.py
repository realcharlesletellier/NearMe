import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize WebDriver
service = Service(executable_path="chromedriver.exe") 
driver = webdriver.Chrome(service=service, options=chrome_options)

# URLs to scrape
url = "https://www.eventbrite.ca/d/canada--kingston/free--business--events/?page=1"

driver.get(url)
time.sleep(5)  # Allowing time for content to load

# CSS selectors
event_card_selector = 'a.event-card-link[data-event-location="Kingston, ON"]'  
details_section_selector = 'section.event-card-details'

try:
    event_card_elements = driver.find_elements(By.CSS_SELECTOR, event_card_selector)
    details_section_elements = driver.find_elements(By.CSS_SELECTOR, details_section_selector)

    if not event_card_elements:
        print("No event cards found. Check CSS selector.")
    if not details_section_elements:
        print("No details sections found. Check CSS selector.")

    # Using a Set to track unique event titles (wow CISC 235 coming in handy finally)
    unique_event_titles = set()

    # Unique events stored below
    events = []

    # Extracting event information
    for element in event_card_elements:
        outer_html = element.get_attribute("outerHTML")
        print("Outer HTML:", outer_html)  # Debug print

        # Extract event title
        start = outer_html.find('aria-label="View ') + len('aria-label="View ')
        end = outer_html.find('"', start)  # Find the closing double quote
        event_title = outer_html[start:end]

        # Skip if in set
        if event_title in unique_event_titles:
            continue
        unique_event_titles.add(event_title)

        # Extract event link
        start = outer_html.find('href="') + len('href="')
        end = outer_html.find('"', start)  # Find closing double quote
        event_link = outer_html[start:end]

        # Store event information
        events.append({
            "title": event_title,
            "link": event_link,
            "image": "https://cdn.discordapp.com/attachments/677639135543951440/1231096812794806323/wPgjS3J7QZDdgAAAABJRU5ErkJggg.png?ex=6633bd00&is=66326b80&hm=6f4fdeaae2da24c0b59b24a985d15ab92ecf59ed4fafa76d819de4445ab33ead&",  # my avatar haha
            "date": None,  # Placeholder
            "location": None  # Placeholder
        })

    # Extract event dates and locations
    for section, event in zip(details_section_elements, events):
        outer_html = section.get_attribute("outerHTML")

        # Extract event date
        try:
            start = outer_html.find('<p class="')  # Find the first `<p>` tag
            start = outer_html.find(">", start) + 1  # Move past `>`
            end = outer_html.find("</p>", start)  # Find closing `</p>`
            event_date = outer_html[start:end]
            event["date"] = event_date
        except Exception as e:
            print(f"Error extracting date: {e}")

        # Extract event location
        try:
            # Find the next `<p>` tag after the first one
            start = outer_html.find('<p class="', end)  # Find second `<p>`
            start = outer_html.find(">", start) + 1  # Find `>`
            end = outer_html.find("</p>", start)  # Find closing `</p>`
            event_location = outer_html[start:end]
            event["location"] = event_location
        except Exception as e:
            print(f"Error extracting location: {e}")

    # Write unique events to JSON file
    with open("events.json", "w") as f:
        json.dump(events, f, indent=2)

    print("Unique events saved to events.json.")

except Exception as e:
    print("An error occurred:", e)

driver.quit()
