import os
import requests
import pandas as pd
from time import sleep, time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

debug = True

if debug:
    # debug times, change when ready to use
    START_TIME = time()
    END_TIME = START_TIME + 90
    LOOP_TIME = 30  # sleep time before next while loop iteration
else:
    today = datetime.now().strftime("%m-%d-%y")
    start_hour = "10:00"
    end_hour = "20:00"
    # convert times into floats
    START_TIME = datetime.strptime(f"{today} {start_hour}", "%m-%d-%y %H:%M").timestamp()
    END_TIME = datetime.strptime(f"{today} {end_hour}", "%m-%d-%y %H:%M").timestamp()
    LOOP_TIME = 600

SLEEP_TIME = 10  # general sleep time for webdriver actions (replace with event-based sleep)
browser_active = False

while True:
    current_time = time()
    # run main script if within specified operational time and there isn't an active browser
    if START_TIME <= current_time <= END_TIME and not browser_active:
        browser_active = True
        #TODO Get environment variables to work
        bearer_headers = {
            # "Authorization": f"Bearer {os.environ['SHEETY_TOKEN']}"
            "Authorization": "Bearer vutube"
        }

        try:
            # sheet_endpoint = os.environ["SHEET_ENDPOINT"]
            sheet_endpoint = "https://api.sheety.co/ab5f25ac623f26b2893bcf4dc383176c/dadTvSchedule/schedule"
            schedule_data = requests.get(sheet_endpoint, headers=bearer_headers).json()["schedule"]
            # for testing code to conserve sheety api requests
            # raise Exception
        except BaseException:
            print("Sheety API call failed. Using default schedule.")
            schedule_data = pd.read_csv("Dad TV Schedule.csv")

        df = pd.DataFrame(schedule_data)
        # subtract one to shift weekday values in line with 0-based index
        videos = df[df.columns[datetime.today().weekday() - 1]].values

        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.youtube.com/")

        for video in videos:
            search = WebDriverWait(driver, SLEEP_TIME).until(EC.visibility_of_element_located((By.NAME, "search_query")))
            search.clear()
            search.send_keys(video)
            search.send_keys(Keys.ENTER)

            video_title = WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.LINK_TEXT, video)))
            hover = ActionChains(driver)
            hover.move_to_element(video_title).perform()
            queue_button = WebDriverWait(driver, SLEEP_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytd-thumbnail-overlay-toggle-button-renderer[aria-label="Add to queue"]')))
            queue_button.click()

        expand_button = WebDriverWait(driver, SLEEP_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Expand (i)"]')))
        expand_button.click()
        # TODO add functionality to check if video is currently playing (don't want to accidentally pause video
        play = WebDriverWait(driver, SLEEP_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-large-play-button")))
        play.click()
        fullscreen = WebDriverWait(driver, SLEEP_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[title="Full screen (f)"]')))
        fullscreen.click()
    elif (current_time >= END_TIME or current_time <= END_TIME) and browser_active:
        driver.quit()
        browser_active = False

    sleep(LOOP_TIME)

# TODO create exception handling for when expected items don't show up
# e.g. the searched video doesn't exist or can't be found, things aren't loading, etc.
# TimeoutExceptions
# catch selenium.common.exceptions.WebDriverException: Message: chrome not reachable
# exception and relaunch script (happens whenever browser closes mid script)
