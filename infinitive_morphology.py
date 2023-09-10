from web_driver import *
import time


def enter_addon() -> None:
    """
    Enter an addon within the web page.

    This function clicks on an addon link if it exists and waits for the web page to load. It then attempts to click the
    selected element, allowing you to interact with the addon.

    :return: None
    """
    
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