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
login = os.getenv("USER")
PW = os.getenv("PW")
print("your username is " + login)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options, executable_path=PATH)

driver.get("https://www.dndbeyond.com")
try:
    login_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-link"))
    )
except:
    print('cant find login link')
login_link.send_keys(Keys.RETURN)

try:
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "signin-with-twitch"))
    )
except:
    print('can not find twitch btn')
element.send_keys(Keys.RETURN)

try:
    print('...finding username')
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-username"))
    )
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password-input"))
    )
except:
    print('can not find input boxes')
print('')
username.send_keys(login)
password.send_keys(PW)

try:
    element = WebDriverWait(driver, TIMEOUT).until(
        EC.title_is("D&D Beyond - An official digital toolset for Dungeons & Dragons (D&D) Fifth Edition (5e)")
    )
except:
    print('{TIMEOUT/3} minute timeout')


driver.get("https://www.dndbeyond.com/my-campaigns")

try:
    game_log_btn = WebDriverWait(driver, TIMEOUT*3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "gamelog-button"))
    )
except:
    print('Please select your campaign within {TIMEOUT/3 * 3} minutes')

game_log_btn.send_keys(Keys.RETURN)
try:
    g_log = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.CLASS_NAME, "GameLog_GameLogEntries__3oNPD"))
    )
except:
    print('unable to find path for log')
g_log_list = g_log.find_elements(By.TAG_NAME, 'li')

print(len(g_log_list))

for roll in g_log_list:
    container = roll.find_element(By.TAG_NAME, 'div')
    divs = container.find_elements(By.TAG_NAME, 'div')
    for div in divs:
        try:
            print(div.text)
        except:
            print("no text")
print('done')
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
