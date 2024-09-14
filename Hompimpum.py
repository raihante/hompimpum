# HOPIM AUTO BET
# Author    : @fakinsit
# Date      : 26/08/24

import os
import time
import json
import sys
import logging
from pyfiglet import Figlet
from colorama import Fore
from fake_useragent import UserAgent
from datetime import datetime
import cloudscraper

# Set up logging
logging.basicConfig(filename='re.log', level=logging.INFO, format='[%(asctime)s] - %(levelname)s - [%(message)s]')

MAX_RETRIES = 20  # Define max retries

def get_formatted_time():
    """Get the current time formatted for display"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def display_banner():
    """Display the welcome banner with bot information"""
    os.system("title HOPIUM BOT | t.me/fakinsit" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")
    custom_fig = Figlet(font='slant')
    print(custom_fig.renderText(' HOPIUM'))
    logging.info('BOT STARTED')
    print(f'{Fore.RED}[#] [C] R E G E X    {Fore.GREEN}[HOPIUM BOT] $$ {Fore.RESET}')
    print(f'{Fore.GREEN}[#] Welcome & Enjoy! {Fore.RESET}')
    print(f'{Fore.YELLOW}[#] Having Troubles? PM Telegram [t.me/fakinsit] {Fore.RESET}')
    print('')

def get_user_agent():
    """Get a random user agent string"""
    user_agent = UserAgent()
    return user_agent.random

# Common headers to be reused
def get_headers(authorization_token):
    """Create common headers to be used across requests"""
    headers = {
    'User-Agent': get_user_agent(),
    'Authorization': f'tma {authorization_token}',
    'Accept': 'application/json, text/plain, */*',
    }
    return headers

def get_status(scraper, authorization_token):
    """Retrieve and display the current wallet status with timestamp in purple"""
    url = 'https://hopium.dev/api/wallets/balance'
    headers = get_headers(authorization_token)
    retries = 0  # Initialize retries counter
    
    while retries < MAX_RETRIES:
        try:
            response = scraper.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()

            balance = result['balance']
            total_score = result['point']

            timestamp = get_formatted_time()  # Get the formatted time

            print(f"{Fore.MAGENTA}[{timestamp}]{Fore.RESET} HOPIUM: {Fore.YELLOW}{balance}{Fore.RESET} | TOTAL SCORE: {Fore.YELLOW}{total_score}{Fore.RESET}")
            return result  # Success, exit the loop

        except cloudscraper.exceptions.CloudflareChallengeError as e:
            retries += 1
            logging.error(f"Error fetching status due to Cloudflare challenge: {e} (Retry {retries}/{MAX_RETRIES})")
            print(f'{Fore.RED}[ERROR] Cloudflare challenge failed! Retrying immediately...{Fore.RESET}')
        except Exception as e:
            retries += 1
            logging.error(f"Error fetching status: {e} (Retry {retries}/{MAX_RETRIES})")
    
    logging.error('Maximum retries reached for get_status.')
    print(f'{Fore.RED}[ERROR] Maximum retries reached for get_status. Stopping...{Fore.RESET}')
    print(f'{Fore.RED}press any key to exit...{Fore.RESET}')
    input()

def play_turn(scraper, authorization_token, payload):
    """Play the game turn and display the result"""
    url = 'https://hopium.dev/api/game/play'
    headers = get_headers(authorization_token)
    retries = 0  # Initialize retries counter
    
    while retries < MAX_RETRIES:
        try:
            response = scraper.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            return result['_id'], result['openPrice'], result['side']  # Success, exit the loop

        except cloudscraper.exceptions.CloudflareChallengeError as e:
            retries += 1
            logging.error(f"Error playing turn due to Cloudflare challenge: {e} (Retry {retries}/{MAX_RETRIES})")
            print(f'{Fore.RED}[ERROR] Cloudflare challenge failed! Retrying immediately...{Fore.RESET}')
        except Exception as e:
            retries += 1
            logging.error(f"Error playing turn: {e} (Retry {retries}/{MAX_RETRIES})")
    
    logging.error('Maximum retries reached for play_turn.')
    print(f'{Fore.RED}[ERROR] Maximum retries reached for play_turn. Stopping...{Fore.RESET}')
    print(f'{Fore.RED}press any key to exit...{Fore.RESET}')
    input()

def get_turn_result(scraper, authorization_token, game_id):
    """Get the result of the played turn"""
    url = f'https://hopium.dev/api/game/turns/{game_id}'
    headers = get_headers(authorization_token)
    retries = 0  # Initialize retries counter

    while retries < MAX_RETRIES:
        try:
            response = scraper.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get('statusCode') == 429:
                retries += 1
                logging.error(f"ERROR TOO MANY REQUESTS! (Retry {retries}/{MAX_RETRIES})")
                print(f'{Fore.RED}[STATUS] ERROR TOO MANY REQUESTS! Retrying immediately...{Fore.RESET}')
                continue
            elif result.get('statusCode') == 400:
                retries += 1
                logging.error(f"ERROR USER ALREADY PLAYING! (Retry {retries}/{MAX_RETRIES})")
                print(f'{Fore.RED}[STATUS] ERROR USER ALREADY PLAYING! Retrying immediately...{Fore.RESET}')
                continue

            return result['closePrice'], result['result'], result['winStreak']  # Success, exit the loop

        except cloudscraper.exceptions.CloudflareChallengeError as e:
            retries += 1
            logging.error(f"Error fetching turn result due to Cloudflare challenge: {e} (Retry {retries}/{MAX_RETRIES})")
            print(f'{Fore.RED}[ERROR] Cloudflare challenge failed! Retrying immediately...{Fore.RESET}')
        except Exception as e:
            retries += 1
            logging.error(f"Error fetching turn result: {e} (Retry {retries}/{MAX_RETRIES})")
    
    logging.error('Maximum retries reached for get_turn_result.')
    print(f'{Fore.RED}[ERROR] Maximum retries reached for get_turn_result. Stopping...{Fore.RESET}')
    print(f'{Fore.RED}press any key to exit...{Fore.RESET}')
    input()

def main_loop():
    """Main loop to keep playing the game"""
    with open('query.txt', 'r') as file:
        authorization_token = file.read().strip()

    payload = {'side': 'PUMP'}

    # Create a cloudscraper session
    scraper = cloudscraper.create_scraper()

    while True:
        get_status(scraper, authorization_token)  # Keep retrying until successful
        game_id, open_price, side = play_turn(scraper, authorization_token, payload)  # Keep retrying until successful
        time.sleep(5)  # Wait for the game result
        close_price, result, win_streak = get_turn_result(scraper, authorization_token, game_id)  # Keep retrying until successful

        # Update payload based on result
        if side == 'PUMP' and result == 'MISS':
            payload = {'side': 'DUMP'}
        elif side == 'DUMP' and result == 'MISS':
            payload = {'side': 'PUMP'}

        display_turn_result(open_price, close_price, side, result, win_streak)

def display_turn_result(open_price, close_price, side, result, win_streak):
    """Display the result of a turn with a timestamp in purple"""
    side_color = Fore.GREEN if side == 'PUMP' else Fore.RED
    result_color = Fore.GREEN if result == 'WIN' else Fore.RED
    win_streak_color = Fore.GREEN if win_streak > 0 else Fore.RED

    timestamp = get_formatted_time()  # Get the formatted time

    print(f"{Fore.MAGENTA}[{timestamp}]{Fore.RESET} BET: {side_color}{side}{Fore.RESET} | OPEN PRICE: {Fore.GREEN}{open_price}{Fore.RESET} | "
          f"CLOSE PRICE: {Fore.RED}{close_price}{Fore.RESET} | WINSTREAK: {win_streak_color}{win_streak}{Fore.RESET} | "
          f"RESULT: {result_color}{result}{Fore.RESET}")
    print('')

if __name__ == "__main__":
    display_banner()
    try:
        main_loop()
    except KeyboardInterrupt:
        logging.info('Program interrupted by user')
        sys.exit()
