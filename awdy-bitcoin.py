import time
import pandas as pd
from selenium import webdriver

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

import lib

###################################################
# Number of entities controllong consensus
###################################################

driver.get("https://www.blockchain.com/pools?timespan=24hours");
time.sleep(lib.default_page_load_wait_time) 

# Get data from page
table = lib.attempt_find_element( lambda: driver.find_element_by_id("known_pools"), driver)
readtable = pd.read_html(table.get_attribute("outerHTML"), header=0, converters={"count": int})
pools = readtable[0]

# Do calculation
pools["cumulative_sum"] = pools["count"].cumsum()
pools["cumulative_percentage"] = 100 * pools["cumulative_sum"] / pools["count"].sum()

# Set the variable
consensus_distribution = pools[pools["cumulative_percentage"].gt(51)].index[0] + 1

print('BTC pools with total >50 % hashrate:', consensus_distribution)

###################################################
# Wealth distribution
###################################################

driver.get("https://bitinfocharts.com/bitcoin/");
time.sleep(lib.default_page_load_wait_time) 

# Get data from page
wealth_text = lib.attempt_find_element( lambda: driver.find_element_by_id("tdid18"), driver=driver).text
cleaned_text = wealth_text.replace(" ", "").split('/')
wealth_distribution = cleaned_text[1]

print('BTC % money held by 100 accounts:', wealth_distribution)

###################################################
# Client Codebases
###################################################
driver.get("https://coin.dance/nodes");
time.sleep(lib.default_page_load_wait_time) 
count_containers = lib.attempt_find_element( lambda: driver.find_elements_by_css_selector(".nodeCountBlock > h3 > .nodeTitle > strong"), driver=driver)
all_counts = [int(container.text) for container in count_containers]
client_codebases = lib.get_cumulative_grouping_count(all_counts, .9)


print('BTC codebases over 90%', client_codebases)
###################################################
# Public Nodes
###################################################

node_count_container = lib.attempt_find_element( lambda: driver.find_element_by_css_selector("[title].nodeTitle > strong"), driver=driver)
public_nodes_source = node_count_container.text

print('BTC node count:', public_nodes_source)

# Close the driver
driver.quit()