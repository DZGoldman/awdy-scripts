import time
from selenium.webdriver.support.ui import WebDriverWait


default_page_load_wait_time = 2

def attempt_find_element(cb, driver, wait_time=10):
    '''
    Wrapper to use with 'find_element' methods. wait_time can be overridden for particularly persnickety cases.
    use : lib.attempt_find_element( lambda: find_element_by_id('#interesting_data'), driver = driver)
    '''
    return WebDriverWait(driver, wait_time).until(lambda x: cb())

def percentage_string_to_float(st):
    return float(st.replace('%', '').strip())