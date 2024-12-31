from flask import Flask, request, jsonify
import requests
from openai import OpenAI


# OpenAI API Configuration
OPENAI_API_KEY = "bla"  # Replace with your OpenAI API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask App
app = Flask(__name__)

# URL of iShares ETF page
ISHARES_URL = "https://www.ishares.com/us/product-screener/product-screener-v3.1.jsn?type=excel&siteEntryPassthrough=true&dcrPath=/templatedata/config/product-screener-v3/data/en/us-ishares/ishares-product-screener-excel-config&disclosureContentDcrPath=/templatedata/content/article/data/en/us-ishares/DEFAULT/product-screener-all-disclaimer"

def scrape_etf_data():
    try:
        # Fetch the file
        response = requests.get(ISHARES_URL)
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        # Parse JSON data
        data = response.json()

        # Extract relevant details
        etf_list = []
        for key, value in data.items():
            # Check if the value contains required keys
            if isinstance(value, dict):
                name = value.get("fundName")
                net_assets = value.get("totalNetAssets", {}).get("d", "N/A")
                ticker = value.get("localExchangeTicker")

                if name and ticker:  # Ensure the required fields are present
                    etf_list.append({"Name": name, "Net Assets (USD)": net_assets, "Ticker": ticker})

        # Print or process the list of ETFs
        for etf in etf_list:
            print(etf)
        return etf_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the data: {e}")
        return []


def get_chatgpt_recommendations(etfs, risk_level):
    """Fetches ETF recommendations from ChatGPT based on risk level."""
    try:
        # print("data: " + etfs)
        # Prepare the input prompt
        etf_list = "\n".join([f"{etf['Ticker']}: {etf['Name']} (Net Assets: ${etf['Net Assets (USD)']})" for etf in etfs])
        print("data: " + etf_list)
    
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