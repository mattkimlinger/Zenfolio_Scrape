#CREATED BY: MATT KIMLINGER
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys


DRIVER_PATH = 'C:/Users/Mkiml/Documents/installs/chromedriver.exe'

s=Service(DRIVER_PATH)

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--log-level=3")


driver = webdriver.Chrome(options=options, service=s)
driver.maximize_window()
driver.get('https://www.google.com')

xPath = '/html/body/div[1]/div[1]/a[1]'

print('This test pulls the text from the select xpath')
print('in this case its the About link on the home page ')
print('of google. displayed below is the text that is grabbed.')
print('')
print('')
xPathValue = driver.find_element('xpath', xPath)
# xPathValue  = driver.find_element_by_xpath("//*[contains(text(),'About')]")
print(xPathValue.text)
sys.stdout.flush()


driver.quit()