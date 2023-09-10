import time
from info import *
from web_driver import *
from pypresence import Presence


def check_discord() -> bool:
    """
    Check if Discord Rich Presence (RPC) can be enabled and establish a connection if possible.

    This function initializes the Discord RPC client and attempts to connect to Discord. If successful, it returns True;
    otherwise, it returns False.

    :return: True if Discord RPC is successfully enabled, False otherwise.
    """

    global RPC
    global RPCTime

    try:
        client_id = '993019974253822034'
        RPC = Presence(client_id)

        if discord_rpc == True:
            RPC.connect()

            RPCTime = int(time.time())
            RPC.update(large_image = "logo1", state = 'Starting up...', start = RPCTime)

            return True
    except:
        return False


def update_rpc(mode: str, assignment: str) -> None:
    """
    Update Discord Rich Presence (RPC) status based on the current mode and assignment.

    This function updates the Discord RPC status based on the provided mode and assignment. It displays relevant details
    and states in the Discord RPC presence.

    :param mode: The current mode, e.g., 'synopsis', '(grasp)', 'reading', etc.
    :param assignment: The current assignment or task.
    :return: None
    """
    
    global RPC
    global RPCTime
    
    RPC_details = None

    match mode:
        case 'synopsis':
            if loadWait(By.XPATH, f"// h1[@class='showScore ui-title']"):
                score = driver.find_element(By.XPATH, f"// h1[@class='showScore ui-title']")
                if 'score' not in str(score.text):
                    RPC_details = str(score.text)
        
        case '(grasp)':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                RPC_details = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text)
        
        case 'reading':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                RPC_details = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text)
        
        case 'composition':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                RPC_details = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text)
        
        case 'translation':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                RPC_details = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text)
        
        case 'ciples':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-title']"):
                RPC_details = '(' + str(assignment.split('(')[1])
                showScore = driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']")

                if str(showScore.text) != 'your score will appear here':
                    RPC_details += ' / ' + str(showScore.text)
                assignment = str(assignment.split('(')[0])
        
        case 'infinitive morphology':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-title']"):
                RPC_details = '(' + str(assignment.split('(')[1])
                showScore = driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']")

                if str(showScore.text) != 'your score will appear here':
                    RPC_details += ' / ' + str(showScore.text)
                assignment = str(assignment.split('(')[0])

        case 'noun-adj':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                showScore = driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']")

                if 'will appear here' not in str(showScore.text):
                    RPC_details = str(str(showScore.text).split('\n')[0]).split('correctly. ')[1]


    if RPC_details is not None:
        RPC.update(large_image = "logo1", details = assignment, state = RPC_details, start = RPCTime)
    
    elif RPC_details is None:
        RPC.update(large_image = "logo1", details = assignment, start = RPCTime)