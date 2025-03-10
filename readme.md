# RD Assignment – Web Scraping Tool

## Overview
This project is a web scraping tool built using Python and Selenium. It scrapes data from the Tines website (https://www.tines.com/library) and performs the following tasks:
1. **Fetch Tools**: Scrapes the list of tools and their number of stories from the Tools page.
2. **Fetch Tool Stories**: For each tool, navigates to the specific tool page and scrapes details for each story.
3. **Fetch All Stories**: Scrapes all stories from the main library page.

## Platform and OS Requirements
- **Operating System**: Windows 10/11, macOS, or Linux.
- **Python Version**: Python 3.8 or higher.
- **Web Browser**: Google Chrome (latest version recommended).
- **ChromeDriver**: Ensure that ChromeDriver is installed and the version matches your installed Google Chrome version. Alternatively, you can use the `webdriver_manager` package to manage the driver automatically.

## Installation
1. **Clone or extract the ZIP file.**
2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate       # On macOS/Linux
   venv\Scripts\activate          # On Windows
3. **Run this command to install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the main script:**
   ```bash
   python main.py
   ```
    **The script will perform all three tasks and save the output CSV files in the data/ directory:**
    1. tools_data.csv
    2. stories_data.csv
    3. all_stories.csv

## Usage
The main script (`main.py`) performs the following tasks:
1. **Fetch Tools**: Scrapes the list of tools and their number of stories from the Tools page.
2. **Fetch Tool Stories**: For each tool, navigates to the specific tool page and scrapes details for each story.
3. **Fetch All Stories**: Scrapes all stories from the main library page.
