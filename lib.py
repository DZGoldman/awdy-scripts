import time
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import numpy as np

default_page_load_wait_time = 2

def attempt_find_element(cb, driver, wait_time=10):
    '''
    Wrapper to use with 'find_element' methods. wait_time can be overridden for particularly persnickety cases.
    use : lib.attempt_find_element( lambda: find_element_by_id('#interesting_data'), driver = driver)
    '''
    return WebDriverWait(driver, wait_time).until(lambda x: cb())

def percentage_string_to_float(st):
    return float(st.replace('%', '').strip())

def get_cumulative_grouping_count(data, target_percentage):
    if isinstance(data, list):
        data = pd.DataFrame(data)[0]
        print(data)
    # Sort values (values are node counts)
    sorted_data = data.sort_values(ascending=False)
    # Get series of percentages of total
    cumulative_sum_percentages = sorted_data.cumsum() / sorted_data.sum()
    # Find how many make > 90 %
    return  np.where(cumulative_sum_percentages.gt(target_percentage) )[0][0] +1
