import requests
import socks
import socket
import logging
import sqlite3
import asyncio
import aiohttp
import aioredis
import json
import argparse
from stem.control import Controller
from email.mime.text import MIMEText
import smtplib
import time
from stem import Signal
from stem.control import Controller
import gnupg
import threading
import random
from fake_useragent import UserAgent
import hashlib
import hmac
import telebot
import sys
from colorama import Fore, Style, init
from tqdm import tqdm
import readline
import curses

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    filename='dark_web_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)


# Database setup
def init_db():
    conn = sqlite3.connect('dark_web_monitor.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS breaches (id INTEGER PRIMARY KEY, email TEXT, breach_data TEXT)''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY, keyword TEXT, site TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


# Redis caching setup
redis_client = aioredis.from_url("redis://localhost")


# Restart Tor Circuit
def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_tor_password")
        controller.signal(Signal.NEWNYM)
        time.sleep(10)


# Tor Proxy Setup
def start_tor_proxy():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket


# Generate random user-agents
def get_random_user_agent():
    return UserAgent().random


# CLI function
def cli():
    history = []
    while True:
        print(Fore.MAGENTA + "\n========================================")
        print(Fore.YELLOW + "      🌐 Sahil's Dark Web Monitor 🌐      ")
        print(Fore.MAGENTA + "========================================\n")
        print(Fore.CYAN + "🔍 1. Check if an email has been breached")
        print(Fore.CYAN + "🕵️ 2. Search for a keyword on the dark web")
        print(Fore.BLUE + "📜 3. View search history")
        print(Fore.RED + "❌ 4. Exit\n")

        choice = input(Fore.MAGENTA + "➡️ Enter your choice (1/2/3/4): ")

        if choice == "1":
            email = input(Fore.CYAN + "📧 Enter the email to check: ")
            history.append(f"Checked email: {email}")
            for _ in tqdm(range(10), desc="Checking", ascii=True):
                time.sleep(0.2)
            asyncio.run(check_hibp_cli(email))
        elif choice == "2":
            keyword = input(Fore.CYAN + "🔑 Enter the keyword to search: ")
            history.append(f"Searched keyword: {keyword}")
            for _ in tqdm(range(10), desc="Searching", ascii=True):
                time.sleep(0.2)
            asyncio.run(scrape_dark_web_cli(keyword))
        elif choice == "3":
            print(Fore.BLUE + "📜 Search History:")
            for item in history:
                print(Fore.YELLOW + "- " + item)
        elif choice == "4":
            print(Fore.RED + "👋 Exiting... Goodbye!")
            sys.exit(0)
        else:
            print(Fore.RED + "⚠️ Invalid choice! Please select a valid option.")


# Check Have I Been Pwned with CLI support
async def check_hibp_cli(email):
    hibp_api_key = "YOUR_HIBP_API_KEY"
    breaches = await check_hibp(email, hibp_api_key)
    if breaches:
        logging.info(Fore.RED + f"🚨 [!] {email} has been found in breaches: {breaches}")
    else:
        logging.info(Fore.GREEN + f"✅ [+] No breaches found for {email}")


# Dark Web Scraping with CLI support
async def scrape_dark_web_cli(keyword):
    dark_web_sites = ["http://exampleonion.onion"]
    logging.info(Fore.YELLOW + f"🔍 [*] Searching for '{keyword}' on the dark web...")
    for site in dark_web_sites:
        found = await scrape_dark_web(keyword, site)
        if found:
            logging.info(Fore.RED + f"🚨 [!] Keyword '{keyword}' found on {site}")
        else:
            logging.info(Fore.GREEN + f"❌ [-] No results found for '{keyword}' on {site}")


# Check Have I Been Pwned with caching
async def check_hibp(email, hibp_api_key):
    cached_result = await redis_client.get(email)
    if cached_result:
        return json.loads(cached_result)

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {'hibp-api-key': hibp_api_key, 'User-Agent': 'DarkWebMonitor'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        breaches = response.json()
        conn = sqlite3.connect('dark_web_monitor.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO breaches (email, breach_data) VALUES (?, ?)", (email, str(breaches)))
        conn.commit()
        conn.close()
        await redis_client.set(email, json.dumps(breaches), ex=86400)
        return breaches
    return []


# Dark Web Scraping with Async Requests
async def scrape_dark_web(keyword, target_url):
    try:
        renew_tor_ip()
        start_tor_proxy()
        headers = {'User-Agent': get_random_user_agent()}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(target_url, timeout=10) as response:
                text = await response.text()
                if keyword.lower() in text.lower():
                    logging.info(Fore.RED + f"🚨 Keyword '{keyword}' found on {target_url}")
                    conn = sqlite3.connect('dark_web_monitor.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO alerts (keyword, site) VALUES (?, ?)", (keyword, target_url))
                    conn.commit()
                    conn.close()
                    return True
        return False
    except Exception as e:
        logging.error(Fore.RED + f"⚠️ Error scraping {target_url}: {e}")
        return False


if __name__ == "__main__":
    cli()
