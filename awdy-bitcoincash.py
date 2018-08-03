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
import ipdb
###################################################
# Number of entities controllong consensus
###################################################
driver.get('https://cash.coin.dance/blocks/today')
time.sleep(lib.default_page_load_wait_time) 
tspan_objects =   lib.attempt_find_element( lambda: driver.find_element_by_id('chartobject-1').find_elements_by_css_selector('tspan'), driver = driver)
a = []
for span in tspan_objects:
    text = span.text
    if ',' in text:
        s = text.split(',')[1].replace('%', '').strip()
        a.append(float(s))
# print(sum(a))
consensus_distribution = lib.get_cumulative_grouping_count(a, .5)
print('BCH consensus dist', consensus_distribution)
###################################################
# Wealth distribution
###################################################

driver.get("https://bitinfocharts.com/top-100-richest-bitcoin%20cash-addresses.html");
time.sleep(lib.default_page_load_wait_time) 

# Get data from page
tables =  lib.attempt_find_element( lambda: driver.find_elements_by_css_selector("#tblOne, #tblOne2"), driver)
rows = []
for table in tables:
        rows += table.find_elements_by_css_selector('tr')
# find % row
percentages = []
for row in rows[1:]:
    columns = row.find_elements_by_css_selector('td')
    percentages.append(float(columns[3].get_attribute('data-val')))
wealth_distribution = sum(percentages)

print('BCH % money held by 100 accounts:', wealth_distribution)

#next two are carbon copy of the methods for BTC, just at the BCH URL:
###################################################
# Client Codebases
###################################################
driver.get("https://cash.coin.dance/nodes");
time.sleep(lib.default_page_load_wait_time) 
count_containers = lib.attempt_find_element( lambda: driver.find_elements_by_css_selector(".nodeCountBlock > h3 > .nodeTitle > strong"), driver=driver)
all_counts = [int(container.text) for container in count_containers]
client_codebases = lib.get_cumulative_grouping_count(all_counts, .9)


print('BCH codebases over 90%:', client_codebases)
###################################################
# Public Nodes
###################################################

node_count_container = lib.attempt_find_element( lambda: driver.find_element_by_css_selector("[title].nodeTitle > strong"), driver=driver)
public_nodes_source = node_count_container.text

print('BCH node count:', public_nodes_source)

# Close the driver
driver.quit()