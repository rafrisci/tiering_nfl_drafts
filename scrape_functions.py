from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

#initiate driver
driver = webdriver.Chrome()
driver.get('https://jacklich10.xyz/' + '/bigboard/nfl/')
#filter by year selected
parent_filters = driver.find_element(By.CLASS_NAME, 'well')
filters = parent_filters.find_elements(By.CLASS_NAME, 'row')
year_filt = Select(filters[0].find_element(By.CLASS_NAME, 'selectpicker'))
# Where year goes in
year_filt.select_by_value("2017")
driver.find_element(By.ID, 'update').click()
element = WebDriverWait(driver, 10).until(
    EC.all_of(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'recalculating')),
        EC.visibility_of_element_located((By.CLASS_NAME, 'rt-page-size-select')),
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'rt-tr-group')))
    )
)
#show max number of rows to minimize loops
rows_dropdown = Select(driver.find_element(By.CLASS_NAME, 'rt-page-size-select'))
rows_dropdown.select_by_value("200")

#get headers
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'rt-tr-header')))
header = driver.find_element(By.CLASS_NAME, 'rt-tr-header')
header_vals = header.find_elements(By.CLASS_NAME, 'rt-text-content')
col_names = []
for cell in header_vals:


pageSelector = driver.find_element(By.CLASS_NAME, 'rt-pagination-nav')
pages = pageSelector.find_elements(By.CLASS_NAME, 'rt-page-button')
skips = [0, len(pages) - 1]

for i in range(len(pages)):
    if i in skips:
        continue
    else:
        pages[i].click()

driver.quit()

#to do:
#get headers
#get body