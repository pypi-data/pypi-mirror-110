from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import random as r
import itertools
import time

def get_instance(headless=True, proxies=[], cookie:dict=None) -> webdriver:
    '''
    Open new tab in Chrome
    PARAMETERS:
        headless = True to run as Headless mode
        proxies = [IP:PORT or HOST:PORT] e.g. ['23.23.23.23:3128', '23.23.23.23:3129']
            If proxy required authen, you need to follow this format: 'scheme://user:pass@host:port'
    '''
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("start-maximized")
    options.add_argument('--disable-dev-shm-usage'); # overcome limited resource problems
    options.add_argument('--no-sandbox'); # Bypass OS security model

    # Bypass notification
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications" : 2})

    if proxies:
        options.add_argument('--proxy-server=%s' % random.choices(proxies))
    
    if headless:
        options.add_argument('--headless')
        
        # Minimal logs - FATAL only
        options.add_argument('--hide-scrollbars')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3') 
    
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
    if cookie:
        driver.add_cookie(cookie)

    return driver



def scroll_down(driver, height = 0):
    driver.execute_script('window.scrollTo({}, document.body.scrollHeight);'.format(height))


def scroll_down_bottom(driver, scroll_increment=300, timeout=10, expandable_button_selectors=[]):
    current_height = 0

    while True:
        for name in expandable_button_selectors:
            try:
                driver.find_element_by_css_selector(name).click()
            except Exception as e:
                # print(f'WARNING: Something wrong but OK with message: {str(e)}')
                pass

        # Use JQuery to click on invisible expandable 'see more...' elements
        driver.execute_script('document.querySelectorAll(".lt-line-clamp__ellipsis:not(.lt-line-clamp__ellipsis--dummy) .lt-line-clamp__more").forEach(el => el.click())')

        # Scroll down to bottom
        new_height = driver.execute_script('return Math.min({}, document.body.scrollHeight)'.format(current_height + scroll_increment))
        if (new_height == current_height):
            break
        
        scroll_down(driver, new_height)
        current_height = new_height

        # Wait to load page
        time.sleep(r.randrange(start=0, stop=30, step=1) / 1000)


def browse(driver, element_id=None) -> webdriver:
    if element_id is not None:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_id)))

    for _ in itertools.repeat(object=None, times=3):
        scroll_down(driver)
        time.sleep(r.randrange(start=0, stop=30, step=1) / 1000)

    scroll_down_bottom(driver)


def get_page_source(driver) -> str:
    return driver.page_source


def click(driver, e) -> str:
    action = ActionChains(driver)
    action.move_to_element(e).click(e).perform()