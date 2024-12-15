import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up Selenium WebDriver
service = Service("/usr/local/bin/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Headless mode for better performance
driver = webdriver.Chrome(service=service, options=options)

# API Configuration (Replace with actual API endpoint and key)
API_ENDPOINT = "https://api.perplexity.ai/query"
API_KEY = "your_api_key_here"  # Replace with your API key

# URL of the iShares ETF page
url = "https://www.ishares.com/us/products/etf-investments#/?productView=etf&pageNumber=1&sortColumn=totalNetAssets&sortDirection=desc&dataView=keyFacts&showAll=true"

# Function to call Perplexity or an AI API
def get_api_insight(ticker, name):
    try:
        # Prepare query payload
        query = f"Provide a financial summary and analysis for ETF {ticker} ({name})."
        headers = {"Authorization": f"Bearer {API_KEY}"}
        payload = {"query": query}
        
        # Call the API
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant information from the response
        return data.get("summary", "No summary available.")
    except Exception as e:
        return f"Error fetching insights: {e}"

# Wait for the table to load and scrape data
try:
    driver.get(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-table-wrapper"))
    )

    # Find the table rows
    rows = driver.find_elements(By.CSS_SELECTOR, ".product-table-wrapper table tbody tr")

    # Extract the required data
    etf_data = []
    for row in rows:
        # Get the columns in each row
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 0:
            ticker = cols[0].text.strip()
            name = cols[1].text.strip()
            net_assets = cols[4].text.strip()  # Adjust index based on column order
            yield_12m = cols[7].text.strip()  # Adjust index based on column order

            # Fetch additional insights using the API
            insights = get_api_insight(ticker, name)

            # Append the data
            etf_data.append({
                "Ticker": ticker,
                "Name": name,
                "Net Assets (USD)": net_assets,
                "12m Yield Return (%)": yield_12m,
                "Insights": insights
            })

    # Convert to a DataFrame
    df = pd.DataFrame(etf_data)

    # Save to CSV
    df.to_csv("ishares_etfs_with_insights.csv", index=False)
    print("Scraping and API calls complete. Data saved to 'ishares_etfs_with_insights.csv'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
