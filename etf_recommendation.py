from flask import Flask, request, jsonify
import requests
from openai import OpenAI

# OpenAI API Configuration
OPENAI_API_KEY = "xxx"  # Replace with your OpenAI API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask App
app = Flask(__name__)

# URL of iShares ETF page
ISHARES_URL = "https://www.ishares.com/us/products/etf-investments#/?productView=etf&pageNumber=1&sortColumn=totalNetAssets&sortDirection=desc&dataView=keyFacts&showAll=true"

def get_chatgpt_recommendations(risk_level):
    """Fetches ETF recommendations from ChatGPT based on risk level."""
    try:
        # Prepare the input prompt
        prompt = (
            f"Scrapes ETF data from iShares website: Ticker, Name, and Net Asset USD:{ISHARES_URL}\n\n"
            f"Recommend three ETFs suitable for a {risk_level} risk level, ordered by net assets. "
            "Provide a brief explanation for each recommendation."
        )

        # Call ChatGPT API
        response = client.chat.completions.create(model="gpt-4",  # Use gpt-4 for better performance
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

    # Prepare ETF list for ChatGPT
    recommended_etfs = get_chatgpt_recommendations(risk_level)
    return jsonify({"recommendations": recommended_etfs})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6001)