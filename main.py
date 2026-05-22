import csv 
import requests 
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time 
import random 

# Businesslist.pk lead scraper 

# Initialize CSV file with headers
with open("leads_businesslist_pk.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Category", "Name", "Address", "Phone"])   
    
categories = ["advertising","consultants", "overseas-business",
              "retail-services", "web-development", ]

base_url = "https://www.businesslist.pk/category/"

ua = UserAgent()
headers = {
    "User-Agent": ua.random
}

for cat in categories:
    print(f"Scraping category: {cat}...")
    cat_url = f"{base_url}/{cat}"

    for page in range(1, 9):  # Scrape first 8 pages
        url = f"{cat_url}/{page}"
        time.sleep(random.uniform(3, 11))
        # Random delay between requests
        print(f"Scraping page {page}...")
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"  # Ensure correct encoding

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.select("div[class^='company']")

    # Use a more specific selector to avoid the 'junk' divs
        cards = soup.find_all("div", class_="company") # Or the specific class you saw for actual listings

        for card in cards:
            # 1. Target ONLY the <a> inside company_header for the name
            # This prevents the Address from leaking into the Name
            name_container = card.find("div", class_="company_header")
            if name_container:
                name_tag = name_container.find("a")
                name = name_tag.get_text(strip=True) if name_tag else "N/A"
            else:
                # Skip this card entirely if it's not a real business card
                continue 

        # 2. Get the Address precisely
            address_tag = card.find("div", class_="address")
            # Some sites put "Address: " text in there, let's strip it
            address_text = address_tag.get_text(strip=True).replace("Address:", "") if address_tag else "N/A"

        # 3. Get the Phone (Using your successful 'span' logic)
            phone_icon = card.find("i", class_="fa-phone")
            phone = phone_icon.find_next_sibling("span").get_text(strip=True) if phone_icon else "N/A"
            # next sibling is used to get the text after the phone icon, which should be the phone number
            
            with open("leads_businesslist_pk.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([cat, name, address_text, phone])
        print(f"Finished scraping page {page}.")
print("Scraping completed. Data saved to leads_businesslist_pk.csv.")
