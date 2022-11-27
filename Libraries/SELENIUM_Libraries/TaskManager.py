import sys
import time
import paramiko
import pandas as pd
import xml.etree.ElementTree as ET
import datetime
from robot.api import logger
from robot.output import librarylogger
#Log.log(os.getcwd())
from lxml import etree
from selenium.webdriver.support.select import Select
import lxml
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
# logging.basicConfig(filename="C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/std2.log",
#                             filemode='a',
#                             format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                             datefmt='%H:%M:%S',
#                             level=logging.DEBUG)


import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Locators = os.path.dirname(parrent_path.parent.absolute()) + os.path.sep + "Resources/PageObject/Locators";
Locators2 = Locators.replace('\\', '/')
sys.path.append(Locators2)

# sys.path.append('C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Resources/PageObject/Locators')
from selenium.webdriver.common.by import By
from Locators import Locator


Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)
import ReadConfigFile as conf
import Log

mon_dictionnaire = {}
mon_dictionnaire['S']='seconds'
mon_dictionnaire['MI']='minutes'
mon_dictionnaire['H']='hours'
mon_dictionnaire['D']='days'
mon_dictionnaire['MO']='months'
mon_dictionnaire['Y']='years'




def cancel_task(driver, task_id):
    Log.log("select task", task_id, 'INFO')
    for i in range(len(task_id)):
        retries = 1
        while retries <= 3:
            try:
                Log.log('open metering section' ,"", 'DEBUG')
                step1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, Locator.metering_task_id)))
                step1.clear()
                step1.send_keys(task_id[i])
                time.sleep(2)
                step2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locator.search_by_profile)))

                driver.execute_script("arguments[0].click();", step2)

                break
            except Exception as e:
                Log.log('TimeoutException' , e, 'DEBUG')
                driver.refresh()
                if retries ==3:
                    raise Exception(e)
                retries += 1

        retries = 1
        time.sleep(2)
        while retries <= 3:
            try:
                Log.log('click cancel' ,"", 'DEBUG')
                step3 =driver.find_elements_by_id(Locator.task_list_dropdownConfig)
                step3[2].click()
                step4=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.task_cancel_button)))
                step4.click()
                time.sleep(2)
                step5=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, Locator.Yes_modal_button)))
                step5.click()


                break
            except Exception as e:
                Log.log('TimeoutException' , e, 'DEBUG')
                driver.refresh()
                if retries ==3:
                    raise Exception(e)
                retries += 1

    return True
