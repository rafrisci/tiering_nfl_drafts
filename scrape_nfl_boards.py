#!/usr/bin/env python3
"""
Use the big_board_scrape function in scrape_function.py to pull all NFL big boards
on jacklich10.xyz
"""
import scrape_function.py
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import os
os.path.isfile