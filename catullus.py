import openai
from info import *
from web_driver import *

def solve():
    global openai_enabled
    global openai_token
    global openai_model
    
    if openai_enabled == False or openai_token == "none":
        return None

    openai.api_key = openai_token

    catullus_poem = str(driver.find_element(By.ID, 'translation_write').text)
    catullus_prompt = str(driver.find_element(By.XPATH, "// div[@class='ui-body ui-body-a']"))
    thesis_input = driver.find_element(By.ID, 'thesis_write')

    response = openai.ChatCompletion.create(model=openai_model, messages=[{"role": "user", "content": f"Write a thesis using the following prompt(keep it at one sentence and short. Write in a formal manner while still highschooler like): {catullus_prompt}\n\nThe 85th poem: {catullus_poem}"}])

    thesis_input.clear()
    thesis_input.send_keys(str(response.choices[0].message.content))
    thesis_input.send_keys(Keys.ENTER)