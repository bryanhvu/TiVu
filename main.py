from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

SLEEP_TIME = 3

#TODO get videos from sheety API
videos = [
    "Adele - Hello",
    "Full Chair Workout - No Equipment, Seated | More Life Health",
    "Paris By Night 73 - Song Ca Đặc Biệt / The Best of Duets (Full Program)"
]

#TODO Play videos listed in sheets based on day/other criteria

#TODO get updated webdriver automatically to match browser version
service = Service(executable_path="/Development/chromedriver")
driver = webdriver.Chrome(service=service)

#TODO make more robust wait commands/conditions
driver.implicitly_wait(15)
driver.get("https://www.youtube.com/")

for video in videos:
    search = driver.find_element(by="name", value="search_query")
    sleep(SLEEP_TIME)
    search.clear()
    search.send_keys(video)
    search.send_keys(Keys.ENTER)

    sleep(SLEEP_TIME)
    # add some handling for when element doesn't show (maybe already handled with implicitly_wait
    video_title = driver.find_element(by="link text", value=video)
    hover = ActionChains(driver)
    hover.move_to_element(video_title).perform()
    sleep(2)
    queue_button = driver.find_element(by="css selector", value='ytd-thumbnail-overlay-toggle-button-renderer[aria-label="Add to queue"]')
    queue_button.click()

sleep(SLEEP_TIME)
expand_button = driver.find_element(by="css selector", value='button[title="Expand (i)"]')
expand_button.click()
sleep(SLEEP_TIME)
play = driver.find_element(by="css selector", value=".ytp-large-play-button")
play.click()
fullscreen = driver.find_element(by="css selector", value='button[title="Full screen (f)"]')
fullscreen.click()

# TODO Setup browser quitting
# specific implementation might depend on how I choose to automatically execute this script
# or look up other ways to close existing browsers and have that run first
# driver.quit()




