import os
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TOKEN or not CHAT_ID:
    raise ValueError('TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set in the .env file')

bot = Bot(token=TOKEN)

BASE_URL = 'https://tophotfashion.x.yupoo.com/'
SEEN_FILE = 'seen_albums.txt'
LOG_FILE = 'log.txt'
CHECK_INTERVAL = 300  # 5 minutes in seconds

# Ensure log file exists
open(LOG_FILE, 'a').close()
# Ensure seen file exists
if not os.path.exists(SEEN_FILE):
    open(SEEN_FILE, 'a').close()


def load_seen_links():
    with open(SEEN_FILE, 'r') as f:
        return set(line.strip() for line in f if line.strip())


def save_seen_links(links):
    with open(SEEN_FILE, 'w') as f:
        for link in links:
            f.write(f"{link}\n")


def log_notification(link):
    from datetime import datetime
    with open(LOG_FILE, 'a') as log:
        log.write(f"{datetime.now().isoformat()} - {link}\n")


def get_album_links():
    """Fetch album links from the Yupoo site."""
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for a in soup.select('a[href]'):
        href = a.get('href')
        if href and '/albums/' in href:
            # Build absolute link if needed
            if href.startswith('http'):
                links.add(href)
            else:
                links.add(requests.compat.urljoin(BASE_URL, href))
    return links


def notify_new_album(link):
    bot.send_message(chat_id=CHAT_ID, text=f"Nouveau album : {link}")
    log_notification(link)


if __name__ == '__main__':
    seen_links = load_seen_links()
    while True:
        try:
            current_links = get_album_links()
            new_links = current_links - seen_links
            for link in new_links:
                notify_new_album(link)
                seen_links.add(link)
            if new_links:
                save_seen_links(seen_links)
        except Exception as e:
            print(f"Error during check: {e}")
        print('Vérification terminée')
        time.sleep(CHECK_INTERVAL)
