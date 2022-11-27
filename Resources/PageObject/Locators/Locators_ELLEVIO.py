class Locator(object):
	#meter details page card current Configuration

	ELLEVIO_Current_Configuration = "/html/body/app-root/app-full-layout/div/div/ng-component/app-meter-details/div[2]/div[1]/div[2]/div/div[2]/siconia-lib-information-card/div/div/div[1]/table/tbody/tr"
	EVN_Current_Configuration = "//app-meter-config-card/div/div/siconia-lib-data-table-card/div/div/div[2]/div/div/table/tbody/tr"

	
	ELLEVIO_Current_Configuration_list = "/html/body/app-root/app-full-layout/div/div/ng-component/app-meter-details/div[2]/div[1]/div[2]/div/div[2]/siconia-lib-information-card/div/div/div[1]"
	EVN_Current_Configuration_list = "//app-meter-config-card/div/div/siconia-lib-data-table-card/div/div/div[2]/div/div"
	# Login Page locators
	LoginUsernameInputBox = "id:txtUsername"
	LoginPasswordInputBox = "id:txtPassword"
	LoginButton = "id:btnLogin"

	# Home Page Locators
	WelcomeText = "id:welcome"
	LogoutButton = 'css:[href="/index.php/auth/logout"]'


	#odm
	movetoqa_button= "//*[contains(text(), 'Move Device To QA')]"
	confirm_movetoqa_button= "//*[contains(text(), 'Continue')]"
	movetoqa_yes_button= "//*[contains(text(), 'Yes')]"

	#QA dashboard
	menue_device= "Device"
	menue_batch="Batch"
	qa_serial_number = "//input[@formcontrolname='deviceMrid']"
	qa_search_button = "//button[@type='submit']"
	qa_dropdownConfig="dropdownConfig"
	qa_Send_for_repair_button= "//*[contains(text(), 'Send for repair')]"
	qaYes_modal_button= "//*[contains(text(), 'Yes')]"
	qaConfirm_modal_button= "//*[contains(text(), 'Confirm')]"
	qaNo_modal_button=  "//*[contains(text(), 'No')]"
	qa_batch_id_input = "//input[@formcontrolname='shipmentFileName']"
	qa_approve_button= "//*[contains(text(), 'Approve')]"
	qa_provisioning_button= "//*[contains(text(), 'Provisioning')]"
	qa_send_provisioning_button= "//*[contains(text(), 'Send')]"
	qaclose_modal_button="//*[contains(text(), 'Close')]"
	qa_scrap_button="//*[contains(text(), 'Scrap')]"
	qa_reject_button="//*[contains(text(), 'Reject')]"



	#expert campaign

	CreateCampaign_button="menu-type-0"
	link_campaign = 'Campaigns'
	button_expert_camp = "//*[contains(text(), 'Expert Cosem')]"
	cosem_name_input_id="updateconfigcampaign-input-name"
	cosem_device_type_name="//app-campaign-cosem-general-info/form/div/div[2]/div/div/div/div[1]/div/select"
	cosem_target_profile_name="//app-campaign-cosem-general-info/form/div/div[2]/div/div/div/div[2]/div/select"
	cosem_device_serial_input_id='//*[@id="meter-search-mrid"]'
	search_by_meter_id=  "meter-search-btn-find"
	first_gp_cosem_view_id='//div[@id="static-0-header"]/h5/button/em'
	first_cosem_view_id='//div[@id="static-0"]/div/div'

# /html/body/app-root/app-full-layout/div/div/ng-component/app-campaign-dashboard/div[1]/div/div[2]/h4/div/div/div/button[1]
	#firmware campaign
	firmware_detail_page = "//app-campaign-dashboard/div[1]/div/div[2]/h4/div/div/div/button[1]"

	dc_actionl_page = "//*[contains(text(), 'Add dc Action Campaign')]"
	dc_fw_campaign_page = "//*[contains(text(), 'Upgrade Campaign')]"

	#collecte
	link_metering= 'Metering Configuration'
	link_task=  "//H3[contains(text(), 'Task')]"
	create_task=  "//button[contains(text(), 'Create task')]"
	create_from_wizard= "//ngb-popover-window/div[2]/div/div/div[1]/div[1]/em"
	task_name_id= 'idTaskName'
	category_id='idTaskCategory'
	#collect_type_input ="//ng-select[@formcontrolname ='selectedTaskCollects']//input[@role='combobox']"
	collect_type_input='idTaskCollectType'
	scheduling_id="idTaskCollectScheduling"
	target_id="idTargetType"
	select_device_for_collect_input ="//ng-select[@formcontrolname ='activatedDevices']//input[@role='combobox']"

	collect_calendar_id_startdate = 'idStartDate'
	start ='/html/body/div[2]/div[2]/div/owl-date-time-container/div[2]'
	collect_calendar_start_YM=start +"/owl-date-time-calendar/div[1]/div/button/span"
	collect_calendar_id_stopdate = 'idStopDate'
	stop ='/html/body/div[2]/div[3]/div/owl-date-time-container/div[2]'
	collect_calendar_stop_YM=stop +"/owl-date-time-calendar/div[1]/div"
	profile_name='name'
	search_by_profile=  "//button[contains(@class, 'btn btn-primary') and text()='Search']"
	profile_list="//table/tbody/tr/td[1]/div/input"
	Select_the_schedulling_type_yes_button="//div/input[@formcontrolname='isPeriodic' and @id='yes']"
	Select_the_schedulling_type_no_button="no"
	task_confirm_period=  "//*[contains(text(), 'Confirm')]"
	select_group_list= "idGroup"
	select_network_type_list="idAliasNatwork"
	select_device_type_list="idTargetDeviceType"
	dc_id_input_for_collect="idDevice"
	class_of_add_dc_button ="//perfect-scrollbar/div/div[1]/div/div[2]/div[3]/button"
	# includ_dc="//div/input[@id='noIsExclude']"
	includ_dc="#noIsExclude"

	#task manager

	metering_task_id="taskId"
	search_button=  "//button[contains(text(), 'Search')]"
	task_list_dropdownConfig="dropdownConfig"
	task_cancel_button= "//*[contains(text(), 'Cancel')]"
	Yes_modal_button= "//*[contains(text(), 'Yes')]"

# /html/body/div[2]/div[2]/div/owl-date-time-container/div[2]/owl-date-time-calendar/div[1]/div/button/span

#/html/body/div[2]/div[2]/div/owl-date-time-container/div[2]/owl-date-time-calendar/div[2]/owl-date-time-multi-year-view
#/html/body/div[2]/div[2]/div/owl-date-time-container/div[2]/owl-date-time-calendar/div[2]/owl-date-time-multi-year-view/table/tbody/tr[3]/td[1]/span
