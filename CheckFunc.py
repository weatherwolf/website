from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
import numpy as np
import time
from selenium.webdriver.chrome.options import Options



countryList = np.array(["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT", "LU", "LT", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK", "XI"])

options = Options()
options.headless = True #Change to False if you want it to happen visually
options.add_argument("--start-naximized") #Headless = True
    
driver = webdriver.Chrome(options=options)

errorMessage = 'DO BY HAND'

def VATNumberValid(VATNumber):
    selectCountry = "none"
    for country in countryList:
        if country in VATNumber:
            selectCountry = country
            split = VATNumber.split(country, 1)
            VATNumber = str(split[1])
            break
    if selectCountry == "none": #If selectCountry == "none", break of program and tell VAT number doens' exist
        return f"{errorMessage}"

    #Going to website
    driver.get('https://ec.europa.eu/taxation_customs/vies/#/vat-validation')


    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="select-country"]')))
        #Fill in the country of the recipient
        time.sleep(1)
        select_country = Select(driver.find_element(By.XPATH, '//*[@id="select-country"]'))
        select_country.select_by_value(selectCountry)
    except: 
        return "DO BY HAND"


    #fill in BTW of recipient
    select_VAT_Number = driver.find_element(By.XPATH, '//*[@id="vat-validation-form"]/div/div[2]/input')
    select_VAT_Number.send_keys(VATNumber)
    select_VAT_Number.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'valid'))
            )
        return "YES"
    except:
        pass
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'FAQ'))
            )
        return "INCORRECT BTW"
    except:
       pass
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'invalid'))
            )
        return "DATABASE DOWN"
    except:
        pass
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'FAQ'))
            )
        return "INCORRECT BTW"
    except:
        return "SITE NOT LOADING"


def MakeDatabase(inputfile):
    btwNummers = []
    outputs = []
    csv_file = "test.csv" #xlsx file compressed to an csv file
    database_down_country = "none"
    countryList = np.array(["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK", "XI"])

    read_file = pd.read_excel (fr'/home/wolf/Documents/VAT Number/{inputfile}')
    read_file.to_csv(fr'/home/wolf/Documents/VAT Number/{csv_file}', index = None, header=True)

    with open(f'{csv_file}') as csv_file:
            for vatNumber in csv_file:
                
                if database_down_country in vatNumber:
                    btwNummers.append(str(vatNumber.strip('\n')))
                    outputs.append("DATABASE DOWN")
                else:
                    output = VATNumberValid(vatNumber)
                    while (output == f"{errorMessage}"):
                        output = VATNumberValid(vatNumber) #sometimes site wont load, so run the same number again until other output
                    btwNummers.append(str(vatNumber.strip('\n')))
                    outputs.append(output)
                    if output == "DATABASE DOWN":
                        for country in countryList:
                            if country in vatNumber:
                                database_down_country = country
    return pd.DataFrame(data={"VAT NUMBER" : btwNummers, "OUTPUT": outputs})