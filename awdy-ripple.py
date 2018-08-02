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
from collections import defaultdict
import lib

###################################################
# Wealth Distribution
###################################################
driver.get("https://ledger.exposed/rich-stats");
time.sleep(lib.default_page_load_wait_time) 
wealth_distribution =  lib.attempt_find_element( lambda:driver.find_element_by_css_selector('[data-v-ca88cbc2].large > b'), driver = driver).text
print('XRP Wealth distribution:', wealth_distribution)

###################################################
# Public Node Count
###################################################
# NOTE: this site is often unresponsive, maybe find another source?
driver.get("https://xrpcharts.ripple.com/#/topology");
# Page sometimes requries more time to load
time.sleep(5) 
nodes_element = lib.attempt_find_element( lambda:driver.find_element_by_class_name('nNodes'), driver = driver)
public_nodes_source =  nodes_element.text

###################################################
# Client Codebases
###################################################

# Get list of nodenames (filtering out empty divs)
node_version_divs =  lib.attempt_find_element( lambda: driver.find_elements_by_css_selector('div.version'), driver = driver) 
node_codebases = [ node.text for node in node_version_divs if node.text]
# Clean to just name, not version number - lazy solution atm, tho I suspect it won't be an issue any time soon ;)
node_codebases = [node_name.split('-')[0]  if '-' in node_name else node_name  for node_name in node_codebases]

# convert to list of tupples of form (node_name, count), in descending order
codebase_counts_dict = defaultdict(int)
for codebase_name in node_codebases:
    codebase_counts_dict[codebase_name] += 1
codebase_counts_list = list(codebase_counts_dict.values())
client_codebases = lib.get_cumulative_grouping_count(codebase_counts_list, .9)
print('XRP nodes that make up > 90% of codebases:', client_codebases)

driver.quit()