from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
import sys
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

zwift_url = "https://www.zwift.com/settings/connections"
DISCONNECT = "Disconnect"
CONNECT = "Connect"
CONNECT_CLASS = "_2fJyAR0ARoDeRRmroezfrx"


def get_element(driver, by_method, value):
    """Add wait to find_element()."""
    element = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(by_method, value)
    )
    time.sleep(1) 
    return element


def read_config():
    """Read the config file."""
    with open("config.json", "r") as read_file:
        config = json.load(read_file)
        return config


def login_strava(driver, acc, config):
    """Login to Strava."""
    username = get_element(driver, By.ID, "email")
    username.send_keys(config["strava"][acc]["username"])

    password = get_element(driver, By.ID, "password")
    password.send_keys(config["strava"][acc]["password"])

    login = get_element(driver, By.ID, "login-button")
    login.click()


def login_zwift(driver, config):
    """Login to Zwift."""
    username = get_element(driver, By.ID, "username")
    username.send_keys(config["zwift"]["username"])

    password = get_element(driver, By.ID, "password")
    password.send_keys(config["zwift"]["password"])

    login = get_element(driver, By.ID, "submit-button")
    login.click()


# load the configuration
config = read_config()

with Chrome(chrome_options=chrome_options) as driver:
    driver.get(zwift_url)

    # login zwift
    login_zwift(driver, config)

    # cookie policy
    cookie_btn = get_element(driver, By.ID, "truste-consent-button")
    cookie_btn.click()

    strava_btn = get_element(driver, By.CLASS_NAME, CONNECT_CLASS)

    # disconnect first
    if strava_btn.text == DISCONNECT:
        strava_btn.click()
        WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.CLASS_NAME, CONNECT_CLASS).text == CONNECT
        )

    # click to connect
    strava_btn.click()

    # login_strava
    acc = sys.argv[1]
    login_strava(driver, acc, config)

    # authorize
    authorize = get_element(driver, By.ID, "authorize")
    authorize.click()

    strava_btn = get_element(driver, By.CLASS_NAME, CONNECT_CLASS)
    if strava_btn.text == DISCONNECT:
        print("SUCCESSFULLY SET!")

