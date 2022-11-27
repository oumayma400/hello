import sys
# from datetime import datetime
import random
import time
import paramiko
import pandas as pd
import xml.etree.ElementTree as ET
import datetime
import logging

from robot.api import logger
from robot.output import librarylogger

import xmlschema
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

# sys.path.append('C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Libraries/Read_Config')
import ReadConfigFile as conf
import Log
mon_dictionnaire = {}
mon_dictionnaire['S']='seconds'
mon_dictionnaire['MI']='minutes'
mon_dictionnaire['H']='hours'
mon_dictionnaire['D']='days'
mon_dictionnaire['MO']='months'
mon_dictionnaire['Y']='years'




def create_collecte_meter (driver,list_meters_id, profile, collect_type , Scheduling , target_type, collect_start_date,collect_stop_date ,recovery_mode, periodicity):
    Log.log("list_meters_id", list_meters_id, 'INFO')

    retries = 1
    while retries <= 3:
        try:
            Log.log('open metering section' ,"", 'DEBUG')
            step1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, Locator.link_metering)))
            step1.click()
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1

    retries = 1
    while retries <= 3:
        try:
            Log.log('click on  link_task' ,"", 'DEBUG')
            step2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.link_task)))
            step2.click()
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1
    retries = 1
    while retries <= 3:
        try:
            Log.log('click on  create_task' ,"", 'DEBUG')
            step3 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.create_task)))
            step3.click()
            Log.log('click on  create_from_wizard' ,"", 'DEBUG')
            step4 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.create_from_wizard)))
            step4.click()
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1


    #create from wizard
    # cp_name = "AUTO_"+ str(list_meters_id[0])+'_'+str(datetime.datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    cp_name = "AUTO_"+str(datetime.datetime.now().isoformat())+'_'+str(random.randint(1,100001))
    retries = 1
    while retries <= 3:
        try:
            Log.log('write on  task_name_id' ,"", 'DEBUG')
            collect_name= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.task_name_id)))
            collect_name.send_keys(cp_name)
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1
    retries = 1
    while retries <= 3:
        try:
            Log.log('click on  category_id' ,"", 'DEBUG')
            selectcategory = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.category_id)))
            selectcategory.click()
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            # driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1



    for option in selectcategory.find_elements_by_tag_name('option'):
        Log.log('option.text' , option.text, 'DEBUG')
        if option.text == 'Collect':
            option.click() # select() in earlier versions of webdriver
            break
    time.sleep(1)
    retries = 1
    while retries <= 3:
        try:
            Log.log('click on  collect_type_input' ,"", 'DEBUG')
            collecttype_elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.collect_type_input)))
            collecttype_elem.click()
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            # driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1

    xpath = "//div[@role='option'][normalize-space(.)='"+ collect_type+"']"
    retries = 1
    while retries <= 3:
        try:

            KEY  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,xpath )))
            KEY.click();
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            # driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1

    retries = 1
    while retries <= 3:
        try:
            Log.log('click on  scheduling' ,"", 'DEBUG')
            selectscheduling = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.scheduling_id)))
            selectscheduling.click()
            for option in selectscheduling.find_elements_by_tag_name('option'):
                Log.log('option selectscheduling' , option.text, 'DEBUG')
                if option.text == Scheduling:
                    option.click() # select() in earlier versions of webdriver
                    break
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            # driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1



    retries = 1
    while retries <= 3:
        try:

            selecttarget = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.target_id)))
            selecttarget.click()
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            # driver.refresh()
            if retries ==3:
                raise Exception(e)
            retries += 1

    for option in selecttarget.find_elements_by_tag_name('option'):
        Log.log('option selecttarget' , option.text, 'DEBUG')
        Log.log('target_type ' ,target_type,  'DEBUG')

        if option.text == 'Devices' and target_type=='"DEVICES"':
            option.click() # select() in earlier versions of webdriver
            buttonnext  =WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Next')]" )))
            buttonnext.location_once_scrolled_into_view
            selectdevice_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, Locator.select_device_for_collect_input)))
            selectdevice_elem.clear()
            selectdevice_elem.click()
            for i in range(len(list_meters_id)):



                # selectdevice_elem.send_keys(list_meters_id[i])
                xpath = "//div[@role='option'][normalize-space(.)='"+ list_meters_id[i]+"']"
                retries = 1
                meter_added =False
                Log.log('list_meters_id***********' , list_meters_id[i], 'INFO')
                while retries <= 5 and meter_added ==False:
                    try:
                        Log.log('select_device_for_collect_input++++++++++' , meter_added, 'INFO')
                        selectdevice_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Locator.select_device_for_collect_input)))
                        selectdevice_elem.clear()
                        selectdevice_elem.send_keys(list_meters_id[i])
                        time.sleep(2)
                        Log.log('select_device_for_collect_input++++++++++cleared' , "", 'INFO')
                        KEY  =WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,xpath )))
                        KEY.click();

                        xpath_device= "//div/span[2][contains(text(), '"+list_meters_id[i] + "')]"
                        Log.log('xpath_device++++++++++' , xpath_device, 'INFO')
                        driver.find_element_by_xpath(xpath_device)
                        meter_added=True
                        break
                    except Exception as e:
                        Log.log('TimeoutException' , e, 'DEBUG')
                        # driver.refresh()
                        if retries ==3:
                            raise Exception(e)
                        retries += 1



                time.sleep(2)
            buttonnext.click()
            break
        elif option.text == 'Group of devices' and target_type=='"GROUP"':
            Log.log("select target object as GROUP", "",'INFO')
            retries = 1
            while retries <= 3:
                try:

                    option.click() # select() in earlier versions of webdriver


                    select_group = Select(driver.find_element_by_id(Locator.select_group_list))
                    select_group.select_by_value(list_meters_id[0])
                    buttonnext  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Next')]" )))
                    buttonnext.location_once_scrolled_into_view
                    buttonnext.click()
                    break
                except Exception as e:
                    Log.log('TimeoutException' , e, 'DEBUG')
                    # driver.refresh()
                    if retries ==3:
                        raise Exception(e)
                    retries += 1


        elif option.text == 'Alias (by network and/or device type)' and target_type=='"ALIAS"':
            option.click() # select() in earlier versions of webdriver
            buttonnext  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Next')]" )))
            buttonnext.location_once_scrolled_into_view

            select_network_type = Select(driver.find_element_by_id(Locator.select_network_type_list))
            select_network_type.select_by_value(list_meters_id[0])
            select_device_type = Select(driver.find_element_by_id(Locator.select_device_type_list))
            select_device_type.select_by_value(list_meters_id[1])
            buttonnext.click()
            break




    # Calendar.singel_calendar_start(driver,'2021/09/04 16:20:01')
    # Calendar.singel_calendar_stop(driver,'2022/09/05 17:21:02')

    if(periodicity != "0"):
        Log.log("step 1", '','DEBUG')
        time.sleep(2)
        retries = 1
        while retries <= 3:
            try:
                Select_the_schedulling_type = driver.find_element_by_xpath(Locator.Select_the_schedulling_type_yes_button)
                driver.execute_script("arguments[0].click();", Select_the_schedulling_type)
                break
            except Exception as e:
                Log.log('TimeoutException' , e, 'DEBUG')
                if retries ==3:
                    raise Exception(e)
                retries += 1

        #Select_the_schedulling_type.click()
        Log.log("step 2", '','DEBUG')
        retries = 1
        while retries <= 3:
            try:
                start = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.collect_calendar_id_startdate)))
                start.send_keys(collect_start_date)
                break
            except Exception as e:
                Log.log('TimeoutException' , e, 'DEBUG')
                if retries ==3:
                    raise Exception(e)
                retries += 1

        period_value= str(periodicity[0])+str(periodicity[1])
        period_selection=""
        if(len(periodicity) ==3):
            period_selection=str(periodicity[2])
        else:
            period_selection=str(periodicity[2])+str(periodicity[3])
        retries = 1
        while retries <= 3:
            try:
                next= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Next')]")))
                next.location_once_scrolled_into_view
                clickd_period = driver.find_element_by_id(mon_dictionnaire[period_selection])
                driver.execute_script("arguments[0].click();", clickd_period)
                break
            except Exception as e:
                Log.log('TimeoutException' , e, 'DEBUG')
                if retries ==3:
                    raise Exception(e)
                retries += 1
        retries = 1
        while retries <= 3:
            try:
                xpath_select = "//*[@id ='"  +mon_dictionnaire[period_selection]+"' and " +"@formcontrolname='" +mon_dictionnaire[period_selection]+"']"
                select = Select(driver.find_element_by_xpath(xpath_select))
                select.select_by_value(period_value)
                buttonconfirm  =WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,Locator.task_confirm_period )))
                buttonconfirm.click()
                break
            except Exception as e:
                Log.log('TimeoutException' , e, 'DEBUG')
                if retries ==3:
                    raise Exception(e)
                retries += 1



    else:
        retries = 1
        while retries <= 3:
            try:
                start = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.collect_calendar_id_startdate)))
                start.send_keys(collect_start_date)

                stop = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.collect_calendar_id_stopdate)))
                stop.send_keys(collect_stop_date)
                break
            except Exception as e:
                Log.log('TimeoutException' , e, 'DEBUG')
                if retries ==3:
                    raise Exception(e)
                retries += 1

    retries = 1
    while retries <= 3:
        try:
            buttonnext  =WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Next')]" )))
            buttonnext.click()
            profile_input_elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.profile_name)))
            profile_input_elem.send_keys(profile)
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            if retries ==3:
                raise Exception(e)
            retries += 1

    #click search
    # searchprofile = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, Locator.search_by_profile)))
    # searchprofile.click()
    time.sleep(1)
    Log.log("go to form ", '','DEBUG')
    list_of_profiles= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
    list_of_profiles.location_once_scrolled_into_view
    # list_of_profiles= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "siconia-lib-data-table-card")))
    # list_of_profiles.location_once_scrolled_into_view
    # driver.find_element_by_xpath("/html/body/app-root/app-full-layout/div/div/app-task-create-wizard/div[2]/div/app-hes-stepper/div[2]/ngx-step-body[3]/div/app-profile/form/div/div[1]/div[2]/app-hes-profile-dashboard/div/app-search-profile/div/div[2]/form/div[3]/div/button[2]").click()
    Log.log("find search button", '','DEBUG')
    #searchby_profile  =WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,Locator.search_by_profile)))
    # searchby_profile= driver.find_element_by_xpath(Locator.search_by_profile)
    retries = 1
    while retries <= 3:
        try:
            searchby_profile= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, Locator.search_by_profile)))
            searchby_profile.click()
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            if retries ==3:
                raise Exception(e)
            retries += 1

     # driver.execute_script("arguments[0].click();", searchby_profile)

    next= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Next')]")))
    next.location_once_scrolled_into_view
    time.sleep(1)
    retries = 1
    while retries <= 3:
        try:
            select_profile =WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,Locator.profile_list)))
            driver.execute_script("arguments[0].click();", select_profile)
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            if retries ==3:
                raise Exception(e)
            retries += 1

    Log.log("next to advanced", '','DEBUG')
    next1= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Next')]")))
    next1.click()

    Log.log("next to summary", '','DEBUG')
    retries = 1
    while retries <= 3:
        try:
            next2= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/app-full-layout/div/div/app-task-create-wizard/div[2]/div/app-hes-stepper/div[2]/ngx-step-body[4]/div/app-advanced-options/form/div/div[2]/div/div/div/button[1]")))
            next2.location_once_scrolled_into_view
            driver.find_element_by_id("dlmsParameters").click()
            driver.find_element_by_id(recovery_mode).click()
            driver.execute_script("arguments[0].click();", next2)
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            if retries ==3:
                raise Exception(e)
            retries += 1

    # next.click()
    retries = 1
    while retries <= 3:
        try:
            Log.log('click on finish button' ,'', 'INFO')
            finish_button= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Finish')]")))
            finish_button.location_once_scrolled_into_view
            time.sleep(2)
            finish_button= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Finish')]")))
            # finish_button.click()
            driver.execute_script("arguments[0].click();", finish_button)
            break
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            if retries ==3:
                raise Exception(e)
            retries += 1




    return 200, cp_name
def clear_file_from_cim(PROJECT,cim_file_path):
	try:
		host = conf.ReadConfigFile.read(PROJECT,'cim_ip')
		#host = '172.30.13.172'
		username = conf.ReadConfigFile.read(PROJECT, 'cim_ip_user')
		password = conf.ReadConfigFile.read(PROJECT, 'cim_ip_pass')
		port = 22

		command = "rm -rf "+file_path
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port, username, password)
		# stdin1, stdout1, stderr1 =ssh.exec_command(command1)
		stdin, stdout, stderr = ssh.exec_command(command)
		lines = stdout.readlines()
		Log.log('lines', lines,'DEBUG')
		return 200
	except Exception as e:
		return 500
def local_download_file(PROJECT, local_path ,remote_path):

	host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
	#host = '172.30.13.172'
	username = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_user')
	password = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_pass')
	port = 22


	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host,port,  username, password)
	# stdin1, stdout1, stderr1 =ssh.exec_command(command1)
	# localpath =local_path+"\\test.xml"
	Log.log("localpath", local_path,'DEBUG')
	remote_path=remote_path.split("\n")[0]
	Log.log("localpath", remote_path,'DEBUG')
	sftp = ssh.open_sftp()

	sftp.get(remote_path, local_path)

	sftp.close()
	ssh.close()
	return 200
def loop_in_cim(PROJECT,meter_list, local_path):
    print("start search in cim")
    collect_path = conf.ReadConfigFile.read(PROJECT,'cim_shared_path')
    #host = '172.30.13.172'
    host = conf.ReadConfigFile.read(PROJECT,'cim_ip')
    username = conf.ReadConfigFile.read(PROJECT, 'cim_ip_user')
    password = conf.ReadConfigFile.read(PROJECT, 'cim_ip_pass')
    port = int(22)

    absolut_file_path = collect_path
    validation=False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    retries = 1
    while retries <= 3:
        try:

            ssh.connect(host, port, username, password)
        except Exception as e:
            Log.log('TimeoutException' , e, 'DEBUG')
            ssh.close()
            if retries ==3:
                raise Exception(e)
            retries += 1
    validation=False
    timeout = 300   # [seconds]
    timeout_start = time.time()
    Log.log('connect to cim machine' , 'connected successfuly' , 'DEBUG')
    while True and time.time() < timeout_start + timeout:

        command = "grep -l -r "+meter_list['meter_id'][0] +" "+absolut_file_path

        # stdin1, stdout1, stderr1 =ssh.exec_command(command1)
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        Log.log("result fo grep command in cim","",'DEBUG')
        if(len(lines)>0):
            Log.log('lines[0]' , lines[0] , 'DEBUG')
            sftp = ssh.open_sftp()
            sftp.get(lines[0].split("\n")[0], local_path)

            tree = ET.parse(local_path)
            root = tree.getroot()

            tab = ['meter_id']
            df = pd.DataFrame(columns= tab)
            for i in range(len(root[1])):

                d2= {'meter_id':root[1][i][0][0].text }
                df = df.append(d2, ignore_index=True)
            Log.log("all meters found : ", (meter_list['meter_id'] == df['meter_id'])[0],'INFO')
            # clear_file_from_cim(PROJECT, lines[0].split("\n")[0])


            # command_remove = "rm -rf "+lines[0].split("\n")[0]
            # stdin_remove, stdout_remove, stderr_remove = ssh.exec_command(command_remove)
            # lines_remove = stdout_remove.readlines()
            # Log.log(lines_remove)

            validation = (meter_list['meter_id'] == df['meter_id'])[0]
            break
    sftp.close()
    ssh.close()
    return 200, validation




    # if  meter_list['meter_id'].values == df['meter_id']:
    #     Log.log("TRUE")
    # else:
    #     Log.log("false")
def validate_cim_collect_file(collect_file, xsd_file):
    print(collect_file)
    print(xsd_file)
    xml_file = lxml.etree.parse(collect_file)
    xml_validator = lxml.etree.XMLSchema(file=xsd_file)
    is_valid = xml_validator.validate(xml_file)
    return is_valid
def save_collect_response(PROJECT, msg, profile):
    project_local_path= conf.ReadConfigFile.read(PROJECT, 'project_local_path')
    with open(project_local_path+"\\" +profile+".xml", "wb") as f:
        f.write(str.encode(msg))
    return True
def check_collect_in_m2m_by_taskid(PROJECT,task_id, period, initial_meters_list: list,m2m_collect_path, local_path, xsd_path, estimated_stop_task):
    test= False
    try:
        Log.log("initial_meters_list_input", initial_meters_list, 'INFO')
        # while len(initial_meters_list) >0:
        date_time_obj = datetime.datetime.strptime(estimated_stop_task, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        Log.log('compare date ' ,now > date_time_obj, 'DEBUG')

        tab = ['meter_id', 'status', 'datasize']

        host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
        #host = '172.30.13.172'
        username = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_user')
        password = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_pass')
        port = 22
        absolut_file_path = m2m_collect_path
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)


        while len(initial_meters_list)>0 and (now < date_time_obj):
            Log.log("************************initial_meters_list**********************", initial_meters_list, 'INFO')
            command = "grep -l -r "+task_id +" "+absolut_file_path

            # stdin1, stdout1, stderr1 =ssh.exec_command(command1)
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            Log.log("result fo grep command", '', 'DEBUG')
            Log.log('lines',lines,  'DEBUG')
            Log.log("length : ",len(lines),  'DEBUG')
            for i in range(len(lines)):
                df = pd.DataFrame(columns= tab)
                Log.log("file : ",lines[i].split("\n")[0],  'DEBUG')
                sftp = ssh.open_sftp()
                sftp.get(lines[i].split("\n")[0], local_path)
                Log.log("remote_path", lines[i].split("\n")[0], 'DEBUG')
                sftp.close()
                tree = ET.parse(local_path)
                root = tree.getroot()


                for k in range(len(root)):
                    Log.log('id' , root[k].get('id'), 'DEBUG')
                    Log.log('association' , root[k][0].get('association'), 'DEBUG')
                    Log.log('status' ,root[k][0].get('status'), 'DEBUG')
                    if (root[k][0].get('status')== 'done'):
                        Log.log('datasize' , len(root[k][0][0].text), 'DEBUG')
                        d2= {'meter_id':root[k].get('id') ,'status' : root[k][0].get('status') ,'datasize' :len(root[k][0][0].text)}
                        df = df.append(d2, ignore_index=True)
                    else:
                        d2= {'meter_id':root[k].get('id') ,'status' : root[k][0].get('status') ,'datasize' :0}
                        df = df.append(d2, ignore_index=True)
                #local_download_file(PROJECT, local_path ,lines[i].split("\n")[0])
                ssh.close()
                if len(df)>0:
                    time.sleep(10)
                    Log.log("last if step", "", 'DEBUG')
                    Log.log("df['status']" , df['status'], 'DEBUG')
                    if 'done' in df['status'].values:
                        # loop_in_cim(PROJECT, df[df['status']=='done'])
                        Log.log("we have done result", "", 'DEBUG')
                        data1= df[df['status']=='done']

                        data2= data1[data1['datasize'] != 4]
                        Log.log('data2' , data2 , 'DEBUG')
                        if(len(data2)>0):
                            code, output = loop_in_cim(PROJECT,data2, local_path)
                            Log.log("loop_in_cim output :", output, 'DEBUG')
                            if output ==True:
                                Log.log("all meters are in cim result file", "", 'DEBUG')
                                valid= validate_cim_collect_file(local_path, xsd_path)
                                Log.log("validation result by xsd : " ,valid, 'DEBUG')
                                if valid== True:

                                    Log.log("validation result by xsd OK", "", 'DEBUG')

                                else:
                                    break

                            else:
                                Log.log("there are some missing meters in the cim result file", "", 'DEBUG')
                    initial_meters_list =[x for x in initial_meters_list if x not in df['meter_id'].values]
                    if len(initial_meters_list)==0:
                        test= True
                    Log.log("updated initial_meters_list : ", initial_meters_list, 'DEBUG')

                # command_remove = "rm -rf "+lines[i].split("\n")[0]
                # stdin_remove, stdout_remove, stderr_remove = ssh.exec_command(command_remove)
                # lines_remove = stdout_remove.readlines()
                # Log.log(lines_remove)
                now = datetime.datetime.now()


        return test, initial_meters_list
    except Exception as e:
        return 500, e


# def test_log():
#     logging.basicConfig(level=logging.INFO, file='C:\\Users\_\g361355\\Desktop\\ROBOT_ECLIPSE\\E2E-AUTO-SICONIA\\sample.log')
#     # log = logging.getLogger("my-logger")
#     logging.info("Hello, world")
#     log = logging.getLogger("C:\\Users\\g361355\\Desktop\\ROBOT_ECLIPSE\\E2E-AUTO-SICONIA\\sample.log")
#     log.setLevel(logging.NOTSET)
#     log.addHandler(logging.StreamHandler())
#     log.info("Initialized ExampleLibrary")

def write(msg, level='INFO'):
    # Log.log("hello haythem"," ++++++++++++++", 'DEBUG')
    importer.import_class_or_module_by_path(os.path.abspath("C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/std2.log"))
    logger.debug("imported page object {}".format("C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/std2.log"))

#
# logging.basicConfig(filename="C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/std2.log",
#                             filemode='a',
#                             format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                             datefmt='%H:%M:%S',
#                             level=logging.DEBUG)


def test_log2():
    logger.debug("hello word *********************")

    logger.info('<i>This</i> is a boring example.', html=False)


def validate_collect_dateTime(local_path, dt):

    dt=datetime.datetime.strptime(dt[0:19], "%Y-%m-%dT%H:%M:%S")
    print(dt)
    tree = ET.parse(local_path)
    root = tree.getroot()
    dateTime_result = root[0][3].text
    dateTime_result=datetime.datetime.strptime(dateTime_result[0:19], "%Y-%m-%dT%H:%M:%S")

    print("dateTime_result",dateTime_result )
    print("dt" , dt)

    shift = datetime.timedelta(minutes=5)
    past = dt - shift
    futur = dt + shift
    past=past.isoformat()
    futur=futur.isoformat()
    print("validate_collect_dateTime",dateTime_result.isoformat() > past and dateTime_result.isoformat() < futur )
    if dateTime_result.isoformat() > past and dateTime_result.isoformat() < futur :
        return True
    else:
        return False

def loop_in_cim_fluvius(PROJECT,meter_id, local_path):
    collect_path = conf.ReadConfigFile.read(PROJECT,'cim_shared_path')
    # collect_reads_day = conf.ReadConfigFile.read(PROJECT,'collect_reads_day')
    host = conf.ReadConfigFile.read(PROJECT,'cim_ip')
    #host = '172.30.13.172'
    username = conf.ReadConfigFile.read(PROJECT, 'cim_ip_user')
    password = conf.ReadConfigFile.read(PROJECT, 'cim_ip_pass')
    port = 22
    absolut_file_path = collect_path
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    validation=False
    timeout = 300   # [seconds]
    timeout_start = time.time()
    while True and time.time() < timeout_start + timeout:
        now = datetime.datetime.now()
        collect_reads_day="reads_"+str(now.year) +str(now.month)+str(now.day)+"*"
        print("collect_reads_day : ")
        print(collect_reads_day)
        Log.log("collect_reads_day",collect_reads_day,'DEBUG')
        command = "grep -l -r "+meter_id +" "+absolut_file_path+collect_reads_day

        # stdin1, stdout1, stderr1 =ssh.exec_command(command1)
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        Log.log("result fo grep command in cim","",'DEBUG')
        if(len(lines)>0):
            Log.log('lines[0]' , lines[len(lines)-1] , 'DEBUG')
            sftp = ssh.open_sftp()
            sftp.get(lines[len(lines)-1].split("\n")[0], local_path)


            break
    return 200

def check_collect_in_m2m_cim_Fluvius(PROJECT,task_id, meter_id ,m2m_collect_path, local_path, xsd_path, estimated_stop_task):
    test= 500
    reason=""
    finish_loop=False
    try:
        Log.log(" 1- meter_id", meter_id, 'INFO')
        # while len(initial_meters_list) >0:
        date_time_obj = datetime.datetime.strptime(estimated_stop_task, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        Log.log('compare date ' ,now > date_time_obj, 'DEBUG')

        tab = ['meter_id', 'status', 'datasize']

        host = conf.ReadConfigFile.read(PROJECT,'m2m_ip')
        #host = '172.30.13.172'
        username = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_user')
        password = conf.ReadConfigFile.read(PROJECT, 'm2m_ip_pass')
        port = 22
        # absolut_file_path = m2m_collect_path
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)


        while  (finish_loop == False) and  (now < date_time_obj):
            Log.log("************************initial_meters_list**********************  22-10-2021/ ", meter_id, 'INFO')
            now = datetime.datetime.now()
            absolut_file_path= m2m_collect_path +str(now.day)+"-" +str(now.month)+"-"+str(now.year)+"/*"
            command = "grep -l -r "+task_id +" "+absolut_file_path
            stdin, stdout, stderr = ssh.exec_command(command)
            lines = stdout.readlines()
            Log.log("result fo grep command", '', 'DEBUG')
            Log.log('lines',lines,  'DEBUG')
            Log.log("length : ",len(lines),  'DEBUG')

            for i in range(len(lines)):
                df = pd.DataFrame(columns= tab)
                Log.log("file : ",lines[i].split("\n")[0],  'DEBUG')

                command_meterid = "grep -l -r "+meter_id +" "+lines[i].split("\n")[0]
                stdin2, stdout2, stderr2 = ssh.exec_command(command_meterid)
                line_meter_filter = stdout2.readlines()
                Log.log('line in for',line_meter_filter,  'DEBUG')



                if len(line_meter_filter)>0:
                    finish_loop = True
                    sftp = ssh.open_sftp()
                    print("***----local_path ---------*******", local_path)
                    sftp.get(line_meter_filter[0].split("\n")[0], local_path)
                    Log.log("remote_path", line_meter_filter[0].split("\n")[0], 'DEBUG')
                    sftp.close()
                    # tree = ET.parse(local_path)
                    # root = tree.getroot()
                    time.sleep(2)
                    tree = ET.parse(local_path)
                    root = tree.getroot()
                    xpath= './/*[@id="'+str(meter_id) +'"]'
                    print("xpath" ,xpath)

                    target=root.find(xpath)

                    dlms = target.find(".//*[@obis='1;0;99;14;0;255']")
                    print(dlms.text)
                    if target[0].get("status")== "done" and target[1].get("status")== "done":
                        if len(dlms.text)==4:
                            test =200
                            reason ="empty buffer"
                        elif len(dlms.text)>4:
                            print("go to check in cim")
                            code = loop_in_cim_fluvius(PROJECT,meter_id, local_path)
                            if code == 200:
                                print(code)
                                now = datetime.datetime.now()
                                taskres =root.get("taskExec")
                                validtime =validate_collect_dateTime(local_path, taskres)
                                if validtime == True :
                                    valid= validate_cim_collect_file(local_path, xsd_path)
                                    if valid:
                                        test =200
                                        break
                                    else:
                                        break
                                else:
                                    break
                    else:
                        test =500
                        reason = "task failed"

        ssh.close()
        return test, reason
    except Exception as e:
        return 500, e
