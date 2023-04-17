#!/usr/bin/env python3
"""
big_board_scrape scrapes the information from jacklich10.xyz concensus big boards
and returns it as a pandas df. It requires the year and league of the big board.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


def big_board_scrape(year, league = 'NFL'):
    """
    Get the draft big boards from jacklich10.xyz for either the NFL or NBA.

    Parameters
    ----------
        year: int
            the year of the draft to be scraped
        league: str
            the league of the big board to be scraped
    
    Returns
    -------
    pandas df
        A dataframe of the big board and all prospects included in it.
    """
    league = league.lower()
    if league not in ['nfl', 'nba']:
        raise ValueError('The only league big boards available on jacklich10.xyz',
                         'are the NBA and NFL.')
    #initiate driver
    driver = webdriver.Chrome()
    driver.get(f"https://jacklich10.xyz/bigboard/{league}/")
    #filter by year selected
    parent_filters = driver.find_element(By.CLASS_NAME, 'well')
    filters = parent_filters.find_elements(By.CLASS_NAME, 'row')
    year_filt = Select(filters[0].find_element(By.CLASS_NAME, 'selectpicker'))
    year_filt.select_by_value(str(year))
    element = WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'shiny-busy'))
    )
    #update table for appropriate year
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'update'))
    ).click()
    element = WebDriverWait(driver, 10).until(
        EC.all_of(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'recalculating')),
            EC.visibility_of_element_located((By.CLASS_NAME,
                                              'rt-page-size-select')),
            EC.element_to_be_clickable((By.CLASS_NAME, 'rt-tr-group'))
        )
    )
    #show max number of rows to minimize number of page changes
    rows_dropdown = Select(driver.find_element(By.CLASS_NAME,
                                               'rt-page-size-select'))
    rows_dropdown.select_by_value("200")
    #get column names
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'rt-tr-header'))
    )
    header = driver.find_element(By.CLASS_NAME, 'rt-tr-header')
    header_vals = header.find_elements(By.CLASS_NAME, 'rt-text-content')
    col_names = []
    for cell in header_vals:
        text = cell.text
        col_names.append(text)
    col_names[0:3] = ['Rank', 'Position', 'Name']
    #find page selection buttons
    pageSelector = driver.find_element(By.CLASS_NAME, 'rt-pagination-nav')
    pages = pageSelector.find_elements(By.CLASS_NAME, 'rt-page-button')
    #body of table info
    prospects = []
    for i in range(int(pages[-2].text)):
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'rt-tr-group'))
        )
        table = driver.find_element(By.CLASS_NAME, 'rt-tbody')
        rows = table.find_elements(By.CLASS_NAME, 'rt-tr-group')
        for row in rows:
            vals = row.find_elements(By.CLASS_NAME, 'rt-td-inner')
            out = []
            for j in range(len(vals)):
                if 1 <= j <= 2:
                    continue
                text = vals[j].text
                text = text.replace('\n', ' ')
                text = text.replace(' -', '')
                out.append(text)
            prospects.append(out)
        if i < int(pages[-2].text) - 1:
            pages[-1].click()
    driver.quit()
    #make the pandas df to return
    df = pd.DataFrame(prospects, columns=col_names)
    return df
