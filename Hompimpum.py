# HOPIM AUTO BET
# Author    : @fakinsit
# Date      : 26/08/24


import os
import asyncio
import aiohttp
import time
from pyfiglet import Figlet
from colorama import Fore
from fake_useragent import UserAgent


async def forever():
    banner()
    while True:
        try:
            await main()
        except:
            print(Fore.RED, '[STATUS] ERROR RESTARTING BOT !', Fore.RESET)
            await main()

def banner():
    os.system("title HOPIUM AUTO BET")
    os.system('cls')
    custom_fig = Figlet(font='slant')
    print(' =========================================')
    print('')
    print(custom_fig.renderText(' HOPIUM')) 
    print(Fore.RED, ' # [C] R E G E X    ', Fore.GREEN, '[HOPIUM AUTO BET] $$ ', Fore.RESET)
    print('')
    print(' =========================================')
    print(Fore.GREEN +' Welcome & Enjoy !', Fore.RESET)
    print(Fore.YELLOW +' Having Troubles? PM Telegram [t.me/fakinsit] ', Fore.RESET)




with open('query.txt', 'r') as pler:
    quentod = pler.read()
user_agent = UserAgent()
random_user_agent = user_agent.random
textpayload = '{"side":"PUMP"}'
headers = {
        "Host": 'hopium.dev',
        "User-Agent": random_user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': 'tma ' + quentod
}


async def getstatus(url, session):
    async with session.get(url, headers=headers) as response:
        res = await response.json()
        jsonlivebalance =  res['balance']
        jsontotalscore =  res['point']

        print("")
        print(Fore.GREEN, '[STATUS]', Fore.RESET, 'HOPIUM :'+ Fore.YELLOW, jsonlivebalance, Fore.RESET,'| TOTAL SCORE :', Fore.YELLOW, jsontotalscore, Fore.RESET)


async def turnsplay(url, session):
    global textpayload
    
    async with session.post(url, headers=headers, data=textpayload) as response3:
        res3 = await response3.json()

        if res3 == {'statusCode': 429, 'message': 'ThrottlerException: Too Many Requests'}:
            print(Fore.RED, '[STATUS] ERROR TOO MANY REQUEST !', Fore.RESET)
        elif res3 == {'message': 'User is already playing', 'error': 'Bad Request', 'statusCode': 400}:
            print(Fore.RED, '[STATUS] ERROR USER ALREADY PLAYING !', Fore.RESET)
        else:
            jsonop =  res3['openPrice']
            jsonside =  res3['side']
            jsonidplay =  res3['_id']

            time.sleep(5)

            async with session.get('https://hopium.dev/api/game/turns/'+jsonidplay, headers=headers, data=textpayload) as response4:
                res4 = await response4.json()

                if res4 == {'statusCode': 429, 'message': 'ThrottlerException: Too Many Requests'}:
                    print(Fore.RED, '[STATUS] ERROR TOO MANY REQUEST !', Fore.RESET)
                elif res4 == {'message': 'User is already playing', 'error': 'Bad Request', 'statusCode': 400}:
                    print(Fore.RED, '[STATUS] ERROR USER ALREADY PLAYING !', Fore.RESET)
                else:

                
                    jsoncloseprice =  res4['closePrice']
                    jsonres =  res4['result']    
                    jsonws =  res4['winStreak']

                    if jsonside == "PUMP" and jsonres == "WIN":
                        textpayload = '{"side":"PUMP"}'
                    elif jsonside == "PUMP" and jsonres == "MISS":
                        textpayload = '{"side":"DUMP"}'
                    elif jsonside == "DUMP" and jsonres == "WIN":
                        textpayload = '{"side":"DUMP"}'
                    else:
                        textpayload = '{"side":"PUMP"}'
                    
                    if jsonres == "MISS":
                        jsonres = Fore.RED + "MISS"
                    else:
                        jsonres = Fore.GREEN + "WIN"

                    if jsonside == "DUMP":
                        jsonside = Fore.RED + 'DUMP'
                    else:
                        jsonside = Fore.GREEN + 'PUMP'

                    if jsonws == 0:
                        jsonws2 = Fore.RED + str(jsonws)
                    else:
                        jsonws2 = Fore.GREEN + str(jsonws)

                    print(Fore.GREEN, '[STATUS]', Fore.RESET, 'BET :', jsonside , Fore.RESET, '| OPEN PRICE :', Fore.GREEN , jsonop , Fore.RESET, '| CLOSE PRICE :', Fore.RED, jsoncloseprice , Fore.RESET, '| WINSTREAK :', jsonws2 , Fore.RESET, '| RESULT :', jsonres , Fore.RESET)

        


async def main():
    try:
        async with aiohttp.ClientSession() as session:
            await getstatus("https://hopium.dev/api/wallets/balance", session)
            await turnsplay("https://hopium.dev/api/game/play", session)
    except:
        await main()
try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(forever())
except:
    print(Fore.RED, '[STATUS] ERROR RESTARTING BOT !', Fore.RESET)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(forever())