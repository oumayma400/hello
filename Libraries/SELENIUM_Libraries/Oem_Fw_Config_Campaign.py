from datetime import datetime
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
from selenium.webdriver.common import action_chains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Locators = os.path.dirname(parrent_path.parent.absolute()) + os.path.sep + "Resources/PageObject/Locators";
Locators2 = Locators.replace('\\', '/')
sys.path.append(Locators2)
from Locators_Fluvius import Locator_Fluvius
from Locators import Locator
# /html/body/app-root/app-full-layout/div/div/ng-component/siconia-lib-body-nav-menu/div/div/div/div/div/button[1]


def create_dc_fw_Compaign(driver,dc_id, target_fw_id):
    time.sleep(2)

    driver.find_element_by_link_text('Campaigns').click()
    time.sleep(2)
    driver.find_element_by_link_text('Create New Campaign').click()
    time.sleep(1)
    # driver.find_element_by_xpath("//*[contains(text(), 'Firmware Update')]").click()

    step1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locator.dc_fw_campaign_page)))
    step1.click()
    select_group = Select(driver.find_element_by_id("targetFirmware"))
    select_group.select_by_value(str(target_fw_id))
    name= 'AUTO_DC_FW_'+str(datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    camp_name_input =driver.find_element_by_id('campaignName')
    camp_name_input.send_keys(name)
    step2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button[contains(text(), 'Next')]")))
    step2.location_once_scrolled_into_view
    step2.click()
    step3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button[contains(text(), 'Next')]")))
    step3.location_once_scrolled_into_view
    step3.click()
    step4 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@class="step-number pointer"]')))
    step4.location_once_scrolled_into_view
    time.sleep(2)

    device= driver.find_element_by_css_selector('.card-text > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > app-search-network-element:nth-child(1) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
    device.send_keys(dc_id)
    button_search = driver.find_elements_by_xpath("//button[contains(text(), 'Search')]")
    driver.execute_script("arguments[0].click();", button_search[1])
    device=driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div")
    device.location_once_scrolled_into_view
    time.sleep(5)
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")
    time.sleep(5)


    for i in range(len(table)):
        check= table[i].find_element_by_xpath(".//input[@type='checkbox']")
        check.click()
    next=driver.find_element_by_xpath("//button[contains(text(), 'Next')]")
    next.location_once_scrolled_into_view
    next.click()
    details=driver.find_element_by_xpath("//button[contains(text(), 'Details')]")
    details.click()

    threepoints= driver.find_element_by_xpath("//i[@id='dropdownConfig']")
    threepoints.click()
    buttonlaunch  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Launch')]" )))
    buttonlaunch.click()
    buttonyes  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Yes')]" )))
    buttonyes.click()
    time.sleep(3)

    return name


def create_dc_config_Compaign(driver,dc_id, target_fw_id):
    time.sleep(2)

    driver.find_element_by_link_text('Campaigns').click()
    time.sleep(2)
    driver.find_element_by_link_text('Create New Campaign').click()
    time.sleep(1)
    # driver.find_element_by_xpath("//*[contains(text(), 'Firmware Update')]").click()

    step1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locator.dc_fw_campaign_page)))
    step1.click()
    select_group = Select(driver.find_element_by_id("targetConfiguration"))
    select_group.select_by_value(str(target_fw_id))
    name= 'AUTO_DC_FW_'+str(datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    camp_name_input =driver.find_element_by_id('campaignName')
    camp_name_input.send_keys(name)
    step2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button[contains(text(), 'Next')]")))
    step2.location_once_scrolled_into_view
    step2.click()
    step3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button[contains(text(), 'Next')]")))
    step3.location_once_scrolled_into_view
    step3.click()
    step4 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@class="step-number pointer"]')))
    step4.location_once_scrolled_into_view
    time.sleep(2)

    device= driver.find_element_by_css_selector('.card-text > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > app-search-network-element:nth-child(1) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
    device.send_keys(dc_id)
    button_search = driver.find_elements_by_xpath("//button[contains(text(), 'Search')]")
    driver.execute_script("arguments[0].click();", button_search[1])
    device=driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div")
    device.location_once_scrolled_into_view
    time.sleep(5)
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")
    time.sleep(5)


    for i in range(len(table)):
        check= table[i].find_element_by_xpath(".//input[@type='checkbox']")
        check.click()
    next=driver.find_element_by_xpath("//button[contains(text(), 'Next')]")
    next.location_once_scrolled_into_view
    next.click()
    details=driver.find_element_by_xpath("//button[contains(text(), 'Details')]")
    details.click()

    threepoints= driver.find_element_by_xpath("//i[@id='dropdownConfig']")
    threepoints.click()
    buttonlaunch  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Launch')]" )))
    buttonlaunch.click()
    buttonyes  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Yes')]" )))
    buttonyes.click()
    time.sleep(3)

    return name
