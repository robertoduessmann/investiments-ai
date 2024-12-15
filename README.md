# Investiments AI

This project is a Python-based web scraper designed to extract ETF data from the iShares website. It uses Selenium for dynamic content rendering and includes an API integration to fetch insights for the scraped ETFs.

```

## Requirements
- Python 3.9 or later
- Google Chrome and ChromeDriver
- Docker (for containerized deployment)

## Setup and Usage

### 1. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 2. Run the Scraper
Run the scraper directly with Python:
```bash
python scraper.py
```

The output will be saved as `ishares_etfs_with_insights.csv` in the project directory.

### 3. Run with Docker
Build and run the scraper in a Docker container:

#### Build the Docker Image
```bash
docker build -t scraper-image .
```

#### Run the Container
```bash
docker run --rm -v $(pwd):/app scraper-image
```

### 4. Configure the API Integration
To fetch additional insights for ETFs:
1. Replace `your_api_key_here` in `scraper.py` with your API key.
2. Update the `API_ENDPOINT` variable with the appropriate endpoint.

## Output
The scraped data is saved to a CSV file with the following columns:
- **Ticker**: The ETF ticker symbol.
- **Name**: The name of the ETF.
- **Net Assets (USD)**: The total net assets under management.
- **12m Yield Return (%)**: The 12-month trailing yield.
- **Insights**: Additional insights fetched from the API.

## Notes
- Ensure ChromeDriver is installed and matches your Chrome version.
- Comply with the website's Terms of Service before scraping.
- Handle API rate limits and errors gracefully.

## License
This project is open-source and free to use. Ensure you comply with all relevant legal and ethical guidelines when using this scraper.
