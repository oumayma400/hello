from datetime import datetime
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
from selenium.webdriver.common import action_chains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
# from timeout_decorator import timeout, TimeoutError
from selenium.common.exceptions import TimeoutException
# @retry(TimeoutError, tries=3)
# @timeout(10)
import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Locators = os.path.dirname(parrent_path.parent.absolute()) + os.path.sep + "Resources/PageObject/Locators";
Locators2 = Locators.replace('\\', '/')
sys.path.append(Locators2)
from Locators_Fluvius import Locator_Fluvius
from Locators import Locator
def create_key_renewal_campaign_on_meter (driver,meter_id, key_names, schedul_type):
    campaigns= driver.find_element_by_xpath("/html/body/app-root/app-full-layout/div/aside/div/app-sidebar/nav/ul/li[3]/a/span")
    campaigns.click()
    #button_create_campaign= driver.find_element_by_id("menu-type-0").click()
    element1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "menu-type-0")))
    element1.click();
    driver.find_element_by_xpath("/html/body/app-root/app-full-layout/div/div/ng-component/app-campaign-dashboard/div[1]/div/div[2]/h4/div/div/div/button[2]").click()
    campaign_name= driver.find_element_by_id("keyrenewalcampaign-input-name")
    cp_name = "KR_"+ str(meter_id)+'_'+str(datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    campaign_name.send_keys(cp_name)
    campaign_strategy= driver.find_element_by_id("keyrenewalcampaign-input-campaign-ordering-strategy")
    campaign_strategy.send_keys("Per Key Type first")

    for i in range(len(key_names)):
        print(i, key_names[i])
        deliveryTimeEle = driver.find_element_by_xpath("//ng-select[@formcontrolname ='securityKeys']//input[@role='combobox']")
        # click on the combo list box
        deliveryTimeEle.click()
        # click on the list option ( you can change the option based on the requirement.
        xpath = "//div[@role='option'][normalize-space(.)='"+ key_names[i]+"']"
        KEY  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,xpath )))
        KEY.click();
    if(schedul_type=="Immediate"):
        target = driver.find_element_by_id('campaign-immediate-start')
        target.location_once_scrolled_into_view
        target.click()
    elif (schedul_type=="Scheduled"):
        target = driver.find_element_by_id('campaign-between-start')
        target.location_once_scrolled_into_view
        target.click()
        driver.find_element_by_id("cal2").click()
        # datefield = driver.find_element_by_xpath('/html/body/app-root/app-full-layout/div/div/ng-component/app-create-campaign/div/div/div/siconia-lib-stepper/div[2]/ngx-step-body[1]/div/app-campaign-general-info-shared/form/div[1]/div[3]/div/div/div/div[1]/div[2]/div/siconia-lib-double-calendar-date/div/div[2]/div[2]/div[1]/owl-date-time-inline/owl-date-time-container/div[2]/owl-date-time-calendar/div[2]/owl-date-time-month-view')
        # print(datefield)
        # ActionChains(driver).move_to_element(datefield).click().send_keys('28072021').perform()

    top_page=driver.find_element_by_xpath("/html/body/app-root/app-full-layout/div/div/ng-component/app-create-campaign/div/div/div/siconia-lib-stepper/div[1]")
    driver.execute_script("return arguments[0].scrollIntoView(true);", top_page)
    elements=driver.find_elements_by_xpath('//*[@class="step-number pointer"]')
    elements[3].click()

    meterid = driver.find_element_by_css_selector('app-search-meter.text-left > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
    meterid.send_keys(meter_id)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    clicksearchmeter  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,'meter-search-btn-find' )))
    clicksearchmeter.location_once_scrolled_into_view
    clicksearchmeter.click();

    listdeviceswidget = driver.find_element_by_xpath("/html/body/app-root/app-full-layout/div/div/ng-component/app-create-campaign/div/div/div/siconia-lib-stepper/div[2]/ngx-step-body[4]/div/app-campaign-meters-shared/div[2]/div/siconia-lib-data-table-card/div/div/div[2]")
    listdeviceswidget.location_once_scrolled_into_view
    time.sleep(3)
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")
    print(len(table))
    buttonnext  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Next')]" )))
    buttonnext.location_once_scrolled_into_view
    for i in range(len(table)):
        print(table[i])
        check= table[i].find_element_by_xpath(".//input[@type='checkbox']")
        check.click()
        # check = driver.find_element_by_css_selector("input[type='checkbox']")
        # check.click()

    top_page=driver.find_element_by_xpath("/html/body/app-root/app-full-layout/div/div/ng-component/app-create-campaign/div/div/div/siconia-lib-stepper/div[1]")
    driver.execute_script("return arguments[0].scrollIntoView(true);", top_page)
    elements=driver.find_elements_by_xpath('//*[@class="step-number pointer"]')
    time.sleep(10)
    elements[5].click()
    buttonsave  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Save')]" )))
    buttonsave.location_once_scrolled_into_view
    buttonsave.click()
    buttonyes  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Yes')]" )))
    buttonyes.click()
    # time.sleep(1)
    # driver.refresh()
    # WebDriverWait(driver, 10).until(EC.Title_contains((By.ID, "Key Renewal Campaign Details")))
    time.sleep(3)
    threepoints= driver.find_element_by_xpath("//i[@id='dropdownConfig']")
    threepoints.click()
    buttonlaunch  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Launch')]" )))
    buttonlaunch.click()
    buttonyes  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Yes')]" )))
    buttonyes.click()
    time.sleep(3)
    driver.refresh()


    return  cp_name


def create_key_renewal_campaign_on_meter_fluvius(driver,meter_id,meter_type , key_name, duration):
    # campaignwindow  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,xpath )))
    driver.find_element_by_link_text('Campaigns').click()
    time.sleep(2)
    driver.find_element_by_link_text('Create Campaign').click()
    time.sleep(1)
    step1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locator_Fluvius.keyrenewal_detail_page)))
    step1.click()
    campaign_name= driver.find_element_by_id("keyrenewalcampaign-input-name")
    cp_name = "KR_"+ str(meter_id)+'_'+str(datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    campaign_name.send_keys(cp_name)
    campaign_strategy= driver.find_element_by_id("keyrenewalcampaign-input-campaignDuration")
    campaign_strategy.send_keys(duration)

    device_type_input= driver.find_element_by_id("keyrenewalcampaign-select-deviceType")
    device_type_input.send_keys(meter_type)
    #
    # key_type_input= driver.find_element_by_id("keyrenewalcampaign-select-keyType")
    # key_type_input.send_keys(key_name)

    deliveryTimeEle = driver.find_element_by_xpath("//ng-select[@formcontrolname ='keyTypes']//input[@role='combobox']")
    deliveryTimeEle.click()
    # click on the list option ( you can change the option based on the requirement.
    xpath = "//div[@role='option'][normalize-space(.)='"+ key_name+"']"
    KEY  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,xpath )))
    KEY.click();

    element=driver.find_element_by_id('meters_key')
    element.location_once_scrolled_into_view
    element.click()

    driver.find_element_by_css_selector('.collapse > app-search-meter:nth-child(1) > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(2)').send_keys(meter_id)
    time.sleep(2)

    step1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.collapse > app-search-meter:nth-child(1) > form:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2)')))
    step1.click()

    device=driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div")
    device.location_once_scrolled_into_view
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")
    time.sleep(5)


    for i in range(len(table)):
        check= table[i].find_element_by_xpath(".//input[@type='checkbox']")
        check.click()

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

    return  cp_name
