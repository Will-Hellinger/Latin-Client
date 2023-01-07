from web_driver import *
import time

driver.get("https://lthslatin.org/")
time.sleep(3)

cookie_key = '"PHPSESSID=ee5b6124e9ea48a76cb92cfa58a4d222"'
driver.execute_script(f'document.cookie = {cookie_key}')
time.sleep(.5)
driver.get("https://lthslatin.org/")