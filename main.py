from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from dotenv import dotenv_values
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

secrets = dotenv_values(".env")
USERNAME_FB = secrets['USERNAME_FB']
PASSWORD_FB = secrets['PASSWORD_FB']

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# Open Tinder
driver.get('https://tinder.com/')
driver.implicitly_wait(3)

log_in = driver.find_element(By.LINK_TEXT, 'Log in')
log_in.click()
driver.implicitly_wait(8)

time.sleep(2)
more_option = driver.find_element(By.XPATH, value='//*[@id="c-1108700915"]/main/div/div/div[1]/div/div/div[2]'
                                                  '/div[2]/span/button')
if more_option:
    more_option.click()
    time.sleep(2)

log_with_fb = driver.find_element(By.CSS_SELECTOR, value='button[aria-label*=Facebook]')
log_with_fb.click()

# After clicking the 'login with Facebook' new window will be opened, so we need to switch window in selenium too:
tinder_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
print(driver.title)

# FB login credentials:
fb_username = driver.find_element(By.ID, 'email')
fb_username.send_keys(f'{USERNAME_FB}')

fb_password = driver.find_element(By.ID, value='pass')
fb_password.send_keys(f'{PASSWORD_FB}')

fb_login = driver.find_element(By.ID, value='loginbutton')
fb_login.click()
driver.implicitly_wait(10)

# switch back to tinder window after login:
driver.implicitly_wait(20)
driver.switch_to.window(tinder_window)
print(driver.title)
allow_location_track = driver.find_element(By.CSS_SELECTOR, value='button[aria-label*=Allow]')
if allow_location_track:
    allow_location_track.click()

enable_notification = driver.find_element(By.CSS_SELECTOR, value='button[aria-label*=Enable]')
if enable_notification:
    enable_notification.click()

accept_cookies = driver.find_element(By.XPATH, value='//*[@id="c619680161"]/div/div[2]/div/div/div[1]/div[1]/button')
if accept_cookies:
    accept_cookies.click()

time.sleep(25)
like_tinder = driver.find_element(By.XPATH, value='//*[@id="c619680161"]/div/div[1]/div/main/div[1]/div/div/div[1]'
                                                  '/div[1]/div/div[3]/div/div[4]/button')

for i in range(15):
    driver.implicitly_wait(7)
    try:
        print('Profile Liked !')
        # like a profile only if it is loaded
        like_tinder.click()
    except ElementClickInterceptedException:
        try:
            # hide pop up (it's a match)
            hide_its_a_match = driver.find_element(By.XPATH, '//*[@id="c-1089923421"]/div/div/div[1]/div/div'
                                                             '[4]/button')
            hide_its_a_match.click()

        except:
            # sometimes tinder shows (add to home screen pop up) so we need to click cancel
            add_tinder_home_screen = driver.find_element(By.XPATH,
                                                         '//*[@id="c1146291598"]/div/div/div[2]/button[2]/span')
            add_tinder_home_screen.click()
        # wait for two seconds for any of the above two exceptions and then click like button
        time.sleep(2)
        like_tinder.click()
        print('Profile Liked !')

    except NoSuchElementException:
        # if profile is not loaded yet, then wait for 2 more sec
        time.sleep(3)
        like_tinder.click()
        print('Profile Liked !')

driver.quit()
