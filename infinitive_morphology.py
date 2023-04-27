from web_driver import *
import time

def enter_addon():
    selected = driver.switch_to.active_element

    if loadWait(By.XPATH, f"// a[@id='inffeedback']"):
        driver.find_element(By.XPATH, f"// a[@id='inffeedback']").click()
    
    while True:
        if 'morphology' not in str(driver.title).lower():
            break

        try:
            selected.click()
            break
        except:
            time.sleep(.1)