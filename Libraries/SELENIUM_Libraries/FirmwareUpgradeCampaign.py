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


def createCompaign(driver,category, type, firmeware, hardeware,scheduling):
    time.sleep(2)

    driver.find_element_by_link_text('Campaigns').click()
    time.sleep(2)
    driver.find_element_by_link_text('Create Campaign').click()
    time.sleep(1)
    # driver.find_element_by_xpath("//*[contains(text(), 'Firmware Update')]").click()

    step1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locator.firmware_detail_page)))
    step1.click()

    driver.find_element_by_xpath("//select[@name='firmwareCategory']/option[text()=' "+category+" ']").click()
    driver.find_element_by_xpath("//select[@name='firmwareType']/option[text()=' "+type+" ']").click()
    driver.find_element_by_xpath("//app-campaign-general-information/form/div/div/div/div/div/div/div/select[@name='hardwareVersion']/option[text()=' "+hardeware+" ']").click()
    driver.find_element_by_id('compaign-search-btn-search').click()

    # driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div/div/div/div/div/select/option[text()=' 100 Per page ']").click()

    #x="//siconia-lib-data-table-card/div/div/div[1]/div[2]/div/div/select"
    #driver.find_element_by_xpath(x+)
    time.sleep(3)
    target=driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div/div/div/div/table/tbody")
    target.location_once_scrolled_into_view
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")


    for i in range(len(table)):
        table[i].location_once_scrolled_into_view


        FR = table[i].find_elements_by_tag_name("td")[1].text
        HV = table[i].find_elements_by_tag_name("td")[2].text
        if FR==firmeware and HV== hardeware:
            radio= table[i].find_element_by_xpath(".//input[@type='radio']")
            radio.click()

    config = driver.find_element_by_id('fw-campaign-name')
    config.location_once_scrolled_into_view

    now = datetime.now().isoformat()
    name=hardeware+'_'+now
    config.send_keys(name)
    time.sleep(2)

    #if scheduling!= 'Immediate':
    #    t=driver.find_element_by_xpath('//*[@id="with-scheduling-parameters-start"]')
     #   t.click()


    target =driver.find_element_by_xpath('//div/ngx-step-header')
    target.location_once_scrolled_into_view
    target.click()

    return name


def devices(driver,mrid,version):
    elements=driver.find_elements_by_xpath('//*[@class="step-number pointer"]')
    elements[int(3)].click()
    driver.find_element_by_xpath("//ngx-step-body/div/app-campaign-meters/div/div/div/app-search-meter/form/div/div/div/input[@name='mrid']").send_keys(mrid)
    time.sleep(2)
    driver.find_element_by_xpath("//app-campaign-meters/div/div/div/app-search-meter/form/div/div/div/select[@name='hardwareVersion']/option[text()=' "+version+" ']").click()
    driver.find_element_by_id('meter-search-btn-find').click()
    device=driver.find_element_by_xpath("//app-campaign-meters/siconia-lib-data-table-card/div/div")
    device.location_once_scrolled_into_view
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")
    time.sleep(5)


    for i in range(len(table)):
        check= table[i].find_element_by_xpath(".//input[@type='checkbox']")
        check.click()

    return True
def devices_ellevio(driver,mrid):
    elements=driver.find_elements_by_xpath('//*[@class="step-number pointer"]')
    elements[int(1)].click()
    driver.find_element_by_xpath("//ngx-step-body/div/app-campaign-meters/div/div/div/app-search-meter/form/div/div/div/input[@name='mrid']").send_keys(mrid)
    time.sleep(2)

    driver.find_element_by_id('meter-search-btn-find').click()
    device=driver.find_element_by_xpath("//app-campaign-meters/siconia-lib-data-table-card/div/div")
    device.location_once_scrolled_into_view
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")
    time.sleep(5)


    for i in range(len(table)):
        check= table[i].find_element_by_xpath(".//input[@type='checkbox']")
        check.click()

    return True

def summaryWindow(driver):
    elements=driver.find_elements_by_xpath('//*[@class="step-number pointer"]')
    elements[int(5)].click()
    time.sleep(2)
    target =driver.find_element_by_xpath("//*[contains(text(), 'Save')]")
    target.location_once_scrolled_into_view
    target.click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[contains(text(), 'Yes')]").click()

    #driver.refresh()
    time.sleep(2)
    threepoints= driver.find_element_by_xpath("//i[@id='dropdownConfig']")
    threepoints.click()
    buttonlaunch  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Launch')]" )))
    buttonlaunch.click()
    buttonyes  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Yes')]" )))
    buttonyes.click()
    time.sleep(3)
    #driver.refresh()

    return True



def summaryWindowEllevio(driver):
    elements=driver.find_elements_by_xpath('//*[@class="step-number pointer"]')
    elements[int(4)].click()
    time.sleep(2)
    target =driver.find_element_by_xpath("//*[contains(text(), 'Save')]")
    target.location_once_scrolled_into_view
    target.click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[contains(text(), 'Yes')]").click()

    #driver.refresh()
    time.sleep(2)
    threepoints= driver.find_element_by_xpath("//i[@id='dropdownConfig']")
    threepoints.click()
    buttonlaunch  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Launch')]" )))
    buttonlaunch.click()
    buttonyes  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Yes')]" )))
    buttonyes.click()
    time.sleep(3)
    #driver.refresh()

    return True

def create_firmware_upgrade_campaign_on_meter (driver,meter_id, category, fw_type,fw_id,scheduling_mode):
    driver.find_element_by_link_text('Campaigns').click()
    time.sleep(1)
    driver.find_element_by_link_text('Create Campaign').click()

    driver.find_element_by_xpath("//*[contains(text(), 'Firmware Update')]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//select[@name='firmwareCategory']/option[text()=' "+category+" ']").click()
    driver.find_element_by_xpath("//select[@name='firmwareType']/option[text()=' "+fw_type+" ']").click()
    driver.find_element_by_id("compaign-search-btn-search").click()
    time.sleep(2)
    target = driver.find_element_by_name(fw_id)
    target.location_once_scrolled_into_view
    target.click()
    driver.find_element_by_name(fw_id).click()
    return true


def createCompaign_fluvius(driver,category, meter_type,manifacture, file_name, fw_version,scheduling):
    time.sleep(2)

    driver.find_element_by_link_text('Campaigns').click()
    time.sleep(2)
    driver.find_element_by_link_text('Create Campaign').click()
    time.sleep(1)
    # driver.find_element_by_xpath("//*[contains(text(), 'Firmware Update')]").click()

    step1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locator_Fluvius.firmware_detail_page)))
    step1.click()

    driver.find_element_by_xpath("//select[@name='campaign-firmware-category']/option[text()=' "+category+" ']").click()
    driver.find_element_by_xpath("//select[@name='campaign-target-firmware-type']/option[text()=' "+meter_type+" ']").click()
    driver.find_element_by_xpath("//select[@name='campaign-target-firmware-manufacturer']/option[text()=' "+manifacture+" ']").click()
    # driver.find_element_by_xpath("//app-campaign-general-information/form/div/div/div/div/div/div/div/select[@name='hardwareVersion']/option[text()=' "+hardeware+" ']").click()
    driver.find_element_by_id('compaign-search-btn-search').click()

    # driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div/div/div/div/div/select/option[text()=' 100 Per page ']").click()

    #x="//siconia-lib-data-table-card/div/div/div[1]/div[2]/div/div/select"
    #driver.find_element_by_xpath(x+)
    time.sleep(3)
    target=driver.find_element_by_xpath("//app-campaign-general-information/form/div/div[2]/div")
    target.location_once_scrolled_into_view
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")


    for i in range(len(table)):
        table[i].location_once_scrolled_into_view


        fw_f = table[i].find_elements_by_tag_name("td")[1].text
        fw_v = table[i].find_elements_by_tag_name("td")[2].text
        print(fw_f,fw_v)
        if fw_v==fw_version and fw_f== file_name:
            radio= table[i].find_element_by_xpath(".//input[@type='radio']")
            radio.click()

    config = driver.find_element_by_id('campaign-group-name')
    config.location_once_scrolled_into_view

    now = datetime.now().isoformat()
    name=fw_v+'_'+now
    config.send_keys(name)
    time.sleep(2)

    #if scheduling!= 'Immediate':
    #    t=driver.find_element_by_xpath('//*[@id="with-scheduling-parameters-start"]')
     #   t.click()


    # target =driver.find_element_by_xpath('//div/ngx-step-header')
    # target.location_once_scrolled_into_view
    # target.click()

    return name
def devices_fluvius(driver,mrid,version):
    element=driver.find_element_by_id('meters')
    element.location_once_scrolled_into_view
    element.click()


    driver.find_element_by_css_selector('.collapse > app-search-meter:nth-child(1) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)').send_keys(mrid)
    time.sleep(2)
    # driver.find_element_by_xpath("//app-campaign-meters/div/div/div/app-search-meter/form/div/div/div/select[@name='hardwareVersion']/option[text()=' "+version+" ']").click()
    # driver.find_element_by_id('meter-search-btn-search').click()


    step1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'form.ng-dirty > div:nth-child(5) > div:nth-child(1) > button:nth-child(2)')))
    step1.click()
    # button_search = driver.find_element_by_id('meter-search-btn-search').click()
    # driver.execute_script("arguments[0].click();", button_search)
    device=driver.find_element_by_xpath("//app-campaign-meters/siconia-lib-data-table-card/div/div")
    device.location_once_scrolled_into_view
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")
    time.sleep(5)


    for i in range(len(table)):
        check= table[i].find_element_by_xpath(".//input[@type='checkbox']")
        check.click()

    return True

def summaryWindowFluvius(driver):
    element=driver.find_element_by_id('summery')
    element.location_once_scrolled_into_view
    element.click()
    time.sleep(2)
    target =driver.find_element_by_xpath("//*[contains(text(), 'Save')]")
    target.location_once_scrolled_into_view
    target.click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[contains(text(), 'Yes')]").click()

    #driver.refresh()
    time.sleep(2)
    threepoints= driver.find_element_by_xpath("//i[@id='dropdownConfig']")
    threepoints.click()
    buttonlaunch  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Launch')]" )))
    buttonlaunch.click()
    buttonyes  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Yes')]" )))
    buttonyes.click()
    time.sleep(3)
    #driver.refresh()

    return True

def summaryWindowFluviusDraft(driver):
    element=driver.find_element_by_id('summery')
    element.location_once_scrolled_into_view
    element.click()
    time.sleep(2)
    target =driver.find_element_by_xpath("//*[contains(text(), 'Save')]")
    target.location_once_scrolled_into_view
    target.click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[contains(text(), 'Yes')]").click()

    #driver.refresh()
    #time.sleep(2)
    #threepoints= driver.find_element_by_xpath("//i[@id='dropdownConfig']")
    #threepoints.click()
    #buttonlaunch  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Launch')]" )))
   # buttonlaunch.click()
    #buttonyes  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Yes')]" )))
    #buttonyes.click()
    time.sleep(3)
    #driver.refresh()

    return True

def check_campaign_status_odm(driver, param, value, camp_id):
    parameters = driver.find_elements_by_tag_name( "siconia-lib-information-card")

    config_list = parameters[1].find_elements_by_xpath( "./div/div/div[1]/table/tbody/tr")
    print(len(config_list))
    validation = True
    reason =""
    element_found= False

    for i in range(1,len(config_list)+1):
        conf = driver.find_element_by_xpath("//table/tbody/tr["+str(i)+"]/td[1]")
        val = driver.find_element_by_xpath("//table/tbody/tr["+str(i)+"]/td[2]")
        print(conf.text, val.text)
	# for j in range(len(param)):
        if conf.text ==param:
            print("conf.text:",conf.text,"param[j] : ", param)
            element_found=True
            print("val.text == value", val.text == value)
            if val.text != value:
                print("val.text != value", val.text != value)
                validation =False
                reason= "parameter "+conf.text +" has wrong value"
                break


    print("element_found", element_found)
    if element_found ==False:
        validation = False
        reason ="element not found in odm GUI"

    else:
        element_found = False
    return validation, reason

def createCompaignEllevio(driver,category, type, firmeware, hardeware,scheduling):
    time.sleep(2)

    driver.find_element_by_link_text('Campaign').click()
    time.sleep(2)
    driver.find_element_by_link_text('Create Campaign').click()
    time.sleep(1)
    # driver.find_element_by_xpath("//*[contains(text(), 'Firmware Update')]").click()

    step1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locator.firmware_detail_page)))
    step1.click()

    driver.find_element_by_xpath("//select[@name='firmwareCategory']/option[text()=' "+category+" ']").click()
    driver.find_element_by_xpath("//select[@name='firmwareType']/option[text()=' "+type+" ']").click()
    driver.find_element_by_xpath("//app-campaign-general-information/form/div/div/div/div/div/div/div/select[@name='hardwareVersion']/option[text()=' "+hardeware+" ']").click()
    driver.find_element_by_id('compaign-search-btn-search').click()

    # driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div/div/div/div/div/select/option[text()=' 100 Per page ']").click()

    #x="//siconia-lib-data-table-card/div/div/div[1]/div[2]/div/div/select"
    #driver.find_element_by_xpath(x+)
    time.sleep(3)
    target=driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div/div/div/div/table/tbody")
    target.location_once_scrolled_into_view
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")


    for i in range(len(table)):
        table[i].location_once_scrolled_into_view


        FR = table[i].find_elements_by_tag_name("td")[1].text
        HV = table[i].find_elements_by_tag_name("td")[2].text
        if FR==firmeware and HV== hardeware:
            radio= table[i].find_element_by_xpath(".//input[@type='radio']")
            radio.click()

    config = driver.find_element_by_id('fw-campaign-name')
    config.location_once_scrolled_into_view

    now = datetime.now().isoformat()
    name=hardeware+'_'+now
    config.send_keys(name)
    time.sleep(2)

    #if scheduling!= 'Immediate':
    #    t=driver.find_element_by_xpath('//*[@id="with-scheduling-parameters-start"]')
     #   t.click()


    target =driver.find_element_by_xpath('//div/ngx-step-header')
    target.location_once_scrolled_into_view
    target.click()

    return name
