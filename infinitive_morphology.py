from web_driver import *
import time

def enter_addon():
    selected = driver.switch_to.active_element

    if loadWait(By.XPATH, f"// a[@id='inffeedback']"):
        driver.find_element(By.XPATH, f"// a[@id='inffeedback']").click()
    
    while True:
        if 'morphology' not in str(driver.title).lower():
            time.sleep(.25)
        elif 'morphology' in str(driver.title).lower():
            selected.click()
            break