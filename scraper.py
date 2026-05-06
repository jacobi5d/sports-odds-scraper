import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import pytz

# Target URLs for MLB, NBA, and NHL
URLS = {
    "MLB": "https://madduxsports.com/baseballodds.php",
    "NBA": "https://madduxsports.com/nba-odds.php",
    "NHL": "https://madduxsports.com/nhl-hockey-odds.php"
}

# Standard headers to bypass basic bot-blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

FILE_NAME = "sportdata.json"

def fetch_odds_data(sport, url):
    """Fetches and parses the odds data for a given sport."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # =========================================================
        # HTML PARSING LOGIC GOES HERE
        # Inspect the target website to find the exact table classes or IDs.
        # Example: table = soup.find('table', class_='odds-table')
        # =========================================================
        
        # Temporary placeholder data indicating successful connection
        scraped_games = [{"status": f"Connected to {sport} successfully. Awaiting HTML parsing logic."}] 
        
        return scraped_games

    except Exception as e:
        print(f"Error fetching {sport}: {e}")
        return []

def main():
    # Set time to Eastern Daylight Time (EDT)
    tz = pytz.timezone('US/Eastern')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %I:%M %p %Z")
    
    # Create the interval structure
    interval_data = {
        "timestamp": current_time,
        "data": {}
    }
    
    # Scrape each URL
    for sport, url in URLS.items():
        print(f"Fetching data for {sport}...")
        interval_data["data"][sport] = fetch_odds_data(sport, url)

    # Load existing JSON data if the file already exists
    historical_data = []
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                historical_data = json.load(f)
        except json.JSONDecodeError:
            historical_data = []

    # Add the newly scraped interval to the historical array
    historical_data.append(interval_data)

    # Save everything back to the JSON file
    with open(FILE_NAME, "w") as f:
        json.dump(historical_data, f, indent=4)
        
    print(f"Data successfully appended to {FILE_NAME}")

if __name__ == "__main__":
    main()
