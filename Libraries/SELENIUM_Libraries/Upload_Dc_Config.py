
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
from xml.etree import ElementTree

import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Locators = os.path.dirname(parrent_path.parent.absolute()) + os.path.sep + "Resources/PageObject/Locators";
Locators2 = Locators.replace('\\', '/')
sys.path.append(Locators2)
from Locators import Locator
Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)
import Log
import ReadConfigFile as conf







def import_dc_config(driver, PROJECT, conf_name):
    path = Path(os.path.abspath(__file__))
    parrent_path = path.parent.absolute()
    parrent_path = parrent_path.parent.absolute()
    ssf_path = os.path.dirname(parrent_path) + os.path.sep + "Resources"
    print(ssf_path+'\\UPLOAD\\')
    ssf_path= ssf_path +'\\UPLOAD\\'+ PROJECT +'\\'+conf_name+'.zip'
    driver.find_element_by_link_text('Configuration File').click()
    time.sleep(2)
    driver.find_element_by_link_text('Create New Configuration File').click()
    time.sleep(2)

    drag_sff= driver.find_element_by_id("file-import")
    drag_sff.send_keys(ssf_path)
    driver.find_element_by_id("import-confirm").click()
    upload= driver.find_element_by_xpath("/html/body/ngb-modal-window/div/div/div[3]/button[2]")
    upload.click()
    return True

def import_dc_fw(driver, PROJECT, conf_name):
    path = Path(os.path.abspath(__file__))
    parrent_path = path.parent.absolute()
    parrent_path = parrent_path.parent.absolute()
    ssf_path = os.path.dirname(parrent_path) + os.path.sep + "Resources"
    print(ssf_path+'\\UPLOAD\\')
    ssf_path= ssf_path +'\\UPLOAD\\'+ PROJECT +'\\'+conf_name+'.zip'
    driver.find_element_by_link_text('Firmware Library').click()
    time.sleep(2)
    driver.find_element_by_link_text('Create New Firmware').click()
    time.sleep(2)

    drag_sff= driver.find_element_by_id("file-import")
    drag_sff.send_keys(ssf_path)
    driver.find_element_by_id("import-confirm").click()
    upload= driver.find_element_by_xpath("/html/body/ngb-modal-window/div/div/div[3]/button[2]")
    upload.click()
    return True
