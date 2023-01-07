from web_driver import *
import time

def enter_addon():
    selected = driver.switch_to.active_element
    if loadWait(By.XPATH, f"// a[@id='inffeedback']"):
        driver.find_element(By.XPATH, f"// a[@id='inffeedback']").click()
    while True:
        try:
            selected.click()
            break
        except Exception as error:
            if 'morphology' not in str(driver.title).lower():
                break
            time.sleep(.25)