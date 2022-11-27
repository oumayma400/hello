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

Current_Configuration  = {}
Current_Configuration['StreetName']='Street Name'
Current_Configuration['CityName']='City Name'
Current_Configuration['RegioGroup']='REGION Group'
Current_Configuration['ParentInstallationPointID']='Parent Installation Point ID'
Current_Configuration['TransformerFactor']='Street Name'
Current_Configuration['Configuration']='Street Name'
Current_Configuration['HouseID']='House ID'
Current_Configuration['HouseNumberSupplement']='House Number Supplement'
Current_Configuration['PostalCode']='Postal Code'
Current_Configuration['HouseID']='House ID'
Current_Configuration['LOAD_LIMIT_VALUE']='LOAD_LIMIT_VALUE'
Current_Configuration['LOAD_LIMIT_DURATION']='LOAD_LIMIT_DURATION'
Current_Configuration['CONTROL_MODE']='CONTROL_MODE'
Current_Configuration['CONTROL_STATE']='CONTROL_STATE'
Current_Configuration['OUTPUT_STATE']='OUTPUT_STATE'
Current_Configuration['LP_RECORDING']='LP_RECORDING'
Current_Configuration['BILLING_RECORDING']='BILLING_RECORDING'
Current_Configuration['BILLING_RESET']='BILLING_RESET'
Current_Configuration['LP_DISPLAY']='LP_DISPLAY'
#Current_Configuration['COLLECT01T1_DELIVERY']='COLLECT01T1_DELIVERY'
Current_Configuration['COLLECT01T2_DELIVERY']='COLLECT01T2_DELIVERY'
Current_Configuration['COLLECT02T1_DELIVERY']='COLLECT02T1_DELIVERY'
Current_Configuration['COLLECT02T2_DELIVERY']='COLLECT02T2_DELIVERY'
Current_Configuration['COLLECT03T1_DELIVERY']='COLLECT03T1_DELIVERY'
Current_Configuration['LP_DISPLAY']='LP_DISPLAY'





def init_driver():
	driver = webdriver.Firefox()
	driver.maximize_window()


	#driver = webdriver.Edge(executable_path = 'C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/msedgedriver.exe')
	return driver

	# try:
    #         options = webdriver.ChromeOptions()
    #         options.add_argument("start_maximized")
    #         options.binary_location = r"C:\Users\g361355\Desktop\ROBOT_ECLIPSE\chromedriver.exe"
    #         path = "C:_Users/g361355/Desktop/ROBOT_ECLIPSE/chromedriver.exe"
    #         chrome_driver = webdriver.Chrome(executable_path=path)
    #         chrome_driver.implicitly_wait(20)
    #         print("Chrome Driver Loaded")
    #         return chrome_driver
	#
	# except Exception as e:
	# 	print("exception is: " + str(e))



def open_gui(driver, url, user, password):
	#url ="https:/nginx.sirius.urd3.local/gateway/"+ gui + "-fe/"
	driver.get(url)
	username= driver.find_element_by_id("username")
	passwordelem= driver.find_element_by_id("password")
	username.send_keys(user)
	passwordelem.send_keys(password)
	driver.find_element_by_name("submit").click()
	time.sleep(4)
	#driver.get(url)
	return True
def login_gui(driver, url):
	#url ="https://nginx.sirius.urd3.local/gateway/"+ gui + "-fe/"

	driver.get(url)
	driver.title
	return driver.title
def go_to_meter_details(driver, url):
	print(url)
	driver.get(url)
	return True
def go_to_link(driver, url):
	driver.get(url)
	return True
def remove_to_qa(driver):
	dest=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".text-left > .card #dropdownConfig")))
	dest.click()
	step2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.movetoqa_button)))
	step2.click()
	time.sleep(2)
	step3 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.confirm_movetoqa_button)))
	step3.click()
	step3 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.movetoqa_yes_button)))
	step3.click()

	return True

def send_for_repair(driver, meter_id):
	step1=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, Locator.menue_device)))
	step1.click()
	step2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_serial_number)))
	step2.send_keys(meter_id)
	time.sleep(2)
	step3=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_search_button)))
	step3.click()
	time.sleep(2)
	step4=driver.find_elements_by_id(Locator.qa_dropdownConfig)
	#step4=WebDriverWait(driver, 20).until(EC.presence_of_elements_located((By.ID, Locator.qa_dropdownConfig)))
	step4[1].click()
	time.sleep(2)

	step5=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_Send_for_repair_button)))
	step5.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaYes_modal_button)))
	step6.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaConfirm_modal_button)))
	step6.click()


	return True

def approve_batch(driver, batch_id):
	step1=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, Locator.menue_batch)))
	step1.click()
	step2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_batch_id_input)))
	step2.send_keys(batch_id)
	time.sleep(2)
	step3=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_search_button)))
	step3.click()
	time.sleep(2)
	step4=driver.find_elements_by_id(Locator.qa_dropdownConfig)
	#step4=WebDriverWait(driver, 20).until(EC.presence_of_elements_located((By.ID, Locator.qa_dropdownConfig)))
	step4[1].click()
	time.sleep(2)

	step5=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_approve_button)))
	step5.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaYes_modal_button)))
	step6.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaConfirm_modal_button)))
	step6.click()
	step7=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaNo_modal_button)))
	step7.click()

	return True

def reject_batch(driver, batch_id):
	step1=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, Locator.menue_batch)))
	step1.click()
	step2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_batch_id_input)))
	step2.send_keys(batch_id)
	time.sleep(2)
	step3=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_search_button)))
	step3.click()
	time.sleep(2)
	step4=driver.find_elements_by_id(Locator.qa_dropdownConfig)
	#step4=WebDriverWait(driver, 20).until(EC.presence_of_elements_located((By.ID, Locator.qa_dropdownConfig)))
	step4[1].click()
	time.sleep(2)

	step5=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_reject_button)))
	step5.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaYes_modal_button)))
	step6.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaConfirm_modal_button)))
	step6.click()
	# step7=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaNo_modal_button)))
	# step7.click()

	return True

def provisionne_batch(driver, batch_id):
	step1=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, Locator.menue_batch)))
	step1.click()
	step2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_batch_id_input)))
	step2.send_keys(batch_id)
	time.sleep(2)
	step3=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_search_button)))
	step3.click()
	time.sleep(2)
	step4=driver.find_elements_by_id(Locator.qa_dropdownConfig)
	#step4=WebDriverWait(driver, 20).until(EC.presence_of_elements_located((By.ID, Locator.qa_dropdownConfig)))
	step4[1].click()
	time.sleep(2)

	step5=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_provisioning_button)))
	step5.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaYes_modal_button)))
	step6.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_send_provisioning_button)))
	step6.click()
	time.sleep(5)
	step7=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaclose_modal_button)))
	step7.click()

	return True


def scrap_meter(driver, meter_id):
	step1=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, Locator.menue_device)))
	step1.click()
	step2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_serial_number)))
	step2.send_keys(meter_id)
	time.sleep(2)
	step3=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_search_button)))
	step3.click()
	time.sleep(2)
	step4=driver.find_elements_by_id(Locator.qa_dropdownConfig)
	#step4=WebDriverWait(driver, 20).until(EC.presence_of_elements_located((By.ID, Locator.qa_dropdownConfig)))
	step4[1].click()
	time.sleep(2)

	step5=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qa_scrap_button)))
	step5.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaYes_modal_button)))
	step6.click()
	step6=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.qaConfirm_modal_button)))
	step6.click()


	return True


def import_new_ssf(driver, PROJECT, ssf_name):
	path = Path(os.path.abspath(__file__))
	parrent_path = path.parent.absolute()
	# parrent_path = parrent_path.parent.absolute()
	parrent_path = parrent_path.parent.absolute()


	ssf_path = os.path.dirname(parrent_path) + os.path.sep + "Resources"
	# ssf_path = ssf_path.replace('\\', '/')
	print(ssf_path+'\\SSF_Files\\')

	ssf_path= ssf_path +'\\SSF_Files\\'+ PROJECT +'\\'+ ssf_name
	ssf_interface= driver.find_element_by_link_text("Shipment file")
	ssf_interface.click()
	drag_sff= driver.find_element_by_id("file-import")
	drag_sff.send_keys(ssf_path)
	driver.find_element_by_id("import-confirm").click()
	upload= driver.find_element_by_xpath("/html/body/ngb-modal-window/div/div/div[3]/button[2]")
	upload.click()
	return True

def import_new_dc_ssf(driver, PROJECT, ssf_name):
	path = Path(os.path.abspath(__file__))
	parrent_path = path.parent.absolute()
	# parrent_path = parrent_path.parent.absolute()
	parrent_path = parrent_path.parent.absolute()


	ssf_path = os.path.dirname(parrent_path) + os.path.sep + "Resources"
	# ssf_path = ssf_path.replace('\\', '/')
	print(ssf_path+'\\SSF_Files\\')

	ssf_path= ssf_path +'\\SSF_Files\\'+ PROJECT +'\\'+ ssf_name
	ssf_interface= driver.find_element_by_link_text("Shipment File")
	ssf_interface.click()
	drag_sff= driver.find_element_by_id("file-import")
	drag_sff.send_keys(ssf_path)
	driver.find_element_by_id("import-confirm").click()
	upload= driver.find_element_by_xpath("/html/body/ngb-modal-window/div/div/div[3]/button[2]")
	upload.click()
	return True

def Close_Driver(driver):
	driver.close()
	return True

def logout(driver):
	#url ="https://nginx.sirius.urd3.local/gateway/"+ gui + "-fe/"
	siconia_link = driver.find_element_by_link_text('siconia')
	siconia_link.click()
	logoutlink = driver.find_element_by_link_text('Logout')
	logoutlink.click()
	return True

def get_total_meters(driver):
	#url ="https://nginx.sirius.urd3.local/gateway/"+ gui + "-fe/"
	total_devices_string = driver.find_element_by_xpath('/html/body/app-root/app-full-layout/div/div/ng-component/app-dashboard-meter/div/div[1]/div/siconia-lib-full-card/div/div/div/div[1]/div[1]/h3')
	total_devices_string=total_devices_string.text
	total_devices_value=total_devices_string.split(':')[1]
	print("hello*------"  ,total_devices_string.split(':')[1])
#       /html/body/app-root/app-full-layout/div/div/ng-component/app-dashboard-meter/div/div[1]/div/siconia-lib-full-card/div/div/div/div[1]/div[1]/h3
	return int(total_devices_value)


def check_config_paramete_gui_updated(driver, param:list, value:list):
	config_list = driver.find_elements_by_xpath( "//table/tbody/tr")
	print(len(config_list))
	validation = True
	reason =""
	element_found= False
	for j in range(len(param)):
		for i in range(1,len(config_list)+1):
			conf = driver.find_element_by_xpath("//table/tbody/tr["+str(i)+"]/td[1]")
			val = driver.find_element_by_xpath("//table/tbody/tr["+str(i)+"]/td[2]")
			print(conf.text, val.text)
		# for j in range(len(param)):
			if conf.text ==param[j]:
				print("conf.text:",conf.text,"param[j] : ", param[j])
				element_found=True
				print("val.text == value[j]", val.text == value[j])
				if val.text != value[j]:
					print("val.text != value[j]", val.text != value[j])
					validation =False
					reason= "parameter "+conf.text +" has wrong value"
					break
		print("element_found", element_found)
		if element_found ==False:
			validation = False
			reason ="element not found in odm GUI"
			break
		else:
			element_found = False

	return validation, reason


def check_config_paramete_gui_updated_hes1_6(PROJECT, driver, param:list, value:list):

	if PROJECT=='ELLEVIO':
		config_list = driver.find_elements_by_xpath( Locator.ELLEVIO_Current_Configuration)
	else:
		config_list = driver.find_elements_by_xpath( Locator.EVN_Current_Configuration)
	print(len(config_list))
	validation = True
	reason =""
	element_found= False
	for j in range(len(param)):
		for i in range(1,len(config_list)+1):


			if PROJECT=='ELLEVIO':
				conf = driver.find_element_by_xpath(Locator.ELLEVIO_Current_Configuration_list +"/table/tbody/tr["+str(i)+"]/td[1]")
				val = driver.find_element_by_xpath(Locator.ELLEVIO_Current_Configuration_list +"/table/tbody/tr["+str(i)+"]/td[2]")
			else:
				conf = driver.find_element_by_xpath(Locator.EVN_Current_Configuration_list +"/table/tbody/tr["+str(i)+"]/td[1]")
				val = driver.find_element_by_xpath(Locator.EVN_Current_Configuration_list +"/table/tbody/tr["+str(i)+"]/td[2]")
			print(conf.text, val.text)
		# for j in range(len(param)):
			if param[j] in Current_Configuration:
				print("first if")
				if conf.text ==Current_Configuration[param[j]]:
					print("conf.text:",conf.text,"param[j] : ", param[j])
					element_found=True
					print("val.text == value[j]", val.text == value[j])
					if val.text != value[j]:
						print("val.text != value[j]", val.text != value[j])
						validation =False
						reason= "parameter "+conf.text +" has wrong value"
						break
			else:
				print("second if")
				print("conf : ",conf.text, "param[j] : ", param[j])
				if conf.text ==param[j]:
					print("conf.text:",conf.text,"param[j] : ", param[j])
					element_found=True
					print("val.text == value[j]", val.text == value[j])
					if val.text != value[j]:
						print("val.text != value[j]", val.text != value[j])
						validation =False
						reason= "parameter "+conf.text +" has wrong value"
						break

		print("element_found", element_found)
		if element_found ==False:
			validation = False
			reason ="element not found in odm GUI"
			break
		else:
			element_found = False

	return validation, reason

def check_meter_status_gui_updated(driver):
	config_list = driver.find_elements_by_xpath( "//siconia-lib-information-card/div/div/div[2]/table/tbody/tr")
	print(len(config_list))
	out = ""

	for i in range(1,len(config_list)+1):
		conf = driver.find_element_by_xpath("//table/tbody/tr["+str(i)+"]/td[1]")
		val = driver.find_element_by_xpath("//table/tbody/tr["+str(i)+"]/td[2]")
		print(conf.text, val.text)
		if conf.text =='Status':
			out=val.text

	return out

def check_cep_event(driver, meter_id, event_type):
	validation=False
	# step1=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "sc_event_object_mrid")))
	# step1.send_keys(meter_id)
	# step2=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "sc_event_type")))
	# step2.send_keys(event_type)
	# step3=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "sc_event_search")))
	# driver.execute_script("arguments[0].click();", step3)
	retries = 1
	while retries <= 3:
		try:
			step1=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "sc_event_object_mrid")))
			step1.send_keys(meter_id)
			step3=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "sc_event_search")))
			driver.execute_script("arguments[0].click();", step3)
			# fisrt_elem=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#\30  > td:nth-child(1) > span:nth-child(1) > p:nth-child(1)")))
                                            # siconia-lib-data-table-card/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/p
			time.sleep(3)

			fisrt_elem = driver.find_element_by_xpath("//siconia-lib-data-table-card/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]")
			# fisrt_elem = driver.find_element_by_css_selector("#\30  > td:nth-child(1) > span:nth-child(1) > p:nth-child(1)")
			print(fisrt_elem)
			fisrt_elem.location_once_scrolled_into_view
			time.sleep(1)
			# driver.execute_script("arguments[0].dblclick();", fisrt_elem);
			actionChains = ActionChains(driver)
			actionChains.double_click(fisrt_elem).perform()
			time.sleep(3)
			event= driver.find_element_by_xpath("//siconia-lib-information-card/div/div/div[1]/table/tbody/tr[6]/td[2]/p").text
			print(event)

			root = etree.fromstring(str.encode(event))
			tree = etree.ElementTree(root)
			root= tree.getroot()
			print(root)
			for header in root.findall('*'):
				print(header.tag)
				if 'Properties' in header.tag:
					print(header[0][0].text)
					if(header[0][0].text =='EVENT_DELIVERY'):
						print(header[0][1].text)
						if(header[0][1].text =='On'):
							validation=True

			break
		except Exception as e:
			Log.log('TimeoutException' , e, 'DEBUG')
			driver.refresh()
			if retries ==3:
				raise Exception(e)
			retries += 1

	return validation


def validate_shipment_parameters_odm_gui(driver , PROJECT, ssf_name, params, device_type):
	mon_dictionnaire = {}
	general_view = ["Supplier", "Serial_number","Year_of_manufactory","Communication_method", "Hardware_version", "Module_active_firmware_version", "Core_active_firmware_version","Device_type", "Configuration_version" ]
	general_comm_view =["IMSI", "IMEI", "Communication_module_id"]
	#mon_dictionnaire['Serial_number']='Mrid'
	#specific ELLEVIO
	if PROJECT =='ELLEVIO':
		mon_dictionnaire['Serial_number']='Serial Number'
	else:
		mon_dictionnaire['Serial_number']='Mrid'
	mon_dictionnaire['Year_of_manufactory']='Year of manufactory'
	mon_dictionnaire['Communication_method']='Communication method'
	mon_dictionnaire['Hardware_version']='Hardware version'
	mon_dictionnaire['Module_active_firmware_version']='Application firmware version'
	mon_dictionnaire['Core_active_firmware_version']='Metrology firmware version'
	mon_dictionnaire['Device_type']='Model'
	mon_dictionnaire['Supplier']='Supplier'
	mon_dictionnaire['Configuration_version']='Configuration version'
	mon_dictionnaire['IMSI']='IMSI'
	mon_dictionnaire['IMEI']='IMEI'
	mon_dictionnaire['Communication_module_id']='Com module id'
	validation= True
	odm_url = conf.ReadConfigFile.read(PROJECT,'odm_url')
	for i in range(len(params)):
		driver.get(odm_url+ 'meter/meter-details/'+params[i]['Serial_number'])
		time.sleep(10)
		config_list = driver.find_elements_by_xpath( "//siconia-lib-information-card/div/div/div[2]/table/tbody/tr")
		odm_tab= {}
		for j in range(1,len(config_list)+1):
			config=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr["+str(j)+"]/td[1]")))
			val=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//table/tbody/tr["+str(j)+"]/td[2]")))
			odm_tab[config.text]= val.text
			# val = driver.find_element_by_xpath("//table/tbody/tr["+str(j)+"]/td[2]")
			# for k in range(len(params[j])):
			# 	print(config.text, val.text)
			# 	if config.text ==params[j]:
			# 		out=val.text
		print("odm_tab")
		print(odm_tab)
		for attribute, value in params[i].items():
			print(attribute, value) # example usage
			if attribute in general_view:
				print("validation of "+ attribute + " value =" + value +" ==>   "+ odm_tab[mon_dictionnaire[attribute]])
				if odm_tab[mon_dictionnaire[attribute]] != value:
					validation = False
					break


		# validation of mobile communication parameters
		if device_type=='ELEC':
			card_info = driver.find_element_by_id( "meter-mobile-communication")
			comm_list = card_info.find_elements_by_xpath("./siconia-lib-information-card/div/div/div[1]/table/tbody/tr")
			odm_comm_tab= {}
			print("len(comm_list)", len(comm_list))
			for j in range(1,len(comm_list)):
				config=driver.find_element_by_xpath("//siconia-lib-information-card/div/div/div[1]/table/tbody/tr["+str(j)+"]/td[1]")
				val=driver.find_element_by_xpath("//siconia-lib-information-card/div/div/div[1]/table/tbody/tr["+str(j)+"]/td[2]")
				odm_comm_tab[config.text]= val.text
				# val = driver.find_element_by_xpath("//table/tbody/tr["+str(j)+"]/td[2]")
				# for k in range(len(params[j])):
				# 	print(config.text, val.text)
				# 	if config.text ==params[j]:
				# 		out=val.text
			print("odm_comm_tab")
			print(odm_comm_tab)
			for attribute, value in params[i].items():
				print(attribute, value) # example usage
				if attribute in general_comm_view:
					print("validation of "+ attribute + " value =" + value +" ==>   "+ odm_comm_tab[mon_dictionnaire[attribute]])
					if odm_comm_tab[mon_dictionnaire[attribute]] != value:
						validation = False
						break
		if validation == False:
			break

	return validation


def validate_shipment_parameters_oem_gui(driver , PROJECT, ssf_name, params):
	mon_dictionnaire = {}
	general_view = ["Supplier", "Serial_number","Year_of_manufactory", "Hardware_version", "Equipment_identifier", "Customer_Article_Number", "APPLICATIVE_FW","PLC_G3_Mac_Address", "WAN_Mac_Address", "Device_type","Configuration_version" ]

	mon_dictionnaire['Serial_number']='Serial number'
	mon_dictionnaire['Year_of_manufactory']='Year of manufactory'
	mon_dictionnaire['Hardware_version']='Hardware version'
	mon_dictionnaire['Equipment_identifier']='Logical Device Name'
	mon_dictionnaire['Customer_Article_Number']='Material ID'
	mon_dictionnaire['APPLICATIVE_FW']='Application firmware version'
	mon_dictionnaire['PLC_G3_Mac_Address']='PLC MAC address'
	mon_dictionnaire['WAN_Mac_Address']='WAN2 MAC Adress'
	mon_dictionnaire['Device_type']='Model'
	mon_dictionnaire['Configuration_version']='Configuration Version'
	mon_dictionnaire['Supplier']='Supplier'
	validation= True
	oem_url = conf.ReadConfigFile.read(PROJECT,'oem_url')
	for i in range(len(params)):
		driver.get(oem_url+ '#/network-element/network-element-details/'+params[i]['Serial_number'])
		time.sleep(10)

		config_list = driver.find_elements_by_xpath( "//siconia-lib-information-card/div/div/div[2]/table/tbody/tr")
		oem_tab= {}
		for j in range(1,len(config_list)+1):
			config=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr["+str(j)+"]/td[1]")))
			val=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//table/tbody/tr["+str(j)+"]/td[2]")))
			oem_tab[config.text]= val.text
			# val = driver.find_element_by_xpath("//table/tbody/tr["+str(j)+"]/td[2]")
			# for k in range(len(params[j])):
			# 	print(config.text, val.text)
			# 	if config.text ==params[j]:
			# 		out=val.text
		print("oem_tab")
		print(oem_tab)
		for attribute, value in params[i].items():
			print(attribute, value) # example usage
			if attribute in general_view:
				print("validation of "+ attribute + " value =" + value +" ==>   "+ oem_tab[mon_dictionnaire[attribute]])
				if oem_tab[mon_dictionnaire[attribute]] != value:
					validation = False
					break
		if validation == False:
			break

	return validation


def search_cep_event_by_event_id(driver, event_id, meter_id ):
	driver.find_element_by_id("sc_event_id").send_keys(event_id)
	driver.find_element_by_id("sc_event_search").click()
	driver.find_element_by_xpath("//table/tbody/tr/td[1]/span/p")
	test= driver.find_element_by_xpath("//table/tbody/tr/td[8]").text == meter_id
	return test
