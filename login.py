from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import login_site_address, site_email, site_password


def start():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    get_cookies(driver)

    return driver


def get_cookies(driver):
    driver.get(login_site_address)
    wait = WebDriverWait(driver, 10)

    email_handler = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/section/section/div/div[1]/form/div[1]/input')))
    email_handler.clear()
    email_handler.send_keys(site_email)

    password = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/section/section/div/div[1]/form/div[2]/input')))
    password.clear()
    password.send_keys(site_password)

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/section/section/div/div[1]/form/div[3]/button[2]')))
    login_button.click()
    cookies =  driver.get_cookie()
    driver.quit()
    return cookies
