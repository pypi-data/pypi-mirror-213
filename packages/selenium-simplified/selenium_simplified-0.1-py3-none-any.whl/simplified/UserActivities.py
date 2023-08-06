from selenium.webdriver.common.by import By
import time


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    original_style = element.get_attribute('style')
    apply_style("background: blue; border: 2px solid orange;")
    time.sleep(.3)
    apply_style(original_style)


class CommonActivities():
    def __init__(self,driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        return element

    def type_in_element(self,web_element,text):
        highlight(element=web_element)
        web_element.send_keys(text)

    def click_on_element(self,web_element):
        highlight(element=web_element)
        web_element.click()