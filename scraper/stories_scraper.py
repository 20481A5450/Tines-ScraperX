import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd

TOOLS_CSV = "data/tools.csv"
OUTPUT_FILE = "data/tool_stories.csv"
BASE_URL = "https://www.tines.com/library/tools/"

def scrape_tool_stories():
    # Read tools from CSV
    if not os.path.exists(TOOLS_CSV):
        print("❌ Tools CSV file not found! Run tools_scraper.py first.")
        return
    
    tools_df = pd.read_csv(TOOLS_CSV)
    all_stories = []

    for _, row in tools_df.iterrows():
        tool_name = row["Tool Name"]
        tool_url = BASE_URL + tool_name.lower().replace(" ", "-")  # Adjust as needed
        
        response = requests.get(tool_url)
        if response.status_code != 200:
            print(f"❌ Failed to fetch {tool_name}. Skipping...")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        stories = soup.find_all("div", class_="story-card")  # Adjust selector if necessary
        
        for story in stories:
            story_title = story.find("h3").text.strip() if story.find("h3") else "N/A"
            works_with = story.find("p", class_="works-with").text.strip() if story.find("p", class_="works-with") else "N/A"
            actions = story.find("p", class_="actions").text.strip() if story.find("p", class_="actions") else "N/A"
            author = story.find("p", class_="author").text.strip() if story.find("p", class_="author") else "N/A"

            all_stories.append([tool_name, story_title, works_with, actions, author])

    # Save to CSV
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Tool Name", "Story", "Works with", "No. of actions", "Author"])
        writer.writerows(all_stories)

    print(f"✅ Tool stories data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_tool_stories()
