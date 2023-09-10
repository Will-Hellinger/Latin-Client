from info import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

try:
    if webbrowserType == 'Chrome' or webbrowserType == 'Chromium' or webbrowserType == 'Brave':
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.core.utils import ChromeType
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('prefs', {"credentials_enable_service": False, "profile.password_manager_enabled": False})
        if webbrowserType == 'Chrome':
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        elif webbrowserType == 'Chromium':
            driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
        elif webbrowserType == 'Brave':
            driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), options=options)
    elif webbrowserType == 'Firefox':
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif webbrowserType == 'Internet Explorer':
        from webdriver_manager.microsoft import IEDriverManager
        driver = webdriver.Ie(IEDriverManager().install())

    elif webbrowserType == 'Edge':
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

    elif webbrowserType == 'Opera':
        from webdriver_manager.opera import OperaDriverManager
        driver = webdriver.Opera(OperaDriverManager().install())
    elif webbrowserType == 'Safari':
        driver = webdriver.Safari()
    else:
        raise ValueError(f'Unsupported browser: {webbrowserType}')
except Exception as error:
    input(f'\033[1;31;40m[-] Failed to Start Client error: {error}')
    exit()

def loadWait(by: type, type: str) -> bool:
    """
    Wait for an element to be present in the web page.

    :param by: The type of locator (e.g., By.XPATH, By.ID).
    :param type: The value of the locator (e.g., "//div[@class='example']").
    :return: True if the element is found within the specified timeout, False otherwise.
    """
    
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, type)))
        return True
    except:
        print(f'unable to load element: {type}')
        return False
