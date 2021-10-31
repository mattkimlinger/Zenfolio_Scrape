from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
from time import sleep
import os

######################### PROGRAM CONFIG #########################
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
ZEN_PATH = os.environ.get("ZEN_PATH")
ZEN_PAGE_PATH = ZEN_PATH + '/e/p'
ZEN_USERNAME = os.environ.get("ZEN_USERNAME")
ZEN_PASSWORD = os.environ.get("ZEN_PASSWORD")
zenHome_URL = 'https://www.zenfolio.com/' + ZEN_PATH + '/e/all-photos.aspx'
Failed_Urls = []
print(ZEN_USERNAME)
print(ZEN_PASSWORD)
print(ZEN_PATH)
print(ZEN_PAGE_PATH)
def printTime(preText):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(preText, current_time)

CURRENT_DIR = os.getcwd()
DOWNLOAD_DIR = CURRENT_DIR + '\Album_Downloads' 
print('DOWNLOAD DIRECTORY: ', DOWNLOAD_DIR)

def enable_download_headless(browser, download_dir):
# function to take care of downloading files
    try:
        browser.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')
        params = {
            'cmd': 'Page.setDownloadBehavior',
            'params': {
                'behavior': 'allow',
                'downloadPath': download_dir
            }
        }
        browser.execute("send_command", params)
    except Exception as e:
        print('enable_download_headless', e)

######################### DRIVER CONFIG #########################
DRIVER_PATH = CURRENT_DIR +'\chromedriver.exe'  #put your driver here
s = Service(DRIVER_PATH)
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.headless = False
chrome_options.add_argument("--window-size=400,800")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument("--log-level=2")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--disable-software-rasterizer')
# chrome_options.add_argument("user-data-dir=Zenfolio")
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "./Album_Downloads",
        "download.prompt_for_download": False,  #disable download prompt 
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
driver = webdriver.Chrome(options=chrome_options, service=s)
driver.maximize_window()
enable_download_headless(driver, DRIVER_PATH)

#XPaths
UsrnmeX = '/html/body/div[2]/div/div[1]/form/div[2]/div/input'
passX = '/html/body/div[2]/div/div[1]/form/div[3]/div/input'
submitButtonX = '/html/body/div[2]/div/div[1]/form/div[5]/a[2]'
allPhotosDirX = '//*[@id="_acaa"]/div[2]/div[8]'
allPhotosDirContainerX = '/html/body/div[2]/div[1]/div[3]/div[1]/div[2]/div/div[2]/div[8]'
selectAllPhotosX = '/html/body/div[2]/div[2]/div/div[6]/div/span/a[1]'
photoActionsX = '/html/body/div[2]/div[2]/div/div[2]/a[1]'
downloadOriginalFilesX = '//*[@id="ui-id-21"]'
downloadOriginalFileX = '//*[@id="ui-id-20"]'
photosContainerX = '//*[@id="_adc"]'
photosContainerFullX = '/html/body/div[2]/div[2]/div/div[5]/div[1]/div[2]/div[1]/div'

######################## LOGIN ################################
try:
    driver.get(zenHome_URL)
    printTime('Starting Zenfolio Scrape Logging in at')
    driver.get(zenHome_URL)
    UsernameElement = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, UsrnmeX)))
    print('entering username')
    UsernameElement.send_keys(ZEN_USERNAME)  #Enter in Login Username
    PasswordElement = driver.find_element(By.XPATH, passX)
    print('entering password')
    secure_pass = ZEN_PASSWORD
    print('secure_password: ', secure_pass)
    PasswordElement.send_keys(secure_pass)  #Enter in passwd
    SubmitElement = driver.find_element(By.XPATH, submitButtonX)
    SubmitElement = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, submitButtonX)))
    print('submitting..')
    SubmitElement.click()  #Submit Credentials
    sleep(10)
except Exception as e:
    print('Error Logging in to Zenfolio!', e)

###################### OPEN ALL MARGIN DIRECTORIES #######################
def expand_dirs():
    try:
        TreeButtons = driver.find_elements(By.CLASS_NAME, 'tree-collapsed')
        if TreeButtons:
            print('found more buttons with "tree-collapsed" class')
            for CollapsedFolder in TreeButtons:
                OpenFolderIcon = CollapsedFolder.find_element(
                    By.CLASS_NAME, "tree-btn")
                OpenFolderIcon.click()
                sleep(.5)
            return False
        else:
            return True
    except Exception as e:
        print('expand_dirs', e)

#Allow up to 6 sub directories expansion passes in "All Photographs" before error
def expand_all_directories():
    try:
        firstExp = expand_dirs()
        if not firstExp:
            print('First Expansion completed')
            secondExp = expand_dirs()
            if not secondExp:
                print('Second Expansion completed')
                thirdExp = expand_dirs()
                if not thirdExp:
                    print('Third Expansion completed')
                    fourthExp = expand_dirs()
                    if not fourthExp:
                        print('Fourth Expansion completed')
                        fifthExp = expand_dirs()
                        if not fifthExp:
                            print('Fifth Expansion completed')
                            sixthExp = expand_dirs()
                            if not sixthExp:
                                print(
                                    "Error: Maximun folder depth reached ('tree-collapsed' class searched 6 times) Adjust code, add more 'if's if this error code is seen"
                                )
                                return False
        print('expand_all_directories: True')
        return True
    except Exception as e:
        print('expand_all_directories', e)

################### GATHER ALBUM URLS #######################
# Create Album URL list
AlbumLinks = []
try:
    dirs_expanded = expand_all_directories()#Expand Folders
    if dirs_expanded:
        DirTree = driver.find_element(By.XPATH, allPhotosDirX)
        PotentialHrefs = DirTree.find_elements(By.TAG_NAME,'a')#Find all a tags
        for PotentialHref in PotentialHrefs: #loop to only match <a> w/ hrefs
            LinkHref = PotentialHref.get_attribute("href")
            if ZEN_PAGE_PATH in LinkHref: #only find user page hrefs
                AlbumLinks.append(LinkHref)
                print('Link Found: ', LinkHref)
    else:
        print('Directories could not expand!')
except Exception as e:
    print('Could not create URLS!', e)
print('Number of Links Found: ', len(AlbumLinks))

################### DOWNLOAD ZIP FILES #######################
try:
    for AlbumLink in AlbumLinks:
        try:
            print('Getting New Link')
            driver.get(AlbumLink)
            sleep(3)
            print('Clicking All Photos')
            driver.find_element(By.XPATH, selectAllPhotosX).click()
            sleep(1)
            print('Clicking Photo Actions')
            driver.find_element(By.XPATH, photoActionsX).click()
            sleep(1)
            try: #This route will depend if album photo count > 1
                driver.find_element(By.XPATH, downloadOriginalFilesX).click()#Try clicking "Download Original Files"
            except:
                print('Could not click Download Button, trying other type..')
                driver.find_element(By.XPATH, downloadOriginalFileX).click()#Try clicking "Download Original File"
            sleep(5)
        except Exception as e:
            Failed_Urls.append(AlbumLink)
            print('Problem Downloading Zip file: ' + AlbumLink + 'ERROR: ', e)
except Exception as e:
    print('Problem Downloading Zip files, ', e)


print('Program End.')
None if len(Failed_Urls) == 0 else print('Errors: ', Failed_Urls)
print('Exiting Chrome Driver in 10 minutes... make sure downloads have finshed before closing browser')
sleep(600)

driver.quit()
