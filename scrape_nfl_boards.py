"""
Use the big_board_scrape function in scrape_function.py to pull all NFL big boards
on jacklich10.com
"""
from scrape_function import big_board_scrape
import os
import pandas as pd

path = os.getcwd()
league = 'NFL'
for year in range(2016, 2024):
    df = big_board_scrape(year, league)
    df.to_csv(os.path.join(path, f'data\\big_boards\\{year}_big_board.csv'))