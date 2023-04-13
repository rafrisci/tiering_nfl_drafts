from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://jacklich10.xyz/' + '/bigboard/nfl/')

#year = driver.find_element(By.XPATH, '//input[@for="year"]')
#year.get_attribute()

driver.find_element(By.ID, 'update').click()
rows_dropdown = Select(driver.find_element(By.CLASS_NAME, 'rt-page-size-select'))
rows_dropdown.select_by_value("200")
parent_filters = driver.find_element(By.CLASS_NAME, 'well')
filters = parent_filters.find_elements(By.CLASS_NAME, 'row')
year_dropdown = Select(filters[0].find_element(By.CLASS_NAME,
                                               'dropdown bootstrap-select form-control bs3'))

pageSelector = driver.find_element(By.CLASS_NAME, 'rt-pagination-nav')
pages = pageSelector.find_elements(By.CLASS_NAME, 'rt-page-button')
skips = [0, len(Pages) - 1]
for i in range(len(Pages)):
    if i in skips:
        continue
    else:
        Pages[i].click()



print(len([my_elem.get_attribute("aria-current") for my_elem in Page.find_elements(By.CLASS_NAME, "rt-page-button")]))

driver.quit()
