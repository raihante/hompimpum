# HOPIM AUTO BET
# Author    : @fakinsit
# Date      : 26/08/24

import os
import urllib.request
import urllib.parse
import time
import json
import sys
import logging
from pyfiglet import Figlet
from colorama import Fore
from fake_useragent import UserAgent
from urllib import request, parse
from datetime import datetime

logging.basicConfig(filename='re.log', level=logging.INFO, format='[%(asctime)s] - %(levelname)s - [%(message)s]')

def restart_program():
    """Restart the bot in case of an error"""
    logging.error('[ERROR] RESTARTING...')
    print(f'{Fore.RED}[ERROR] RESTARTING...{Fore.RESET}')
    print(f'{Fore.RED}[ERROR] IF CONTINUOUSLY RESTARTING{Fore.RESET} CHAT TELEGRAM [t.me/fakinsit]')
    time.sleep(5)
    main_loop()

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


def get_status(authorization_token):
    """Retrieve and display the current wallet status with timestamp in purple"""
    url = 'https://hopium.dev/api/wallets/balance'
    headers = {'user-agent': get_user_agent(), 'authorization': f'tma {authorization_token}'}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request).read()
    result = json.loads(response.decode('utf-8'))

    balance = result['balance']
    total_score = result['point']

    timestamp = get_formatted_time()
    logging.info(f'HOPIUM BALANCE: {balance} | TOTAL SCORE: {total_score}')
    
    print(f"{Fore.MAGENTA}[{timestamp}]{Fore.RESET} HOPIUM: {Fore.YELLOW}{balance}{Fore.RESET} | TOTAL SCORE: {Fore.YELLOW}{total_score}{Fore.RESET}")


def play_turn(authorization_token, payload):
    """Play the game turn and display the result"""
    data = parse.urlencode(payload).encode()
    url = 'https://hopium.dev/api/game/play'
    headers = {'user-agent': get_user_agent(), 'authorization': f'tma {authorization_token}'}
    request = urllib.request.Request(url, data=data, headers=headers)
    response = urllib.request.urlopen(request).read()
    result = json.loads(response.decode('utf-8'))

    if result.get('statusCode') == 429:
        logging.error('ERROR TOO MANY REQUESTS!')
        print(f'{Fore.RED}[STATUS] ERROR TOO MANY REQUESTS!{Fore.RESET}')
        return None
    elif result.get('statusCode') == 400:
        logging.error('ERROR USER ALREADY PLAYING!')
        print(f'{Fore.RED}[STATUS] ERROR USER ALREADY PLAYING!{Fore.RESET}')
        return None

    logging.info(f'PLAYED TURN : GAME_ID: {result["_id"]} | OPEN PRICE: {result["openPrice"]} | BET : {result["side"]}')
    return result['_id'], result['openPrice'], result['side']


def get_turn_result(authorization_token, game_id):
    """Get the result of the played turn"""
    url = f'https://hopium.dev/api/game/turns/{game_id}'
    headers = {'user-agent': get_user_agent(), 'authorization': f'tma {authorization_token}'}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request).read()
    result = json.loads(response.decode('utf-8'))

    if result.get('statusCode') == 429:
        logging.error('ERROR TOO MANY REQUESTS!')
        print(f'{Fore.RED}[STATUS] ERROR TOO MANY REQUESTS!{Fore.RESET}')
    elif result.get('statusCode') == 400:
        logging.error('ERROR USER ALREADY PLAYING!')
        print(f'{Fore.RED}[STATUS] ERROR USER ALREADY PLAYING!{Fore.RESET}')
    else:
        return result['closePrice'], result['result'], result['winStreak']


def main_loop():
    """Main loop to keep playing the game"""
    with open('query.txt', 'r') as file:
        authorization_token = file.read().strip()

    payload = {'side': 'PUMP'}

    while True:
        try:
            get_status(authorization_token)
            game_id, open_price, side = play_turn(authorization_token, payload)
            if game_id:
                time.sleep(5) 
                close_price, result, win_streak = get_turn_result(authorization_token, game_id)

                if side == 'PUMP' and result == 'MISS':
                    payload = {'side': 'DUMP'}
                elif side == 'DUMP' and result == 'MISS':
                    payload = {'side': 'PUMP'}

                display_turn_result(open_price, close_price, side, result, win_streak)

        except Exception as e:
            logging.exception(f'Exception occurred: {e}')
            restart_program()


def display_turn_result(open_price, close_price, side, result, win_streak):
    """Display the result of a turn with a timestamp in purple"""
    side_color = Fore.GREEN if side == 'PUMP' else Fore.RED
    result_color = Fore.GREEN if result == 'WIN' else Fore.RED
    win_streak_color = Fore.GREEN if win_streak > 0 else Fore.RED

    timestamp = get_formatted_time() 
    logging.info(f'TURN RESULT : BET {side} | OPEN PRICE {open_price} | CLOSE PRICE {close_price} | RESULT {result} | WINSTREAK {win_streak}')
    
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
