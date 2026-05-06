import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import pytz

# Target URLs including the specific MLB endpoint
URLS = {
    "MLB": "https://madduxsports.com/baseballodds.php",
    "NBA": "https://madduxsports.com/nba-odds.html",
    "NHL": "https://madduxsports.com/nhl-odds.html"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

FILE_NAME = "sportdata.json"

def fetch_odds_data(sport, url):
    """Scrapes odds data for a specific sport."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        scraped_games = []
        
        # =========================================================
        # HTML PARSING LOGIC
        # You will need to inspect the tables on baseballodds.php 
        # to map the exact row (tr) and column (td) elements.
        # =========================================================
        
        # Example extraction framework:
        # table = soup.find('table') 
        # if table:
        #     for row in table.find_all('tr')[1:]: # Skip header row
        #         cols = row.find_all('td')
        #         if len(cols) >= 4:
        #             scraped_games.append({
        #                 "matchup": cols[0].text.strip(),
        #                 "spread": cols[1].text.strip(),
        #                 "total": cols[2].text.strip(),
        #                 "moneyline": cols[3].text.strip()
        #             })
        
        # Placeholder so the JSON file generates structure before HTML parsing is mapped
        scraped_games = [{"matchup": "Pending HTML mapping", "spread": "N/A", "total": "N/A"}] 
        
        return scraped_games

    except Exception as e:
        print(f"Error fetching {sport}: {e}")
        return []

def main():
    # Set current time to EDT
    tz = pytz.timezone('US/Eastern')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %I:%M %p %Z")
    
    interval_data = {
        "timestamp": current_time,
        "data": {}
    }
    
    # Scrape data for each sport
    for sport, url in URLS.items():
        print(f"Scraping {sport} from {url}...")
        interval_data["data"][sport] = fetch_odds_data(sport, url)

    # Load existing historical data
    historical_data = []
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                historical_data = json.load(f)
        except json.JSONDecodeError:
            historical_data = []

    # Append the new interval
    historical_data.append(interval_data)

    # Save everything back to the JSON file
    with open(FILE_NAME, "w") as f:
        json.dump(historical_data, f, indent=4)
        
    print(f"Data successfully saved to {FILE_NAME}")

if __name__ == "__main__":
    main()
