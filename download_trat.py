from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path, PureWindowsPath
from selenium.webdriver.firefox.options import Options
import os
from time import sleep

def rename_result_files(session_no):
    try:
        os.rename(fr'Session {session_no}\analyse_results.csv',fr'Session {session_no}\q1.csv')
        os.rename(fr'Session {session_no}\analyse_results(1).csv',fr'Session {session_no}\q2.csv')
        os.rename(fr'Session {session_no}\analyse_results(2).csv',fr'Session {session_no}\q3.csv')
    except:
        pass

def download_trat_results(session):
 
    download_dir = fr'C:\Users\a-vanniekerk\OneDrive - UWE Bristol\UWE\2020_2021\UFMFMS30-1 Dynamics, Modelling, and Simulation\TBL-data-extractor\Session {session}'
   
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for i in range(1,4):
        if os.path.exists(download_dir+fr"\q{i}.csv"):
            os.remove(download_dir+fr"\q{i}.csv")

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.dir", download_dir)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-download")

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(firefox_profile=fp, options=options)
    driver.get("https://dewisprod.uwe.ac.uk/cgi-bin/fixed/2022/secure/management/first.cgi?uweEND")
    driver.find_element_by_id("uweusername").send_keys("USERNAME")
    driver.find_element_by_xpath('/html/body/div/div[5]/div/form[1]/div/input[2]').send_keys("PASSWORD")
    driver.find_element_by_xpath('//*[@id="mainForm"]/div/button').click()
    driver.find_element_by_xpath('/html/body/div/div[5]/div/span[6]/span[1]').click()
    driver.find_element_by_xpath('/html/body/div/div[5]/div/button[2]').click()
    driver.find_element_by_xpath('/html/body/div/div[5]/div/button[2]').click()

    for i in range(1,4):
        driver.find_element_by_xpath(f'//*[contains(text(), "trat{session}_{i}")]').click() #Select test
        if i == 1:
            buttons = driver.find_elements_by_class_name('button1')
            for i in range(0,len(buttons)):
                if buttons[i].text == "Goto Reporter":
                    buttons[i].click() #Select "Go to reporter"
                    break
        driver.find_element_by_xpath('/html/body/div/div[5]/div/div[3]/button[1]').click() # Select "Analyse results"
        driver.find_element_by_xpath('/html/body/div/div[5]/div/div[2]/button').click() # Select "Download CSV"
        if i != 3:
            driver.find_element_by_xpath('/html/body/div/div[2]/div/div/span[4]').click() # Select "Reporter"

    driver.quit()
    rename_result_files(session)
