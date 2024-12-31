# Investiments AI

This project provides a REST API that recommends Exchange-Traded Funds (ETFs) based on the user's specified risk level (`high`, `medium`, or `low`). It uses **Selenium** for web scraping to dynamically extract ETF data from the iShares website and integrates the **ChatGPT API** to enhance recommendations with intelligent insights.

---

## Features

- **Dynamic Web Scraping**: Extracts live ETF data (ticker, name, net assets) from the iShares website.
- **Risk-Based Recommendations**: Provides tailored ETF suggestions for different risk levels.
- **ChatGPT Integration**: Uses OpenAI's ChatGPT API to generate insightful ETF recommendations.
- **REST API**: Accessible API endpoint for fetching recommendations.

---

## Technologies Used

- **Python**: Core programming language.
- **Flask**: REST API framework.
- **Selenium**: Web scraping tool for dynamic content.
- **OpenAI API**: Provides intelligent insights and recommendations.
- **Chromedriver**: Required for Selenium to interact with Chrome.

---

## Prerequisites

1. **Python**: Version 3.7 or later.
2. **Google Chrome**: Installed and updated.
3. **Chromedriver**: Matching version of Chromedriver for your Chrome browser.
4. **OpenAI API Key**: Obtain your key from the [OpenAI API](https://platform.openai.com/).

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/etf-recommendation-api.git
cd etf-recommendation-api
```

### 2. Install Dependencies
```bash
pip install flask selenium openai
```

### 3. Set Up Chromedriver
1. Download Chromedriver from [here](https://chromedriver.chromium.org/downloads).
2. Place it in a directory (e.g., `/usr/local/bin` or `C:\chromedriver\`).
3. Ensure the path in the code matches the location of your Chromedriver.

### 4. Set Up OpenAI API Key
Replace `your_openai_api_key_here` in the script with your OpenAI API key:
```python
openai.api_key = "your_openai_api_key_here"
```
Alternatively, set the key as an environment variable:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

---

## Usage

### Start the API
Run the Flask app:
```bash
python etf_recommendation.py
```
The server will start at:
```
http://127.0.0.1:5000/
```

### API Endpoint

#### **GET /recommend_etfs**
Fetch ETF recommendations based on risk level.

##### **Query Parameters**
- **`risk_level`** (required): Specifies the risk level (`high`, `medium`, or `low`).

##### **Example Request**
```bash
curl "http://127.0.0.1:5000/recommend_etfs?risk_level=medium"
```

##### **Example Response**
```json
{
    "recommendations": "1. IVV: iShares Core S&P 500 ETF (Net Assets: $35000000000) - Suitable for medium risk due to large-cap stability.\n\n2. IEMG: iShares Core MSCI Emerging Markets ETF (Net Assets: $27000000000) - Offers exposure to high-growth emerging markets, which are inherently risky.\n\n3. IWM: iShares Russell 2000 ETF (Net Assets: $15000000000) - Focuses on small-cap stocks, which tend to be more volatile."
}
```
