from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://developer.apple.com/documentation/visionos"

# Use Selenium to get the page
driver.get(url)

# Wait for JavaScript to load
time.sleep(5)  # Adjust time as necessary based on your observation of how long the page takes to load

# Now you can parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Example: Find and print all section titles - adjust the selector as necessary
for section in soup.find_all('h1'):  # This is a placeholder; adjust your selector based on actual content
    print(section.text.strip())

# Clean up: Close the browser window
driver.quit()


# Assuming 'soup' is the BeautifulSoup object containing the page source
base_url = "https://developer.apple.com"

# Find all <a> tags
links = soup.find_all('a', href=True)

# Filter out and build full URLs
doc_urls = []
for link in links:
    href = link['href']
    # Check if the link is a relative path to documentation
    if href.startswith("/documentation/visionos"):
        full_url = base_url + href
        doc_urls.append(full_url)

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
"""
# Data structure to hold all documents
documents = []

for url in doc_urls:
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)
    
    # Parse the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extract the title (assuming it's in a <title> or similar tag)
    title = soup.find('title').text.strip()
    
    # Initialize content and code_examples lists
    content = []
    code_examples = []

    # Extract textual content (adjust selector as needed)
    content_sections = soup.find_all(['p', 'li'])  # Simplified example
    for section in content_sections:
        content.append(section.text.strip())
    
    # Extract code (assuming code is directly within <pre><code> tags)
    code_sections = soup.find_all('pre')
    for code_section in code_sections:
        code_examples.append(code_section.text.strip())

    # Compile document data
    document = {
        "url": url,
        "title": title,
        "content": " ".join(content),  # Joining paragraphs for simplicity
        "code_examples": code_examples
    }
    
    # Add to documents list
    documents.append(document)"""


# Function to wait for the presence of code sections and then extract content
def extract_content_and_code(url):
    driver.get(url)
    try:
        # Wait for the page to be loaded
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        print(f"Timed out waiting for page to load: {url}")
        return {"url": url, "title": "", "content": []}
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.find('title').text.strip() if soup.find('title') else ""
    
        # Collecting all paragraphs and code blocks
    elements = soup.find_all(['p', 'li', 'pre'])
    content = []

    for element in elements:
        if element.name in ['p', 'li']:
            content.append(element.get_text().strip())
        elif element.name == 'pre':
            # Extracting text directly from <pre> or its child <code>
            code_text = element.get_text().strip()
            content.append(code_text)

    # Combine all paragraphs and code blocks into a single string
    content = "\n".join(content)
    
    
    document = {
        "url": url,
        "title": title,
        "content": content,
    }
        
    return document


documents = [extract_content_and_code(url) for url in doc_urls]


# Quit the driver session
driver.quit()

# Prepare data for JSON output
data_to_save = {"documents": documents}

# Save data to a JSON file
with open('scraped_docs.json', 'w', encoding='utf-8') as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

# Indicate completion
print("Data saved to scraped_docs.json")
