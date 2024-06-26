import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM

# print('=====================================================================================================')
# print('Heyy, you have to login manully on tiktok, so the bot will wait you 1 minute for loging in manually!')
# print('=====================================================================================================')
# time.sleep(8)
# print('Running bot now, get ready and login manually...')
# time.sleep(4)

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\omidh\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--auto-open-devtools-for-tabs")
RemoteConnection.set_timeout(30)
bot = webdriver.Chrome(options=options,  executable_path=CM().install())
bot.set_window_size(1680, 900)

# bot.get('https://www.tiktok.com/login')
# ActionChains(bot).key_down(Keys.CONTROL).send_keys(
#     '-').key_up(Keys.CONTROL).perform()
# ActionChains(bot).key_down(Keys.CONTROL).send_keys(
#     '-').key_up(Keys.CONTROL).perform()
# print('Waiting 50s for manual login...')
# time.sleep(50)
bot.get('https://www.tiktok.com/upload/?lang=en')
time.sleep(3)


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True


def upload(video_path):
    while True:
        time.sleep(1.5)
        # WebDriverWait(bot, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div[3]/button[1]')))
        # file_uploader = bot.find_element_by_xpath(
        #     "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div[3]/button[1]")
        iframe = bot.find_element_by_xpath('//iframe[@data-tt="Upload_index_iframe"]')
        bot.switch_to.frame(iframe)
        file_uploader = bot.find_element_by_xpath("//input[@type='file']")

        file_uploader.send_keys(video_path)
        time.sleep(2)
        caption = bot.find_element_by_xpath(
            "//div[@contenteditable='true']")

        bot.implicitly_wait(10)
        bot.execute_script("arguments[0].scrollIntoView(true);", caption)  # scrolls into view of caption
        print('moved')
        time.sleep(0.5)
        # ActionChains(bot).move_to_element(caption).click(
        #     caption).perform()

        # ActionChains(bot).key_down(Keys.CONTROL).send_keys(
        #     'v').key_up(Keys.CONTROL).perform()

        bot.execute_script("arguments[0].click();", caption)


        with open(r"caption.txt", "r") as f:
            tags = [line.strip() for line in f]

        for tag in tags:
            ActionChains(bot).send_keys(tag).perform()
            time.sleep(2)
            ActionChains(bot).send_keys(Keys.RETURN).perform()
            time.sleep(1)

        time.sleep(5)
        bot.execute_script("window.scrollTo(150, 300);")
        time.sleep(5)

        post = WebDriverWait(bot, 100).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[text()='Post']")))

        post.click()

        # post = WebDriverWait(bot, 100).until(
        #     EC.visibility_of_element_located(
        #         (By.XPATH, "//div[text()='Upload']")))
        # time.sleep(30)

        # if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
        #     reupload = WebDriverWait(bot, 100).until(EC.visibility_of_element_located(
        #         (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))
        #
        #     reupload.click()
        # else:
        #     print('Unknown error cooldown')
        #     while True:
        #         time.sleep(600)
        #         post.click()
        #         time.sleep(15)
        #         if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
        #             break
        #
        # if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
        #     reupload = WebDriverWait(bot, 100).until(EC.visibility_of_element_located(
        #         (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))
        #     reupload.click()
        #
        # time.sleep(1)


# ================================================================
# Here is the path of the video that you want to upload in tiktok.
# Plese edit the path because this is different to everyone.
upload(r"G:\omidh\Documents\Github\Tiktok-Automated\outputs\output1_subtitled.mp4")
# ================================================================
