import time
import pandas as pd
from selenium import webdriver
import html5lib
# These are the variables which must be calculated by the script. 
consensus_distribution = None
wealth_distribution = None
client_codebases = None
public_nodes_source = None

# Tell Selenium to run Chrome in headless mode, with a preset window size
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("window-size=1200x600")

# Start driver with specified options
driver = webdriver.Chrome(chrome_options=options) 

###################################################
######## ~ You can edit below this point ~ ########
###################################################

###################################################
# Wealth Distribution
###################################################
driver.get("https://ledger.exposed/rich-stats");
time.sleep(1) 
wealth_distribution = driver.find_element_by_css_selector('[data-v-ca88cbc2].large > b').text
print('XRP Wealth distribution:', wealth_distribution)

###################################################
# Public Node Count
###################################################
driver.get("https://xrpcharts.ripple.com/#/topology");
time.sleep(1) 
public_nodes_source = driver.find_element_by_class_name('nNodes').text
print('XRP public node count:', public_nodes_source)