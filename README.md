# Zenfolio Scrape

This program will automatically download all content from your zenfolio account,
just create a .env file with your credentials and watch the magic happen!

Created by: Matt Kimlinger <br/>
Mattkimlinger@gmail.com <br/>
https://github.com/mattkimlinger/Zenfolio_Scrape

## HOW TO USE

Designed and tested on a Window's Machine. Driver configurations may 
need to change in order to work on other machines

### Prerequisites:
* python 3 installed
### Install Packages
pip install selenium

### Create ENV
1. create new '.env' file in root directory
2. create these variables with your values<br/>
    ZEN_USERNAME=johndoe@gmail.net<br/>
    ZEN_PASSWORD=password1<br/>
    ZEN_PATH=johndoe<br/>

ZEN_PATH FOUND AT
https://www.zenfolio.com/johndoe/e/p773939117

## How to Run 
npm start

##
## If Chrome driver does not work <br/>Install Chrome Driver & replace path
1. Find your current chrome version type - chrome://settings/
2. download the corresponding driver from
https://chromedriver.chromium.org/downloads
3. replace the driver './chromedriver.exe' with newly downloaded one
