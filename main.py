from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
chrome_options = Options()

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def main():
    driver.get("https://www.tines.com/library/tools/")
    
    try:
        # Wait for the table body to be visible
        wait = WebDriverWait(driver, 15)
        tbody = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[1]/table/tbody')))

        # Click the pagination dropdown
        pagination_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pagination-per-page"]/option[5]')))
        pagination_dropdown.click()

        # Wait for the new table data to load
        wait.until(EC.staleness_of(tbody))  # Ensures the old tbody is stale
        tbody = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div[1]/div/div/div[2]/div/div[2]/div/div[1]/table/tbody')))

        # Extract data
        tools_data = []
        rows = tbody.find_elements(By.CSS_SELECTOR, 'tr')
        for row in rows:
            tool_name = row.find_element(By.CSS_SELECTOR, 'th a').text
            num_stories = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            tools_data.append([tool_name, num_stories])
        # print(tools_data,end='\n')

        # Write data to a CSV file
        with open('tools_data.csv', 'w') as f:
            f.write('Tool Name,Number of Stories\n')
            for tool in tools_data:
                f.write(f'{tool[0]},{tool[1]}\n')

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == '__main__':
    main()
