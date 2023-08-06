# Step 1 : install the library
# pip install selenium-simplified

# Step 2: import the library
from simplified import SeleniumSimplified

# Step 3 - Open the chrome browser
driver = SeleniumSimplified()

'''
Examples - Showing how to use SeleniumSimplified functions
Please Note - SeleniumSimplified uses XPATH only as its locator strategy
'''

# How to open a specific url
driver.open_url(url='https://www.google.com')
# How to find an element and type some text in it
driver.type_in_element(xpath="//*[@name='q']",text='selenium')
# How to find an element and click on it
driver.click_on_element(xpath="//*[@name='btnK']")
# How to take screenshot and save it inside the screenshot directory
driver.take_screenshot(dir='../screenshot/')
# how to get the current browser tab title
print(driver.get_tab_title())
# How to close the current browser tab
driver.close_current_tab()
# How to close browser
driver.close_browser()