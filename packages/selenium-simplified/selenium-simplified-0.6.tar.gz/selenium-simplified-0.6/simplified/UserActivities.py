from selenium.webdriver.common.by import By
import time
from datetime import datetime


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    original_style = element.get_attribute('style')
    apply_style("background: blue; border: 2px solid orange;")
    time.sleep(.3)
    apply_style(original_style)


class CommonActivities:
    def __init__(self,driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def find_element(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def type_in_element(self,web_element,text):
        highlight(element=web_element)
        web_element.send_keys(text)

    def click_on_element(self,web_element):
        highlight(element=web_element)
        web_element.click()

    def close_current_tab(self):
        self.driver.close()

    def close_browser(self):
        self.driver.quit()

    def click_screenshot(self, dir):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        current_date = dt_string.split(" ")[0].replace('/','_')
        current_time = dt_string.split(" ")[1].replace(':', '_')
        file_name = current_date+'_'+current_time.replace(':','_')+".png"
        self.driver.save_screenshot(dir+file_name)

