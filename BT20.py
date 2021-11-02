import time
import asyncio
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()

TIMEOUT = 180
PATH = "C:\Program Files (x86)\chromedriver.exe"

#you can automate login by putting username and password into a .env file
login = os.getenv("USER")
PW = os.getenv("PW")
CHROME_USER_PATH = os.getenv("CHROME_DEFAULT_USER_PATH")
print("your username is " + login)

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={CHROME_USER_PATH}")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options, executable_path=PATH)

driver.get("https://www.dndbeyond.com")
main_page = driver.current_window_handle

def roll_message():
    print()

#needs to be reworked to account for multiple rolls in quick succession
# i.e. if it goes from 12 rolls to 15 rolls, print out divs[0, 1, 2]
def roll_listener(g_log):
    print("listener, engaged")
    rolls = g_log.find_elements(By.TAG_NAME, 'li')
    curr_rolls = len(rolls)
    prev_rolls = curr_rolls

    while curr_rolls == prev_rolls:
        print(f"rolls: {len(rolls)}")
        rolls = g_log.find_elements(By.TAG_NAME, 'li')
        curr_rolls = len(rolls)
        time.sleep(1)
    rolls = g_log.find_elements(By.TAG_NAME, 'li')
    divs = rolls[0].find_elements(By.TAG_NAME, 'div')

    try:
        print(f"here is first div: {divs[0].text}")
    except:
        print(f"here is first div: {divs[0].text()}")
    try:
        message_container = divs[0].find_elements(By.TAG_NAME, 'div')
        name = message_container[0]
        message_container2 = message_container[1].find_elements(By.TAG_NAME, 'div')
        message = message_container2[0].find_element(By.TAG_NAME, 'div')
        roll_info = message.find_elements(By.TAG_NAME, 'div')
        roll_info_2 = roll_info[0].find_elements(By.TAG_NAME, 'div')
        dice_rolls = roll_info_2[1].find_element(By.TAG_NAME, 'span')
        total = roll_info[1]

        print(f"here is name of roller: {name.text}")
        print(f"expecting roll type: {roll_info_2[0].text}")
        print(f"expecting dice roll notation: {roll_info_2[2].text}")
        print(f"expecting dice roll results: {dice_rolls.get_attribute('title')}")
        print(f"expecting total: {total.text}")
        print(f"*******\nhere is roll_info:\n{roll_info.text}")
        print(f"*******\nhere is roll_info_2:\n{roll_info_2.text}")
    except Exception as e:
        print("deep fail")
        print(e)
    roll_listener(g_log)


#Login process
try:
    login_link = WebDriverWait(driver, 0).until(
        EC.presence_of_element_located((By.ID, "login-link"))
    )
    login_link.send_keys(Keys.RETURN)
    try:
        #OAUTH automation
        #You can remove/ignore this section if you want to login manually
        signin_with_google = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "signin-with-google"))
        )
        signin_with_google.send_keys(Keys.RETURN)
        driver.implicitly_wait(1)

        #gets the login page
        for handle in driver.window_handles:
            if handle != main_page:
                login_page = handle

        #switches to login window and selects first email
        try:
            driver.switch_to.window(login_page)
            your_account_expected = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "lCoei"))
            )
            your_account_expected.click()
            driver.switch_to_window(main_page)
        except:
            print("could not switch to login or could not find any emails to login to")

        #login automation with user info from .env
        # try:
        #     print('...finding username')
        #     username = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "login-username"))
        #     )
        #     password = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "password-input"))
        #     )
        # except:
        #     print('can not find input boxes')
        # print('')
        # username.send_keys(login)
        # password.send_keys(PW)
    except:
        print('can not find google btn')
except:
    print('Can not find login link. You might already be logged in')



try:
    driver.get("https://www.dndbeyond.com/my-campaigns")

    s = "s" if (TIMEOUT/3 > 1) else ""
    print(f"Select a campaign within {TIMEOUT/60 * 3} minute{s}")

    try:
        game_log_btn = WebDriverWait(driver, TIMEOUT * 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gamelog-button"))
        )
        game_log_btn.send_keys(Keys.RETURN)
    except:
        print(f'Process failed. Please select your campaign within {TIMEOUT/60 * 3} minutes')

    ###################################

    try:
        g_log = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.CLASS_NAME, "GameLog_GameLogEntries__3oNPD"))
        )
        driver.implicitly_wait(3)
        roll_listener(g_log)
    except Exception as e:
        print('unable to find path for log')
        print(e)
except:
    print(f'{TIMEOUT/3} minute timeout')

# sender = roll.find_element(By.CLASS_NAME, "GameLogEntry_Sender_1nlKd").text
# action = roll.find_element(By.CLASS_NAME, "DiceMessage_action__192Yv").text
# roll_type = roll.find_element(By.CLASS_NAME, "DiceMessage_RollType__wlBs").text
# dice = roll.find_element(By.CLASS_NAME, "DiceMessage_notation__1Rbq5").text
# total = roll.find_element(By.CLASS_NAME, "DiceMessage_total__2BPku").text
#
# print(sender)
# print(action)
# print(roll_type)
# print(dice)
# print(total)
#sender class: GameLogEntry_Sender_1nlKd
#throws/checks/attacks: DiceMessage_action__192Yv
#to hit/damage/check/save: DiceMessage_RollType__wlBs
#dice rolled: DiceMessage_notation__1Rbq5
#dice result: DiceMessage_total__2BPku



# game_log_list = game_log_entries.find_elements_by_css_selector("div")
# try:
#     print("length:")
#     print(len(game_log_list))
# except:
#     print("failed len()")
#
# x = 0
# for ele in game_log_list:
#     print(x)
#     print(ele.tag_name)
#     x = x + 1
#
# print("***************")
# print(game_log_entries)
# game_log_entries = game_log_entries.find_element_by_css_selector("ol")
# print("***************")
# print(game_log_entries)

# when array.length == array.length + 1, do stuff, then wait for
