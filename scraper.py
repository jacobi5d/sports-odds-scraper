import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import pytz

# Target URLs (Update these if the actual endpoints differ)
URLS = {
    "NBA": "https://madduxsports.com/nba-odds.html",
    "NHL": "https://madduxsports.com/nhl-odds.html",
    "MLB": "https://madduxsports.com/mlb-odds.html"
}

# Use a standard User-Agent so the site doesn't block the request
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
        
        # =========================================================
        # TODO: UPDATE HTML PARSING LOGIC HERE
        # You must inspect Madduxsports to find the correct table classes.
        # Example: table = soup.find('table', {'class': 'odds-table'})
        # =========================================================
        
        scraped_games = []
        
        # Simulated extraction logic (Replace with actual table row iteration)
        # for row in table.find_all('tr')[1:]:
        #     cols = row.find_all('td')
        #     if len(cols) > 3:
        #         scraped_games.append({
        #             "matchup": cols[0].text.strip(),
        #             "spread": cols[1].text.strip(),
        #             "total": cols[2].text.strip(),
        #             "moneyline": cols[3].text.strip()
        #         })
        
        # Placeholder data to show structure if parsing isn't configured yet
        scraped_games = [{"status": "Parsing logic needs HTML tags from site"}] 
        
        return scraped_games

    except Exception as e:
        print(f"Error fetching {sport}: {e}")
        return []

def main():
    # Set current time in EDT
    tz = pytz.timezone('US/Eastern')
    current_time = datetime.now(tz).strftime("%Y-%m-%d %I:%M %p %Z")
    
    # Initialize data dictionary
    interval_data = {
        "timestamp": current_time,
        "data": {}
    }
    
    # Scrape data for each sport
    for sport, url in URLS.items():
        print(f"Scraping {sport}...")
        interval_data["data"][sport] = fetch_odds_data(sport, url)

    # Load existing data from JSON file
    historical_data = []
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                historical_data = json.load(f)
        except json.JSONDecodeError:
            historical_data = []

    # Append new interval data
    historical_data.append(interval_data)

    # Save updated data back to JSON file
    with open(FILE_NAME, "w") as f:
        json.dump(historical_data, f, indent=4)
        
    print(f"Data successfully saved to {FILE_NAME}")

if __name__ == "__main__":
    main()
