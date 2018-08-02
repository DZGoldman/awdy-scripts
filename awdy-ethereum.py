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
import re, json
import numpy as np
import lib

###################################################
# Public Node Count
###################################################
driver.get("https://www.ethernodes.org/network/1");
time.sleep(lib.default_page_load_wait_time) 
list_items = lib.attempt_find_element( lambda: driver.find_elements_by_css_selector(".pull-right.text-muted"), driver = driver)
# Get "total node" element (has 100% in text)
total_node_text = [e.text for e in list_items if '(100%)' in e.text][0]
# Extract count from string
public_nodes_source = re.sub("[\(\[].*?[\)\]]", "", total_node_text).strip()
print('Eth node count: ', public_nodes_source)

###################################################
# Client Codebases
###################################################

# Import pie chart canvas element 
client_graph =  lib.attempt_find_element( lambda: driver.find_element_by_class_name('ex-graph'), driver = driver)
# Extract stringified json
client_data_json_string = client_graph.get_attribute('data-value')
# Convert to dictionary
client_data_json = json.loads(client_data_json_string)
# Convert to Dataframe
client_data_df = pd.DataFrame(client_data_json)
# Sort values (values are node counts)
node_counts_sorted = client_data_df['value'].sort_values(ascending=False)
# Get series of percentages of total
cumulative_sum_percentages = node_counts_sorted.cumsum() / node_counts_sorted.sum()
# Find how many make > 90 %
client_codebases = np.where(cumulative_sum_percentages.gt(.9) )[0][0] +1
print('Eth codebases count:', client_codebases)


###################################################
# Wealth Distribution
###################################################

# get page with 100 elements
driver.get("https://etherscan.io/accounts/1?ps=100");
time.sleep(lib.default_page_load_wait_time)
table = lib.attempt_find_element( lambda: driver.find_element_by_css_selector(".table"), driver=driver)

# Read table as dataframe, sanitizing % column to float
readtable = pd.read_html(table.get_attribute("outerHTML"), header=0,  converters={"Percentage": lib.percentage_string_to_float } )[0]
# Sum of % column
wealth_distribution = readtable['Percentage'].sum()
print('ETH wealth distribution:', wealth_distribution)


###################################################
# Number of entities controllong consensus
###################################################
driver.get("https://etherscan.io/stat/miner?range=7&blocktype=blocks");
time.sleep(lib.default_page_load_wait_time)
table = lib.attempt_find_element( lambda: driver.find_element_by_css_selector(".table"), driver = driver)
# read table, sanitize percentage
readtable = pd.read_html(table.get_attribute("outerHTML"), header=0,  converters={"Percentage":lib.percentage_string_to_float } )[0]
# get cumulative sum series
cumulative_sum = readtable['Percentage'].cumsum()
# get index of first element where sum is > 50%
consensus_distribution = np.where(cumulative_sum.gt(50) )[0][0] + 1

print('Eth consensus distribution:', consensus_distribution)

driver.quit()