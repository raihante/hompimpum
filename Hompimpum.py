# HOPIM AUTO BET
# Author    : @fakinsit
# Date      : 26/08/24


import os
import urllib.request
import urllib.parse
import time
import json
import sys
from pyfiglet import Figlet
from colorama import Fore
from fake_useragent import UserAgent
from urllib import request, parse



def forever():
    try:
        value = True
        while (value):
            turnsplay()
    except Exception as e:

        print('\033[1;91m[ERROR] Restarting!!\033[1;m')
        time.sleep(5)
        forever()

def banner():
    os.system("title HOPIUM BOT | t.me/fakinsit" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")
    custom_fig = Figlet(font='slant')
    print('')
    print(custom_fig.renderText(' HOPIUM'));
    print(Fore.RED + '[#] [C] R E G E X    ' + Fore.GREEN + '[HOPIUM BOT] $$ ' + Fore.RESET)
    print(Fore.GREEN +'[#] Welcome & Enjoy !', Fore.RESET)
    print(Fore.YELLOW +'[#] Having Troubles? PM Telegram [t.me/fakinsit] ', Fore.RESET)
    print('')




with open('query.txt', 'r') as pler:
    quentod = pler.read()
user_agent = UserAgent()
random_user_agent = user_agent.random
textpayload = {'side':'PUMP'}
header = {
        'user-agent': random_user_agent,
        'authorization': 'tma ' + quentod
}


def getstatus():
	url = 'https://hopium.dev/api/wallets/balance'
	request = urllib.request.Request(url, headers=header)
	response = urllib.request.urlopen(request).read()
	encme = response.decode('utf-8')
	res = json.loads(encme)

	jsonlivebalance =  res['balance']
	jsontotalscore =  res['point']

	print("")
	print(Fore.GREEN, '[STATUS]', Fore.RESET, 'HOPIUM :'+ Fore.YELLOW, jsonlivebalance, Fore.RESET,'| TOTAL SCORE :', Fore.YELLOW, jsontotalscore, Fore.RESET)


def turnsplay():
    global textpayload
    getstatus()
    data = parse.urlencode(textpayload).encode()
    url = 'https://hopium.dev/api/game/play'
    request = urllib.request.Request(url, data=data, headers=header)
    response = urllib.request.urlopen(request).read()
    encme = response.decode('utf-8')
    res3 = json.loads(encme)

    if res3 == {'statusCode': 429, 'message': 'ThrottlerException: Too Many Requests'}:
            print(Fore.RED, '[STATUS] ERROR TOO MANY REQUEST !', Fore.RESET)
    elif res3 == {'message': 'User is already playing', 'error': 'Bad Request', 'statusCode': 400}:
            print(Fore.RED, '[STATUS] ERROR USER ALREADY PLAYING !', Fore.RESET)
    else:
            jsonop =  res3['openPrice']
            jsonside =  res3['side']
            jsonidplay =  res3['_id']

            time.sleep(5)
            url2 = 'https://hopium.dev/api/game/turns/'+jsonidplay
            request = urllib.request.Request(url2, headers=header)
            response = urllib.request.urlopen(request).read()
            encme2 = response.decode('utf-8')
            res4 = json.loads(encme2)
            #print(res4)

            if res4 == {'statusCode': 429, 'message': 'ThrottlerException: Too Many Requests'}:
                    print(Fore.RED, '[STATUS] ERROR TOO MANY REQUEST !', Fore.RESET)
            elif res4 == {'message': 'User is already playing', 'error': 'Bad Request', 'statusCode': 400}:
                    print(Fore.RED, '[STATUS] ERROR USER ALREADY PLAYING !', Fore.RESET)
            else:

                
                    jsoncloseprice =  res4['closePrice']
                    jsonres =  res4['result']    
                    jsonws =  res4['winStreak']

                    if jsonside == "PUMP" and jsonres == "WIN":
                        textpayload = {'side':'PUMP'}
                    elif jsonside == "PUMP" and jsonres == "MISS":
                        textpayload = {'side':'DUMP'}
                    elif jsonside == "DUMP" and jsonres == "WIN":
                        textpayload = {'side':'DUMP'}
                    else:
                        textpayload = {'side':'PUMP'}
                    
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
        


# NYALAIN SENDIRI ABANGKUHH
if __name__ == "__main__":
    try:
        banner()
        forever()
    except KeyboardInterrupt:
        sys.exit()
