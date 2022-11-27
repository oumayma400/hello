from datetime import datetime
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import xml.etree.ElementTree as ET
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
from selenium.webdriver.common import action_chains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys


from selenium.common.exceptions import TimeoutException
# @retry(TimeoutError, tries=3)
# @timeout(10)
# from lxml import etree

import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Locators = os.path.dirname(parrent_path.parent.absolute()) + os.path.sep + "Resources/PageObject/Locators";
Locators2 = Locators.replace('\\', '/')
sys.path.append(Locators2)
from selenium.webdriver.common.by import By
from Locators import Locator
Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)
import ReadConfigFile as conf
import Log
import paramiko
from robot.api import logger
from robot.output import librarylogger
def create_cosem_campaign_on_meter (driver,meter_id, device_type, profile_name):



    campaigns= driver.find_element_by_link_text(Locator.link_campaign)
    campaigns.click()
    time.sleep(2)
    driver.find_element_by_link_text('Create Campaign').click()
    driver.find_element_by_xpath(Locator.button_expert_camp).click()
    #button_create_campaign= driver.find_element_by_id("menu-type-0").click()

    campaign_name= driver.find_element_by_id(Locator.cosem_name_input_id)
    cp_name = "COSEM_auto_"+ str(meter_id)+'_'+str(datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    campaign_name.send_keys(cp_name)

    # selectcategory = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.cosem_device_type_name)))
    # selectcategory.click()


    test1=driver.find_element_by_xpath(Locator.cosem_device_type_name)
    test1.click()

    select_device_type = Select(driver.find_element_by_xpath(Locator.cosem_device_type_name))
    # time.sleep(2)
    select_device_type.select_by_value(device_type)
    # time.sleep(2)

    test2=driver.find_element_by_xpath(Locator.cosem_target_profile_name)
    test2.click()

    select_target_profile = Select(driver.find_element_by_xpath(Locator.cosem_target_profile_name))
    # time.sleep(2)
    select_target_profile.select_by_value(profile_name)

    next= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Next')]")))
    next.location_once_scrolled_into_view
    next.click()
    next= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Next')]")))
    next.location_once_scrolled_into_view
    next.click()
    next= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Next')]")))
    next.location_once_scrolled_into_view
    next.click()

    serial = driver.find_elements_by_xpath(Locator.cosem_device_serial_input_id)
    serial[1].send_keys(meter_id)
    search  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,Locator.search_by_meter_id )))

    driver.execute_script("arguments[0].click();", search)
    next= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Next')]")))
    next.location_once_scrolled_into_view
    time.sleep(1)
    table = driver.find_elements_by_xpath ("//*[@class= 'table table-hover zui-table']/tbody/tr")
    for i in range(len(table)):
        print(table[i])
        check= table[i].find_element_by_xpath(".//td[1]/div/input[@type='checkbox']")
        check.click()
    next= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Next')]")))
    next.location_once_scrolled_into_view
    next.click()
    next= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Next')]")))
    next.location_once_scrolled_into_view
    next.click()
    save= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Save')]")))
    save.location_once_scrolled_into_view
    save.click()

    yes= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,Locator.Yes_modal_button)))
    yes.click()
    time.sleep(2)
    threepoints= driver.find_element_by_xpath("//i[@id='dropdownConfig']")
    threepoints.click()
    buttonlaunch  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Launch')]" )))
    buttonlaunch.click()
    yes= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,Locator.Yes_modal_button)))
    yes.click()




    return  200, cp_name

def download_profile_from_cim(PROJECT, local_path ,remote_path):

	host = conf.ReadConfigFile.read(PROJECT,'cim_ip')
	#host = '172.30.13.172'
	username = conf.ReadConfigFile.read(PROJECT, 'cim_ip_user')
	password = conf.ReadConfigFile.read(PROJECT, 'cim_ip_pass')
	port = 22


	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host,port,  username, password)
	# stdin1, stdout1, stderr1 =ssh.exec_command(command1)
	# localpath =local_path+"\\test.xml"
	Log.log("localpath", local_path,'DEBUG')
	remote_path=remote_path
	Log.log("localpath", remote_path,'DEBUG')
	sftp = ssh.open_sftp()

	sftp.get(remote_path, local_path)

	sftp.close()
	ssh.close()
	return 200

def validate_cosem_update_gui(PROJECT, driver, url, meter_id, profile_name):
    cim_profile_dir = conf.ReadConfigFile.read(PROJECT,'cim_profiledir_path')
    project_local_path= conf.ReadConfigFile.read(PROJECT,'project_local_path')
    profile_path=project_local_path+'\\'+profile_name+'.xml'
    cim_profile_path=cim_profile_dir+'/'+profile_name+'.xml'

    dwld_cim= download_profile_from_cim(PROJECT,profile_path, cim_profile_path)
    time.sleep(2)
    tree = ET.parse(profile_path)
    root = tree.getroot()
    namespaces = {'xmlns': 'http://www.sagemcom.com/amm/hes2015/types/profile/v1/'}
    transactions = root.findall('xmlns:transactions', namespaces)
    print(transactions[0])
    # print(root[0])
    # print(root[1])
    # print(root[2])
    reason=""
    validation=False
    # df = pd.DataFrame(columns= tab)
    for transaction in transactions[0]:
        print(transaction)
        tr = transaction.findall('xmlns:dlms', namespaces)
        for i in range(len(tr)):
            print(tr[i].get('operation'))
            if tr[i].get('operation') == 'GETM':
                for j in range(len(tr[i])):
                    print(tr[i][j].get('obis'))
                    print(tr[i][j].get('attribute'))
                    print(url)
                    driver.get(url)
                    obis= driver.find_element_by_xpath("//app-cosem-accordion/div/div[1]/div/div/div/div[1]/div/div/input")
                    obis.send_keys(tr[i][j].get('obis'))
                    driver.find_element_by_xpath(Locator.first_gp_cosem_view_id).click()
                    driver.find_element_by_xpath(Locator.first_cosem_view_id).click()
                    date_xpath="//*[@class= 'table cosem-stripped-table']/tbody/tr["+str(tr[i][j].get('attribute'))+"]/td[5]/span"
                    date = driver.find_element_by_xpath(date_xpath)
                    print(date.text)
                    dateTimeObj = datetime.now()
                    timestampStr = dateTimeObj.strftime("%d %b. %Y")
                    print("timestampStr", timestampStr)
                    print("dateODM", date.text)

                    currentday= timestampStr.split(' ')[0]
                    currentmonth= timestampStr.split(' ')[1].upper()
                    currentyear= timestampStr.split(' ')[2]


                    odmday= date.text.split(' ')[0]
                    if len(odmday)<2:
                        odmday='0'+str(odmday)
                    odmmonth= date.text.split(' ')[1].upper()
                    odmyear= date.text.split(' ')[2]
                    print('currentdate')
                    print(currentday+' '+currentmonth+' '+currentyear)
                    print('odmdate')
                    print(odmday+' '+odmmonth.upper()+' '+odmyear)
                    #validation =  currentday+' '+currentmonth+' '+currentyear == odmday+' '+odmmonth.upper()+' '+odmyear
                    validation =  currentday+' '+currentyear == odmday+' ' +odmyear
                    if validation != True:
                        reason="Current value date not updated"
                        break
                    value_xpath="//*[@class= 'table cosem-stripped-table']/tbody/tr["+str(tr[i][j].get('attribute'))+"]/td[4]/a"
                    value = driver.find_element_by_xpath(value_xpath)
                    print(value.text)
                    if len(value.text) ==0 :
                        reason="Current value null"
                        break

    #
    # for i in range(len(root[2])):
    #     for j in range(len(root[2][i])):
    #         print(root[2][i][j].get('operation'))
    #         print(root[2][i][j][0].get('obis'))
    #         print(root[2][i][j][0].get('attribute'))
    #         if root[2][i][j].get('operation') =='GETM':
    #             print(url)
    #             driver.get(url)
    #             obis= driver.find_element_by_xpath("//app-cosem-accordion/div/div[1]/div/div/div/div[1]/div/div/input")
    #             obis.send_keys(root[2][i][j][0].get('obis'))
    #             driver.find_element_by_xpath(Locator.first_gp_cosem_view_id).click()
    #             driver.find_element_by_xpath(Locator.first_cosem_view_id).click()
    #             date_xpath="//*[@class= 'table cosem-stripped-table']/tbody/tr["+str(root[2][i][j][0].get('attribute'))+"]/td[5]/span"
    #             date = driver.find_element_by_xpath(date_xpath)
    #             print(date.text)
    #             dateTimeObj = datetime.now()
    #             timestampStr = dateTimeObj.strftime("%d %b %Y")
    #             validation = timestampStr==date.text
    #             if validation != True:
    #                 reason="Current value date not updated"
    #                 break
    #             value_xpath="//*[@class= 'table cosem-stripped-table']/tbody/tr["+str(root[2][i][j][0].get('attribute'))+"]/td[4]/a"
    #             value = driver.find_element_by_xpath(value_xpath)
    #             print(value.text)
    if validation==False:
        return 500, reason
    else:
        return 200, "all values are up to date"
