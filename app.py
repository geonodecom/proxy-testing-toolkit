import os
from dotenv import load_dotenv
from seleniumwire import webdriver  
from selenium.webdriver.chrome.options import Options


load_dotenv()

proxy_host = 9000
proxy_port = '92.204.164.15'
username = 'geonode_demouser'
password = 'demopass'
GEONODE_DNS = 'proxy.geonode.io'

proxy_options = {
    'proxy': {
        'http': f'http://{username}:{password}@{proxy_host}:{proxy_port}',
        'https': f'https://{username}:{password}@{proxy_host}:{proxy_port}',
    }
}



chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--ignore-certificate-errors')

browser = webdriver.Chrome(seleniumwire_options=proxy_options, options=chrome_options)


urlToGet = "https://ip-api.com/"
browser.get(urlToGet)


input("Press Enter to close the browser...")

browser.quit()


