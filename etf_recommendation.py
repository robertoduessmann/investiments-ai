from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import openai
from openai import OpenAI
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# OpenAI API Configuration
OPENAI_API_KEY = "bla"  # Replace with your OpenAI API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask App
app = Flask(__name__)

# Selenium WebDriver Setup
service = Service("/usr/local/bin/chromedriver")  # Adjust path to your chromedriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode

# URL of iShares ETF page
ISHARES_URL = "https://www.ishares.com/us/products/etf-investments#/?productView=etf&pageNumber=1&sortColumn=totalNetAssets&sortDirection=desc&dataView=keyFacts&showAll=true"

def scrape_etf_data():
    """Scrapes ETF data from iShares website."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = webdriver.chrome.service.Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    etf_data = []
    try:
        driver.get(ISHARES_URL)
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".mat-table cdk-table ishares-theme grid-margin-as-padding"))
        )
        rows = driver.find_elements(By.CSS_SELECTOR, ".mat-table cdk-table ishares-theme grid-margin-as-padding")
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 0:
                ticker = cols[0].text.strip()
                name = cols[1].text.strip()
                net_assets = cols[4].text.strip()  # Adjust index if necessary
                etf_data.append({
                    "Ticker": ticker,
                    "Name": name,
                    "Net Assets (USD)": net_assets.replace(",", "").replace("$", "")
                })
    except TimeoutException:
        print("Timeout while waiting for the table to load.")
    finally:
        driver.quit()
    return etf_data

def get_chatgpt_recommendations(etfs, risk_level):
    """Fetches ETF recommendations from ChatGPT based on risk level."""
    try:
        # Prepare the input prompt
        etf_list = "\n".join([f"{etf['Ticker']}: {etf['Name']} (Net Assets: ${etf['Net Assets (USD)']})" for etf in etfs])
        prompt = (
            f"Based on the following list of ETFs:\n\n{etf_list}\n\n"
            f"Recommend three ETFs suitable for a {risk_level} risk level, ordered by net assets. "
            "Provide a brief explanation for each recommendation."
        )

        # Call ChatGPT API
        response = client.chat.completionss.create(model="gpt-4",  # Use gpt-4 for better performance
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500)

        # Extract and return recommendations
        recommendations = response.choices[0].message.content

        return recommendations
    except Exception as e:
        return f"Error fetching insights: {e}"

@app.route('/recommend_etfs', methods=['GET'])
def api_recommend_etfs():
    """API endpoint to recommend ETFs based on risk level using ChatGPT."""
    risk_level = request.args.get('risk_level', '').lower()
    if risk_level not in ["high", "medium", "low"]:
        return jsonify({"error": "Invalid risk level. Choose from 'high', 'medium', or 'low'."}), 400
    
    # Scrape data
    etf_data = scrape_etf_data()
    
    # Prepare ETF list for ChatGPT
    recommended_etfs = get_chatgpt_recommendations(etf_data, risk_level)
    return jsonify({"recommendations": recommended_etfs})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6001)