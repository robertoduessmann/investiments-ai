# Investiments AI

This project provides a REST API that recommends Exchange-Traded Funds (ETFs) based on the user's specified risk level (`high`, `medium`, or `low`). It fetches ETF data from the iShares API, processes the data to rank ETFs by net assets, and integrates the **ChatGPT API** to enhance recommendations with intelligent insights.

---

## Features

- **Dynamic Data Fetching**: Extracts live ETF data (ticker, name, net assets) from the iShares API.
- **Net Asset Ranking**: Sorts ETFs by net assets and retrieves the top 60.
- **Risk-Based Recommendations**: Provides tailored ETF suggestions for different risk levels.
- **ChatGPT Integration**: Uses OpenAI's ChatGPT API to generate insightful ETF recommendations.
- **REST API**: Accessible API endpoint for fetching recommendations.

---

## Technologies Used

- **Python**: Core programming language.
- **Flask**: REST API framework.
- **OpenAI API**: Provides intelligent insights and recommendations.
- **Requests**: For making HTTP requests to the iShares API.

---

## Prerequisites

1. **Python**: Version 3.7 or later.
2. **OpenAI API Key**: Obtain your key from the [OpenAI API](https://platform.openai.com/).

---

## Installation

### 1. Clone the Repository

### 2. Install Dependencies
```bash
pip install -r requirements.txt
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
"recommendations": [
    {
    "name": "IVV: iShares Core S&P 500 ETF",
    "allocation": "40%"
    },
    {
    "name": "IWF: iShares Russell 1000 Growth ETF",
    "allocation": "30%"
    },
    {
    "name": "IEMG: iShares Core MSCI Emerging Markets ETF",
    "allocation": "30%"
    }
]
}
```