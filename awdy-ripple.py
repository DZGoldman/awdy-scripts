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
# Page sometimes requries more time to load
time.sleep(3) 
public_nodes_source = driver.find_element_by_class_name('nNodes').text
print('XRP public node count:', public_nodes_source)

###################################################
# Client Codebases
###################################################

# Get list of nodenames (filtering out empty divs)
node_codebases = [ node.text for node in driver.find_elements_by_css_selector('div.version') if node.text]
# Clean to just name, not version number - lazy solution atm, tho I suspect it won't be an issue any time soon ;)
node_codebases = [node_name.split('-')[0]  if '-' in node_name else node_name  for node_name in node_codebases]

# convert to list of tupples of form (node_name, count), in descending order
codebase_counts = defaultdict(int)
for codebase_name in node_codebases:
    codebase_counts[codebase_name] += 1
codebases_sorted_by_freq = sorted( 
    [(code_base, codebase_counts[code_base]) for code_base in codebase_counts], 
    key = lambda tup: tup[1],  reverse=True
    )
# iterate, upping percentages until we break 90% (this is probably overkill considering what we're dealing with, but hey)
total_percent = 0
for i, code_base_tup in enumerate(codebases_sorted_by_freq):
    total_percent =  code_base_tup[1] / len(node_codebases)
    if total_percent >= .9:
        client_codebases = i +1 
        break
print('XRP nodes that make up > 90% of codebases:', client_codebases)

driver.quit()