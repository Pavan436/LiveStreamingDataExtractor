from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd


def chrome_connection(headless=True):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options)
    return driver


def data_extractor():
    MaxRetries = 10
    driver = chrome_connection(headless=True)
    driver.get('https://bitcasino.io/#login')
    element = driver.find_element_by_xpath(
        "//*[@id='modal']/div/div/div[1]/div/div[1]/form/div[1]/div[1]/input")
    username = 'm12345'
    element.send_keys(username)
    time.sleep(2)
    password = 'M@12345'
    element = driver.find_element_by_xpath(
        "//*[@id='modal']/div/div/div[1]/div/div[1]/form/div[1]/div[2]/input")
    element.send_keys(password)
    time.sleep(2)
    element = driver.find_element_by_xpath("//*[@id='submitLoginButton']")
    element.click()
    time.sleep(5)

    for i in range(MaxRetries):
        try:
            login_page = driver.find_element_by_xpath(
                '//*[@class="sc-pTHAw jzutTq"]')
            break
        except:
            time.sleep(3)
            pass
    print("Entered into the LoginPage ")

    driver.get(
        'https://bitcasino.io/casino/bombay-club-baccarat/bombay-club-speed-baccarat-1')
    time.sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    main_streaming_link = soup.find("iframe", {"id": "gameIframe"})["src"]
    driver.get(main_streaming_link)
    time.sleep(3)
    videostream_page_source = driver.page_source
    print("Video Streaming")
    videostream_soup = BeautifulSoup(videostream_page_source, 'html.parser')
    data = videostream_soup.find(
        "div", {"class": "bead-road--lBdbG"}).getText()
    print("Collected Data")
    df = pd.DataFrame(list(data), columns=["Stroke1"])
    df.to_csv("bitcasino_data.csv")
    print("Saved into a CSV file")
    return "Sucessfully Completed the task"
