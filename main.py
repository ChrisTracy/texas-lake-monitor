import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get the current water level percentage
def get_lake_info(uri):
    try:
        response = requests.get(uri)
        soup = BeautifulSoup(response.content, 'html.parser')
        h2_content = soup.find(class_="page-title").h2.get_text()
        
        # Regex to extract the percentage
        percentage_match = re.search(r'(\d+\.?\d*)% full', h2_content)
        
        percentage = percentage_match.group(1) if percentage_match else None
        
        return percentage
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return "Unknown Lake", None

# Function to read the last stored percentage from JSON
def read_last_percentage():
    try:
        with open('/data/last_percentage.json', 'r') as file:
            data = json.load(file)
            return data['last_percentage']
    except FileNotFoundError:
        return None
    except Exception as e:
        logging.error(f"Error reading from file: {e}")
        return None

# Function to save the current percentage to JSON
def save_current_percentage(percentage):
    try:
        os.makedirs('/data', exist_ok=True)
        with open('/data/last_percentage.json', 'w') as file:
            json.dump({'last_percentage': percentage}, file)
        logging.info("Successfully saved the current percentage.")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")

# Function to send an alert using Pushover
def send_alert(message, app_token, user_key):
    try:
        pushover_url = 'https://api.pushover.net/1/messages.json'
        data = {
            'token': app_token,
            'user': user_key,
            'message': message
        }
        response = requests.post(pushover_url, data=data)
        response.raise_for_status()  # This will raise an error for non-200 responses
        logging.info("Alert sent successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send alert: {e}")

def main():
    app_token = os.getenv('PUSHOVER_APP_TOKEN')
    user_key = os.getenv('PUSHOVER_USER_KEY')
    lake_name = os.getenv('LAKE_NAME')
    interval = int(os.getenv('INTERVAL', '21600'))  # Default to 6 hours

    #set uri
    uri = f"https://waterdatafortexas.org/reservoirs/individual/{lake_name}"

    # Test Pushover alert at startup
    send_alert(f"Starting monitoring service for lake {lake_name}.", app_token, user_key)

    while True:
        current_percentage = get_lake_info(uri)
        last_percentage = read_last_percentage()

        if current_percentage and current_percentage != last_percentage:
            send_alert(f'Lake {lake_name} is now {current_percentage}% full.', app_token, user_key)
            save_current_percentage(current_percentage)

        time.sleep(interval)

if __name__ == '__main__':
    main()