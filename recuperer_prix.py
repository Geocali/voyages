from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import sys
import datetime
from pathlib import Path

global driver
driver = webdriver.Firefox()

from sncf import *

city_start = "Paris+%28Toutes+gares+intramuros%29"
city_stop = "Marseille"
time_go = "17"
date_go = "21%2F09%2F2017"

def save_to_file(df_prices, fichier):
    my_file = Path(fichier)
    if my_file.is_file():
        df_prices.to_csv(fichier, header=False, index=False, mode='a+')
    else:
        df_prices.to_csv(fichier, header=True, index=False, mode='a+')

sncf = sncf(driver)
sncf.charger_page(city_start, city_stop, time_go, date_go)
prix_sncf = sncf.lire_page()
save_to_file(prix_sncf, "sncf_prices.csv")

driver.quit()
