import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless=new")  # If you don't want a chrome window to open, Use the new headless mode
# chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

TOOLS_URL = "https://www.tines.com/library/tools"
STORIES_URL = "https://www.tines.com/library?view=all"
DATA_DIR = "data"

# data directory
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_tools():
    """Scrapes tool names and the number of stories for each tool, saves them to tools_data.csv"""
    driver.get(TOOLS_URL)
    time.sleep(3)  # Wait for some time for the webpage to get loaded with contents

    try:
        # Click "Show All" in pagination
        pagination_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pagination-per-page"]/option[last()]')))
        pagination_dropdown.click()
        time.sleep(3)  # Wait for page refresh after clicking the button

        print("Task-1 : Writing the data to tools_data.csv")

        # Locate tools table
        tools_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody")))
        rows = tools_table.find_elements(By.CSS_SELECTOR, "tr")

        tools_data = []
        for row in rows:
            try:
                tool_name = row.find_element(By.CSS_SELECTOR, "th a").text.strip()
                tool_link = row.find_element(By.CSS_SELECTOR, "th a").get_attribute("href").strip()
                num_stories = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
                
                tools_data.append([tool_name, num_stories, tool_link])
                print(tool_name, num_stories, tool_link, end="\n")
            except Exception:
                continue  # Skip row if any error occurs

        # Save to CSV
        with open(f"{DATA_DIR}/tools_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tool Name", "Number of Stories", "Tool Link"])  # CSV Header
            writer.writerows(tools_data)

        print("Tools data saved to tools_data.csv")

    except Exception as e:
        print(f"Error in fetch_tools(): {e}")

def fetch_tool_stories():
    """Fetches stories from each tool's page and saves them to stories_data.csv"""
    input_file = f"{DATA_DIR}/tools_data.csv"
    output_file = f"{DATA_DIR}/stories_data.csv"

    if not os.path.exists(input_file):
        print("tools_data.csv not found. Run fetch_tools() first.")
        return

    try:
        print("Task-2 : Writing the data to stories_data.csv")
        # Read tool names
        with open(input_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            tools = [(row[0], row[2]) for row in reader]  # Extract tool names and links

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tool Name", "Story", "Works with", "No. of Actions", "Author"])  # CSV Header
            for tool_name, tool_link in tools:
                tool_url = tool_link
                driver.get(tool_url)
                print(tool_name)
                print(tool_url)
                time.sleep(3)  # Allow time to load

                try:
                    pagination_elements = driver.find_elements(By.XPATH, '//*[@id="pagination-per-page"]/option[last()]')

                    if pagination_elements:  # If pagination exists
                        pagination_dropdown = pagination_elements[0]
                        pagination_dropdown.click()
                        time.sleep(3)  # Wait for reload
                        # Locate stories table
                        stories_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody")))
                        rows = stories_table.find_elements(By.CSS_SELECTOR, "tr")

                        for row in rows:
                            # print(row.get_attribute("outerHTML"))
                            try:
                                story_name = row.find_element(By.CSS_SELECTOR, "th a").text.strip()
                                parent = row.find_element(By.CSS_SELECTOR, "table tbody tr td a")
                                # Find the correct 'td' that contains taaq09w
                                parent_td = row.find_element(By.CLASS_NAME, "lnfq6m")

                                # Extract all elements with class "taaq09w" inside the td
                                div_elements = parent_td.find_elements(By.CLASS_NAME, "taaq09w")
                                # print(div_elements)
                                
                                works_with = []
                                
                                # Iterate through all found div elements
                                for div_element in div_elements:                        
                                    # print("Element: ", div_element)
                                    # Locate the <span> inside each div
                                    span_element = div_element.find_element(By.TAG_NAME, "span")
                                    # print("Div HTML:", div_element.get_attribute("outerHTML")) 
                                    text = driver.execute_script("return arguments[0].textContent;", span_element)
                                    # print("Extracted Text (JS):", text)                   
                                    works_with.append(text)    
                                    # Print extracted text
                                    # print(f"Story: {story_name}, Extracted Text: {span_element.text}")
                            
                                # Extract and print the text inside the <span>
                                # print("Extracted Text:", span_element.text)
                                num_actions = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()
                                
                                # print(num_actions)
                                author = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
                                print(tool_name,story_name, works_with, num_actions, author, end="\n")
                                writer.writerow([tool_name, story_name, works_with, num_actions, author])

                            except Exception:
                                continue  # Skip row if error occurs
                
                    else:
                        print(f"No pagination found for {tool_name}, proceeding without it.")
                        stories_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody")))
                        rows = stories_table.find_elements(By.CSS_SELECTOR, "tr")

                        for row in rows:
                            try:
                                story_name = row.find_element(By.CSS_SELECTOR, "th a").text.strip()
                                parent = row.find_element(By.CSS_SELECTOR, "table tbody tr td a")
                                # Find the correct 'td' that contains taaq09w
                                parent_td = row.find_element(By.CLASS_NAME, "lnfq6m")

                                # Extract all elements with class "taaq09w" inside the td
                                div_elements = parent_td.find_elements(By.CLASS_NAME, "taaq09w")
                                # print(div_elements)
                                
                                works_with = []
                                
                                # Iterate through all found div elements
                                for div_element in div_elements:                        
                                    # print("Element: ", div_element)
                                    # Locate the <span> inside each div
                                    span_element = div_element.find_element(By.TAG_NAME, "span")
                                    # print("Div HTML:", div_element.get_attribute("outerHTML"))
                                    text = driver.execute_script("return arguments[0].textContent;", span_element)
                                    # print("Extracted Text (JS):", text)
                                    works_with.append(text)
                                    # Print extracted text
                                    # print(f"Story: {story_name}, Extracted Text: {span_element.text}")
                                num_actions = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()
                                author = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
                                print(tool_name,story_name, works_with, num_actions, author, end="\n")
                                writer.writerow([tool_name, story_name, works_with, num_actions, author])
                            except Exception:
                                continue
                except Exception as e:
                    print(f"Error extracting stories for {tool_name}: {e}")
        print("Stories data saved to stories_data.csv")
    except Exception as e:
        print(f"Error in fetch_tool_stories(): {e}")

def fetch_all_stories():
    """Scrapes all stories from the main library page and saves them to all_stories.csv"""
    driver.get(STORIES_URL)
    time.sleep(3)

    output_file = f"{DATA_DIR}/all_stories.csv"

    try:
        print("Task-3 : Writing the data to all_stories.csv")
        # Click "Show All" in pagination
        pagination_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pagination-per-page"]/option[last()]')))
        pagination_dropdown.click()
        time.sleep(3)  # Wait for reload

        # Locate stories table
        stories_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody")))
        rows = stories_table.find_elements(By.CSS_SELECTOR, "tr")

        with open(output_file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Story", "Works with", "No. of Actions", "Author"])
            i =0 
            for row in rows:
                try:
                    story_name = row.find_element(By.CSS_SELECTOR, "table tbody tr th a").text.strip()         
                    parent = row.find_element(By.CSS_SELECTOR, "table tbody tr td a")
                    
                    # Find the correct 'td' that contains taaq09w
                    parent_td = row.find_element(By.CLASS_NAME, "lnfq6m")

                    # Extract all elements with class "taaq09w" inside the td
                    div_elements = parent_td.find_elements(By.CLASS_NAME, "taaq09w")
                    # print(div_elements)
                    
                    works_with = []
                    
                    # Iterate through all found div elements
                    for div_element in div_elements:                        
                        # print("Element: ", div_element)
                        # Locate the <span> inside each div
                        span_element = div_element.find_element(By.TAG_NAME, "span")
                        # print("Div HTML:", div_element.get_attribute("outerHTML")) 
                        text = driver.execute_script("return arguments[0].textContent;", span_element)
                        # print("Extracted Text (JS):", text)                   
                        works_with.append(text)    
                        # Print extracted text
                        # print(f"Story: {story_name}, Extracted Text: {span_element.text}")
                    num_actions = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()
                    author = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
                    print(story_name, works_with, num_actions, author, end="\n")
                    writer.writerow([story_name, works_with, num_actions, author])

                except Exception:
                    continue  # Skip row if error occurs
                # i += 1
                # if (i ==1):
                #     break
        print("All stories data saved to all_stories.csv")

    except Exception as e:
        print(f"Error in fetch_all_stories(): {e}")

def main():
    fetch_tools()         # Task 1: Scrape tools and their number of stories
    fetch_tool_stories()  # Task 2: Scrape stories under each tool
    fetch_all_stories()   # Task 3: Scrape all stories from library page
    driver.quit()

if __name__ == '__main__':
    main()
