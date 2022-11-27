*** Settings ***
Documentation     NR
Resource    ./AMQ_North_Interface.robot
Resource    ./UAA_Requests.robot
Resource    ./XML_Preparation.robot
Resource    ./XML_Verification.robot
Resource    ./SQL_Validation.robot
Resource    ./Assert.robot

Library           Collections
Library   ../../Libraries/SELENIUM_Libraries/SeleniumLib.py  
Library    ../../Libraries/DB_Libraries/AccessDB.py               
Library    ../../Libraries/SSH_Libraries/RemoveFile.py           
Library    ../../Libraries/Read_Config/ReadConfigFile.py  
Library    ../../Libraries/Read_Config/Getconf.py
   
Library   ../../Libraries/DB_Libraries/ElasticLib.py    
Library    ../../Libraries/SELENIUM_Libraries/FirmwareUpgradeCampaign.py  
Library    ../../Libraries/SELENIUM_Libraries/KeyRenewalCampaign.py     
Library    ../../Resources/PageObject/KeywordDefinationFiles/ExpertCampaignPage.py         
Library    ../../Libraries/SELENIUM_Libraries/Collect.py    
Library    ../../Libraries/XML_Libraries/Collect_Validation.py    
Library    ../../Libraries/Relay_Libraries/RELAY.py 
Library    ../../Libraries/Log_Parser_Libraries/M2M_Parser.py   
Variables    ../../Libraries/Read_Config/ConfigVariables.py   C:\Users\g551651\Desktop\Test_auto_esb_project\system_e2e_automation_tests-SYSTEM_AUTO_ESB\Configurations\ESB_config.ini

Library           Remote    http://127.0.0.1:8270/    WITH NAME    remoteServer


#*** Variables ***

#${PROJECT}    ESB
#${odm_table}    odm_db
#${timeout}    300
#${Link_type}      1

#${state Ready for Reconnection}    ${2}
#${state connected}    ${1}
#${state disconnected}    ${0}


    
*** Keywords ***
login to page
    [Arguments]    ${driver}    ${odm_url}
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass
    #${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    
clean db
    [Arguments]    ${ssf_name}    ${ssf_remote_path}
    ${meters_ids}    Get Meters List Fluvius    ${PROJECT}    ${ssf_name}
    ${tab_meters_id_din}    extract meters id    ${meters_ids}    din
    ${tab_meters_id_ldn}    extract meters id    ${meters_ids}    ldn
    delete SSF meters from m2m db    ${PROJECT}    m2m_db    m2m_schema    ${tab_meters_id_din}
    #delete SSF meters from m2m db    FLUVIUS    m2m_qa_db    m2m_schema    ${tab_meters_id_din}
    delete SSF meters from vsdc db    ${PROJECT}    vsdc_db    vsdc    ${tab_meters_id_ldn}
    #delete SSF meters from vsdc db    FLUVIUS    vsdc_qa_db    vsdc_qa    ${tab_meters_id_ldn}
    delete SSF meters from kms db    ${PROJECT}    kms_db    kms    ${tab_meters_id_din}
    delete SSF from kms db    ${PROJECT}    kms_db    ${ssf_name}
    delete meters and SSF from odm_db    ${PROJECT}    ${odm_table}    ${ssf_name}
    Remove File From Shared Folder    ${PROJECT}    ${ssf_remote_path}    ${ssf_name}
    Sleep    1

clean db without kms
    [Arguments]    ${ssf_name}    ${ssf_remote_path}
    Log    ${PROJECT}
    ${meters_ids}    Get Meters List    ${PROJECT}    ${ssf_name}
    ${tab_meters_id_din}    extract meters id    ${meters_ids}    din
    ${tab_meters_id_ldn}    extract meters id    ${meters_ids}    ldn
    delete SSF meters from m2m db    ${PROJECT}    m2m_db    m2m_schema    ${tab_meters_id_din}
    #delete SSF meters from m2m db    FLUVIUS    m2m_qa_db    m2m_schema    ${tab_meters_id_din}
    delete SSF meters from vsdc db    ${PROJECT}    vsdc_db    vsdc    ${tab_meters_id_ldn}
    #delete SSF meters from vsdc db    FLUVIUS    vsdc_qa_db    vsdc_qa    ${tab_meters_id_ldn}
    delete meters and SSF from odm_db    ${PROJECT}    ${odm_table}    ${ssf_name}
    Remove File From Shared Folder    ${PROJECT}    ${ssf_remote_path}    ${ssf_name}
    Sleep    1
    
verify_ssf_import_ok
    [Arguments]    ${ssf_name}
    ${current_ssf}    Get Ssf Status Fluvius    ${PROJECT}    ${ssf_name}
    #${ssf_idfromODM}    select request    172.30.12.2    odm_db    odm    postgres    postgres    sf_status    asset_shipment_file    ${condition} 
    #${ssf_status}    extract meters id    ${ssf_idfromODM}    sf_status
    #log    ${ssf_status}
    Should Be True    ${current_ssf}    
    
verify_ssf_import_ok_standard
    [Arguments]    ${ssf_name}
    ${current_ssf}    Get Ssf Status    ${PROJECT}    ${ssf_name}
    #${ssf_idfromODM}    select request    172.30.12.2    odm_db    odm    postgres    postgres    sf_status    asset_shipment_file    ${condition} 
    #${ssf_status}    extract meters id    ${ssf_idfromODM}    sf_status
    #log    ${ssf_status}
    Should Be True    ${current_ssf}  


Precondition_DISPLAY_CREDIT_INFORMATION-Off
    [Arguments]    ${meterID}
    ${assetQueue}   Read Conf    ${PROJECT}    assetQueue 
    ${assetQueueResponse}   Read Conf    ${PROJECT}    assetQueueResponse 
    ${xml}    GET_XML_REQUEST    ${PROJECT}    ELEC_DISPLAY_CREDIT_INFORMATION
	${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${meterID}    1    meterAsset
    Log    ${preparedXML} 
    ${preparedXML}    Meter Updateparams By Param Name    ${preparedXML}    DISPLAY_STATE     Off
    ${preparedXML}    Meter Updateparams By Param Name    ${preparedXML}    PREPAYMENT_STATE    Off
    Inject into AMQ on Queue    ${assetQueue}    ${preparedXML}   
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${assetQueueResponse}    ${correlationID}    ${timeout}
    Should Be Equal As Integers    0    ${replaycode} 
    Sleep    2s

    
Prepare_Inject_Consume_DISPLAY_CREDIT_INFORMATION
    [Arguments]    ${meterID}    ${state}
    ${assetQueue}   Read Conf    ${PROJECT}    assetQueue 
    ${assetQueueResponse}   Read Conf    ${PROJECT}    assetQueueResponse 
    ${xml}    GET_XML_REQUEST    ${PROJECT}    ELEC_DISPLAY_CREDIT_INFORMATION
	${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${meterID}    1    meterAsset
    Log    ${preparedXML} 
    ${preparedXML}    Meter Updateparams By Param Name    ${preparedXML}    DISPLAY_STATE     ${state}
    ${preparedXML}    Meter Updateparams By Param Name    ${preparedXML}    PREPAYMENT_STATE    ${state} 
    Inject into AMQ on Queue    ${assetQueue}    ${preparedXML}   
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${assetQueueResponse}    ${correlationID}    ${timeout}
    Should Be Equal As Integers    0    ${replaycode} 
    Sleep    2s
    [Return]    ${correlationID}    ${response_dateTime}


Prepare_Inject_Consume_Message_old1
    [Arguments]    ${project}    ${RequestQueue}    ${ResponseQueue}    ${mrid_tag}    ${meterID}    ${file_name}    ${param}    ${value}    ${timeout}
    ${xml}    GET_XML_REQUEST    ${project}    ${file_name} 
	${preparedXML}    ${correlationID}    DCT without params to inject        ${xml}    ${meterID}    ${mrid_tag}    ${param}    ${value} 
    Log    ${preparedXML} 
    Inject into AMQ on Queue    ${RequestQueue}    ${preparedXML}   
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ResponseQueue}    ${correlationID}    ${timeout}
    [Return]    ${preparedXML}    ${correlationID}    ${XMLreply}    ${replaycode}    ${response_dateTime}       
    Sleep    2s

Prepare_Inject_Consume_Message_old
    [Arguments]    ${project}    ${RequestQueue}    ${ResponseQueue}    ${mrid_tag}    ${meterID}    ${file_name}    ${param}    ${value}    ${timeout}
    ${xml}    GET_XML_REQUEST    ${project}    ${file_name} 
	${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${meterID}    1    ${mrid_tag}
	${preparedXML}    Update Xml Request    ${preparedXML}    ${param}    ${value} 
    Log    ${preparedXML} 

    Inject into AMQ on Queue    ${RequestQueue}    ${preparedXML}   
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ResponseQueue}    ${correlationID}    ${timeout}
    Should Be Equal As Integers    0    ${replaycode} 
    Sleep    2s
    [Return]    ${correlationID}    ${response_dateTime}    ${XMLreply} 
   
Prepare_odr_message_and_inject_it_into_activemq
    [Arguments]    ${project}    ${mrid_tag}    ${meterID}    ${file_name}    ${param}    ${value}    ${timeout}    ${priority}
    ${readsQueue}    Read Conf    ${project}    readsQueue
    ${readsQueueResponse}    Read Conf    ${project}    readsQueueResponse
     ${xml}    GET_XML_REQUEST    ${project}    ${file_name} 
	${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${meterID}    1    ${mrid_tag}
	${preparedXML}    Update Xml Request    ${preparedXML}    ${param}    ${value}
	${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${priority}
	 
    Log    ${preparedXML} 

    Inject into AMQ on Queue    ${readsQueue}    ${preparedXML}   
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${readsQueueResponse}    ${correlationID}    ${timeout}
    Should Be Equal As Integers    0    ${replaycode} 
    Sleep    2s
    [Return]    ${correlationID}    ${response_dateTime}    ${XMLreply} 
     
Prepare_Inject_Consume_Message_replay_ko
    [Arguments]    ${project}    ${RequestQueue}    ${ResponseQueue}    ${mrid_tag}    ${meterID}    ${file_name}    ${param}    ${value}    ${timeout}
     ${xml}    GET_XML_REQUEST    ${project}    ${file_name} 
     #datetime should be equal to 5 if sla 1 used
     #datetime should be equal to 2875 if sla 2 used
	#datetime should be equal to 10075 if sla 3 used
	${preparedXML}    ${correlationID}    Request Update Past Mrid    ${xml}    ${meterID}    ${mrid_tag}   dateTime    10075 
	${preparedXML}    Update Xml Request    ${preparedXML}    ${param}    ${value} 
    Log    ${preparedXML} 

    Inject into AMQ on Queue    ${RequestQueue}    ${preparedXML}   
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ResponseQueue}    ${correlationID}    ${timeout}
    Should Be Equal As Integers    2    ${replaycode} 
    [Return]    ${correlationID}    ${response_dateTime}    ${XMLreply} 
    
Prepare_Inject_Consume_Message_empty_executeStartTime
    [Arguments]    ${project}    ${RequestQueue}    ${ResponseQueue}    ${mrid_tag}    ${meterID}    ${file_name}    ${param}    ${value}    ${timeout}
     ${xml}    GET_XML_REQUEST    ${project}    ${file_name} 
	${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${meterID}    1    ${mrid_tag}
	${preparedXML}    Update Xml Request Empty Param    ${preparedXML}    ${param}
	${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${value}
    Log    ${preparedXML} 

    Inject into AMQ on Queue    ${RequestQueue}    ${preparedXML}   
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ResponseQueue}    ${correlationID}    ${timeout}
    Should Be Equal As Integers    2    ${replaycode} 
    Sleep    2s
    [Return]    ${correlationID}    ${response_dateTime}    ${XMLreply} 
    
Prepare_Inject_Consume_Message_past_executeStartTime
    [Arguments]    ${project}    ${RequestQueue}    ${ResponseQueue}    ${mrid_tag}    ${meterID}    ${file_name}    ${param}    ${value}    ${timeout}
     ${xml}    GET_XML_REQUEST    ${project}    ${file_name} 
	${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${meterID}    1    ${mrid_tag}
	${preparedXML}    Update Xml Request   ${preparedXML}    ${param}    2010-11-17T12:11:01+01:00
	${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${value} 
    Log    ${preparedXML} 

    Inject into AMQ on Queue    ${RequestQueue}    ${preparedXML}   
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ResponseQueue}    ${correlationID}    ${timeout}
    Should Be Equal As Integers    2    ${replaycode} 
    Sleep    2s
    [Return]    ${correlationID}    ${response_dateTime}    ${XMLreply} 
Prepare_Inject_Consume_UAA_Update
    [Arguments]    ${project}    ${file_name}    ${meterID}    ${items}    ${timeout}    ${req_priority}
    ${assetQueue}   Read Conf    ${PROJECT}    assetQueue 
    ${assetQueueResponse}   Read Conf    ${PROJECT}    assetQueueResponse 
    ${preparedXML}    GET_XML_REQUEST    ${project}    ${file_name}
    ${preparedXML}    ${correlationID}    Request Update Mrid    ${preparedXML}    ${meterID}    1    meterAsset
    ${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${req_priority}
    FOR    ${i}    IN RANGE    len(${items[0]}) 
        Log    ${items[0][${i}]}
        ${preparedXML}    Meter Updateparams By Param Name    ${preparedXML}    ${items[0][${i}]}    ${items[1][${i}]}  
    END
    Inject into AMQ on Queue    ${assetQueue}    ${preparedXML} 
    #######         validation of MDMS response #########  
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${assetQueueResponse}    ${correlationID}    ${timeout}
    Log    ${XMLreply}
    Should Be Equal As Integers    0    ${replaycode}  
    Sleep    2s 
    [Return]    ${correlationID}    ${response_dateTime}
Prepare_Inject_Consume_UAA_Update_without_priority
     [Arguments]    ${project}    ${file_name}    ${meterID}    ${items}    ${timeout}    
    ${assetQueue}   Read Conf    ${PROJECT}    assetQueue 
    ${assetQueueResponse}   Read Conf    ${PROJECT}    assetQueueResponse 
    ${preparedXML}    GET_XML_REQUEST    ${project}    ${file_name}
    ${preparedXML}    ${correlationID}    Request Update Mrid    ${preparedXML}    ${meterID}    1    meterAsset
   
    FOR    ${i}    IN RANGE    len(${items[0]}) 
        Log    ${items[0][${i}]}
        ${preparedXML}    Meter Updateparams By Param Name    ${preparedXML}    ${items[0][${i}]}    ${items[1][${i}]}  
    END
    Inject into AMQ on Queue    ${assetQueue}    ${preparedXML} 
    #######         validation of MDMS response #########  
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${assetQueueResponse}    ${correlationID}    ${timeout}
    Log    ${XMLreply}
    Should Be Equal As Integers    0    ${replaycode}  
    Sleep    2s 
    [Return]    ${correlationID}    ${response_dateTime}
    
Prepare_Inject_Consume_UAA_Update_With_Params
    [Arguments]    ${project}    ${file_name}    ${meterID}    ${items}    ${timeout}    ${req_priority}
    ${assetQueue}   Read Conf    ${PROJECT}    assetQueue 
    ${assetQueueResponse}   Read Conf    ${PROJECT}    assetQueueResponse 
    ${preparedXML}    GET_XML_REQUEST    ${project}    ${file_name}
    ${preparedXML}    ${correlationID}    Request Update Mrid    ${preparedXML}    ${meterID}    1    meterAsset
    ${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${req_priority}
    FOR    ${i}    IN RANGE    len(${items[0]}) 
        Log    ${items[0][${i}]}
        ${preparedXML}    Meter Addparams By Param Name    ${project}    ${preparedXML}    ${items[0][${i}]}    ${items[1][${i}]}  
    END
    Inject into AMQ on Queue    ${assetQueue}    ${preparedXML} 
    #######         validation of MDMS response #########  
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${assetQueueResponse}    ${correlationID}    ${timeout}
    Log    ${XMLreply}
    Should Be Equal As Integers    0    ${replaycode}   
    [Return]    ${correlationID}    ${response_dateTime}  
  
Prepare_Inject_Consume_UAA_Update_With_Params_And_Without_Priority
    [Arguments]    ${project}    ${file_name}    ${meterID}    ${itemsbilling}    ${timeout}
    ${assetQueue}   Read Conf    ${PROJECT}    assetQueue 
    ${assetQueueResponse}   Read Conf    ${PROJECT}    assetQueueResponse 
    ${preparedXML}    GET_XML_REQUEST    ${project}    ${file_name}
    ${preparedXML}    ${correlationID}    Request Update Mrid    ${preparedXML}    ${meterID}    1    meterAsset
    FOR    ${i}    IN RANGE    len(${itemsbilling[0]}) 
        Log    ${itemsbilling[0][${i}]}
        ${preparedXML}    Meter Addparams By Param Name    ${project}    ${preparedXML}    ${itemsbilling[0][${i}]}    ${itemsbilling[1][${i}]}  
    END
    Inject into AMQ on Queue    ${assetQueue}    ${preparedXML} 
    #######         validation of MDMS response #########  
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${assetQueueResponse}    ${correlationID}    ${timeout}
    Log    ${XMLreply}
    Should Be Equal As Integers    0    ${replaycode}   
    [Return]    ${correlationID}    ${response_dateTime} 
      
Prepare_Inject_Consume_SET_Periodic_Delivery
    [Arguments]    ${project}    ${req_priority}        ${file_name}    ${meterID}    ${items}    ${timeout}
    ${assetQueue}   Read Conf    ${PROJECT}    assetQueue 
    ${assetQueueResponse}   Read Conf    ${PROJECT}    assetQueueResponse 
    ${preparedXML}    GET_XML_REQUEST    ${project}    ${file_name}
    ${preparedXML}    ${correlationID}    Request Update Mrid    ${preparedXML}    ${meterID}    1    meterAsset
    ${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${req_priority}
    FOR    ${i}    IN RANGE    len(${items[0]}) 
        Log    ${items[0][${i}]}
        ${preparedXML}    Meter Addparams By Param Name    ${project}    ${preparedXML}    ${items[0][${i}]}    ${items[1][${i}]}  
    END
    Inject into AMQ on Queue    ${assetQueue}    ${preparedXML} 
    #######         validation of MDMS response #########  
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${assetQueueResponse}    ${correlationID}    ${timeout}
    Log    ${XMLreply}
    Should Be Equal As Integers    0    ${replaycode}   
    [Return]    ${correlationID}    ${response_dateTime}   
Prepare_Inject_Consume_Message
    [Arguments]    ${project}    ${RequestQueue}    ${meterID}    ${file_name}    ${path}    ${value}    
    ${xml}    GET_XML_REQUEST    ${project}    ${file_name} 
	${preparedXML}    ${correlationID}    DCT without params to inject    ${xml}    ${meterID}    ${path}    ${value} 
    Log    ${preparedXML} 
    Inject into AMQ on Queue    ${RequestQueue}    ${preparedXML}
    Sleep    5
    [Return]    ${correlationID}   

Prepare_Inject_ODR_Message
    [Arguments]    ${WATER_meterID}    ${file}    ${profile}    ${priority}
    ${ReadsQueue}   Read Conf    ${PROJECT}    readsQueue 
    ${xml}    GET_XML_REQUEST    ${PROJECT}    ${file}
    ${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${WATER_meterID}    1    Meter
    ${preparedXML}    Update Xml Request    ${preparedXML}    measurementProfile    ${profile} 
    ${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${priority}
    Log    ${preparedXML} 
    Inject into AMQ on Queue    ${ReadsQueue}    ${preparedXML}   
    Sleep    5
    [Return]    ${correlationID}
  
Prepare_Inject_CDC_Message
    [Arguments]    ${WATER_meterID}    ${file}    ${priority}
    ${controlQueue}   Read Conf    ${PROJECT}    controlQueue 
    ${xml}    GET_XML_REQUEST    ${PROJECT}    ${file}
    ${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${WATER_meterID}    1    meterAsset
    ${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${priority}
    Log    ${preparedXML} 
    Inject into AMQ on Queue    ${controlQueue}    ${preparedXML}   
    Sleep    5
    [Return]    ${correlationID}  
Prepare_Inject_ELEC_DISPLAY_CREDIT_INFORMATION
    [Arguments]    ${meterID}    ${req_priority}    ${value}
    ${assetQueue}   Read Conf    ${PROJECT}    assetQueue
    ${xml}    GET_XML_REQUEST    ${PROJECT}    ELEC_DISPLAY_CREDIT_INFORMATION
    ${preparedXML}    ${correlationID}    Request Update Mrid    ${xml}    ${meterID}    1    meterAsset
    Log    ${preparedXML} 
    ${preparedXML}    Meter Updateparams By Param Name    ${preparedXML}    DISPLAY_STATE     ${value}
    ${preparedXML}    Meter Updateparams By Param Name    ${preparedXML}    PREPAYMENT_STATE    ${value} 
    ${preparedXML}    Update Xml Request    ${preparedXML}    requestPriority    ${req_priority}
    Inject into AMQ on Queue    ${assetQueue}    ${preparedXML}   
    Sleep    8
    [Return]    ${correlationID}
Capa_Validation
    [Arguments]    ${CapalQueue}    ${meterID}    ${timeout}    ${params_buffer}   ${params_values_buffer}    ${params_availability_buffer}
    ${code}    ${message}    consume CAPA from AMQ    ${CapalQueue}    ${meterID}    ${timeout}
    Log    ${message} 
    ${Capacode}    ${validation_capa}    Verify Capa    ${params_buffer}    ${message}    ${params_values_buffer}    ${params_availability_buffer}
    Should Be True    ${validation_capa}  
    

Capa_Not_Sent
    [Arguments]    ${CapalQueue}    ${meterID}    ${timeout}    ${params_buffer}   ${params_values_buffer}    ${params_availability_buffer}
    ${code}    ${message}    consume CAPA from AMQ    ${CapalQueue}    ${meterID}    ${timeout}
    Log    ${message} 
    Should Be Equal As Integers    ${code}     408    
    
xyzzy
    Log    haythem
  
InitializeTestcase_EVENT_DELIVERY_OFF
    @{items}    Create List
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List  
    Append To List    ${DELIVERY_param}    EVENT_DELIVERY    
	Append To List    ${DELIVERY_value}    Off    
	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
	[Return]    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
	

InitializeTestcase_EVENT_DELIVERY_ON
    @{items}    Create List
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List  
    Append To List    ${DELIVERY_param}    EVENT_DELIVERY    
	Append To List    ${DELIVERY_value}    On   
	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
	[Return]    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
	
InitializeTestcase_Lux_SYS-8256_1
    @{items}    Create List
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List
    Append To List    ${DELIVERY_param}    SWITCHPOINT_PROFILE    
	Append To List    ${DELIVERY_value}    TUTBR   
	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
	[Return]    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
	
InitializeTestcase_SWITCHPOINT_PROFILE "${tut_value}"
    @{items}    Create List
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List
    Append To List    ${DELIVERY_param}    SWITCHPOINT_PROFILE    
	Append To List    ${DELIVERY_value}    ${tut_value}    
	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
	[Return]    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
  

InitializeTestcase_LOAD_LIMIT_ACTIVATE
    @{items}    Create List
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List
    Append To List    ${DELIVERY_param}    LOAD_LIMIT_VALUE    LOAD_LIMIT_DURATION        
    Append To List    ${DELIVERY_value}    30    180    
    Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
    [Return]    ${items}    ${DELIVERY_param}    ${DELIVERY_value}  
    
InitializeTestcase_LOAD_LIMIT_DESACTIVATE
    @{items}    Create List
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List
    Append To List    ${DELIVERY_param}    LOAD_LIMIT_VALUE    LOAD_LIMIT_DURATION        
    Append To List    ${DELIVERY_value}    0    180    
    Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
    [Return]    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
    
InitializeTestcase_CAPACITY_LIMIT_VALUE "${fus_val}"
    @{items}    Create List
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List
    Append To List    ${DELIVERY_param}    CAPACITY_LIMIT_VALUE   
    Append To List    ${DELIVERY_value}    ${fus_val}  
    Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}    
    [Return]    ${items}    ${DELIVERY_param}    ${DELIVERY_value}

InitializeTestcase_USER_PORT "${value}"
    @{items}    Create List
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List
    Append To List    ${DELIVERY_param}    USER_PORT   
    Append To List    ${DELIVERY_value}    ${value}  
    Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}    
    [Return]    ${items}    ${DELIVERY_param}    ${DELIVERY_value}

InitializeTestcase_Meter_Technical_Ids "${meter_to_delete}"
    ${m2m_technical_meter_id}    Select    ${PROJECT}    m2m_db    m2m_schema    m2m_db_user    m2m_db_pass    id    m2m_device    device_id = '${meter_to_delete}'
    ${meter_ldn}    Select    ${PROJECT}    ${odm_table}    odm    odm_db_user    odm_db_pass    ldn    metering_meter    mrid = '${meter_to_delete}'
    ${vsdc_technical_meter_id}    Select    ${PROJECT}    vsdc_db    vsdc    vsdc_db_user    vsdc_db_pass    id    vsdc_device    device_id = '${meter_ldn}'
    [Return]    ${m2m_technical_meter_id}    ${vsdc_technical_meter_id}
  
SET_PERIODIC_DELIVERY_WATER_FOR_SLA_GROUP
    [Arguments]    ${sla_groups}    ${WATER_meterID}    ${driver}    ${req_priority}
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue
    FOR    ${i}    IN RANGE   len(${sla_groups})
        @{items}    Create List
        @{DELIVERY_param}    Create List
        @{DELIVERY_value}    Create List    
        Append To List    ${DELIVERY_param}    REGISTER_DELIVERY    INTERVAL_DELIVERY    EVENT_DELIVERY    ALARM_DELIVERY
    	Append To List    ${DELIVERY_value}    Off    Off    Off    Off     
    	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
    	
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    WATER_SET_PERIODIC_DELIVERY    ${WATER_meterID}    ${items}    ${timeout}
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${WATER_meterID}    30
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${WATER_meterID}    10
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${WATER_meterID}    10
        
        #dataset
        ${sla_group}    Set Variable    ${sla_groups}[${i}]
        @{items}    Create List
        @{DELIVERY_param}    Create List
        @{DELIVERY_value}    Create List
        Append To List    ${DELIVERY_param}    REGISTER_DELIVERY    INTERVAL_DELIVERY     
    	Append To List    ${DELIVERY_value}    ${sla_group}    ${sla_group}   
    	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
       
        # start the test
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    WATER_SET_PERIODIC_DELIVERY    ${WATER_meterID}    ${items}    ${timeout}
       
        ############     ODM DB verification  ###########
        ASSERT DELIVERY PARAMS DB UPDATED    ${WATER_meterID}    ${items}
        
        ${DELIVERY_param2}    Set Variable    REGISTERS_DELIVERY    INTERVALLEN_DELIVERY    
        ${DELIVERY_value2}    Set Variable    ${sla_group}    ${sla_group}   
        ${item}    Set Variable    ${DELIVERY_param2}    ${DELIVERY_value2}
        
        ASSERT MBUS DELIVERY GROUPS UPDATED IN M2M AND VSDC DB    ${WATER_meterID}    ${item} 
      
        ############### CAPA validation     ############
        CAPA DELIVERY PARAMS UPDATED TO ACTIVE    ${WATER_meterID}    ${DELIVERY_param2}    120
        
        ########         ODM GUI verification #############
        ASSERT ODM GUI UPDATED    ${driver}    ${WATER_meterID}     ${items}

        # test EVENT DELIVERY
        @{items}    Create List
        @{DELIVERY_param}    Create List
        @{DELIVERY_value}    Create List
        Append To List    ${DELIVERY_param}    EVENT_DELIVERY    
    	Append To List    ${DELIVERY_value}    On      
    	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
       
        # start the test
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    WATER_SET_PERIODIC_DELIVERY    ${WATER_meterID}    ${items}    ${timeout}
       
        ############     ODM DB verification  ###########
        ASSERT DELIVERY PARAMS DB UPDATED    ${WATER_meterID}    ${items}
    
        ############### CAPA validation     ############
        CAPA DELIVERY PARAMS UPDATED TO ACTIVE    ${WATER_meterID}    ['EVENTS_DELIVERY']    120
        
        ########         ODM GUI verification #############
        ASSERT ODM GUI UPDATED    ${driver}    ${WATER_meterID}     ${items}
        
        # test ALARMS DELIVERY
        @{items}    Create List
        @{DELIVERY_param}    Create List
        @{DELIVERY_value}    Create List
        Append To List    ${DELIVERY_param}    ALARM_DELIVERY    
    	Append To List    ${DELIVERY_value}    On      
    	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
       
        # start the test
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    WATER_SET_PERIODIC_DELIVERY    ${WATER_meterID}    ${items}    ${timeout}
       
        ############     ODM DB verification  ###########
        ASSERT DELIVERY PARAMS DB UPDATED    ${WATER_meterID}    ${items}
    
        ############### CAPA validation     ############
        CAPA DELIVERY PARAMS UPDATED TO ACTIVE    ${WATER_meterID}    ['ALARM_DELIVERY']    120
       
        ########         ODM GUI verification #############
        ASSERT ODM GUI UPDATED    ${driver}    ${WATER_meterID}     ${items}
    
        #########  SLA validation  ############ 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}"
     END
 
SET_PERIODIC_DELIVERY_GAZ_FOR_SLA_GROUP
    [Arguments]    ${sla_groups}    ${GAZ_meterID}    ${driver}    ${req_priority}
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue
    FOR    ${i}    IN RANGE   len(${sla_groups})
        @{items}    Create List
        @{DELIVERY_param}    Create List
        @{DELIVERY_value}    Create List
        Append To List    ${DELIVERY_param}    REGISTER_DELIVERY    INTERVAL_DELIVERY    EVENT_DELIVERY    
    	Append To List    ${DELIVERY_value}    Off    Off    Off         
    	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
    	
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    WATER_SET_PERIODIC_DELIVERY    ${GAZ_meterID}    ${items}    ${timeout}
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${GAZ_meterID}    30
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${GAZ_meterID}    30
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${GAZ_meterID}    30
        
        #dataset
        ${sla_group}    Set Variable    ${sla_groups}[${i}]
        @{items}    Create List
        @{DELIVERY_param}    Create List
        @{DELIVERY_value}    Create List
        Append To List    ${DELIVERY_param}    REGISTER_DELIVERY    INTERVAL_DELIVERY     
    	Append To List    ${DELIVERY_value}    ${sla_group}    ${sla_group}   
    	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
       
        # start the test
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    WATER_SET_PERIODIC_DELIVERY    ${GAZ_meterID}    ${items}    ${timeout}
       
        ############     ODM DB verification  ###########
        ASSERT DELIVERY PARAMS DB UPDATED    ${GAZ_meterID}    ${items}
        
        ${DELIVERY_param2}    Set Variable    REGISTERS_DELIVERY    INTERVALLEN_DELIVERY    
        ${DELIVERY_value2}    Set Variable    ${sla_group}    ${sla_group}   
        ${item}    Set Variable    ${DELIVERY_param2}    ${DELIVERY_value2}
        
        ASSERT MBUS DELIVERY GROUPS UPDATED IN M2M AND VSDC DB    ${GAZ_meterID}    ${item} 
      
        ############### CAPA validation     ############
        CAPA DELIVERY PARAMS UPDATED TO ACTIVE    ${GAZ_meterID}    ${DELIVERY_param2}    120
        
        ########         ODM GUI verification #############
        ASSERT ODM GUI UPDATED    ${driver}    ${GAZ_meterID}     ${items}

        # test EVENT DELIVERY
        @{items}    Create List
        @{DELIVERY_param}    Create List
        @{DELIVERY_value}    Create List
        Append To List    ${DELIVERY_param}    EVENT_DELIVERY    
    	Append To List    ${DELIVERY_value}    On      
    	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
       
        # start the test
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    WATER_SET_PERIODIC_DELIVERY    ${GAZ_meterID}    ${items}    ${timeout}
       
        ############     ODM DB verification  ###########
        ASSERT DELIVERY PARAMS DB UPDATED    ${GAZ_meterID}    ${items}
    
        ############### CAPA validation     ############
        CAPA DELIVERY PARAMS UPDATED TO ACTIVE    ${GAZ_meterID}    ['EVENTS_DELIVERY']    120
        
        ########         ODM GUI verification #############
        ASSERT ODM GUI UPDATED    ${driver}    ${GAZ_meterID}     ${items}

    
        #########  SLA validation  ############ 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}"
    END       
SET_PERIODIC_DELIVERY_ELEC_FOR_SLA_GROUP
    [Arguments]    ${sla_groups}    ${meterID}    ${driver}    ${req_priority}
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue
    @{items_all}    Create List
    @{DELIVERY_param_all}    Create List
    @{DELIVERY_value_all}    Create List
    Append To List    ${DELIVERY_param_all}    REGISTER_DELIVERY    INTERVAL_DELIVERY    PQ3_DELIVERY    PQ2_DELIVERY    PQ4_DELIVERY    PQ1_DELIVERY    EVENT_DELIVERY    
	Append To List    ${DELIVERY_value_all}    Off    Off    Off    Off    Off    Off    Off        
	Append To List    ${items_all}    ${DELIVERY_param_all}    ${DELIVERY_value_all}
	
    @{items_event}    Create List
    @{DELIVERY_param_event}    Create List
    @{DELIVERY_value_event}    Create List
    Append To List    ${DELIVERY_param_event}    EVENT_DELIVERY    
	Append To List    ${DELIVERY_value_event}    On      
	Append To List    ${items_event}    ${DELIVERY_param_event}    ${DELIVERY_value_event}
	
    FOR    ${i}    IN RANGE   len(${sla_groups})

        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    ELEC_SET_PERIODIC_DELIVERY    ${meterID}    ${items_all}    ${timeout}
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    30
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    30
        ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    30
        
        #dataset
        ${sla_group}    Set Variable    ${sla_groups}[${i}]
        @{items}    Create List
        @{DELIVERY_param}    Create List
        @{DELIVERY_value}    Create List
        Append To List    ${DELIVERY_param}    REGISTER_DELIVERY    INTERVAL_DELIVERY    PQ3_DELIVERY    PQ2_DELIVERY    PQ4_DELIVERY    PQ1_DELIVERY    
    	Append To List    ${DELIVERY_value}    ${sla_group}    ${sla_group}    ${sla_group}    ${sla_group}    ${sla_group}    ${sla_group}   
    	Append To List    ${items}    ${DELIVERY_param}    ${DELIVERY_value}
       
        # start the test
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    ELEC_SET_PERIODIC_DELIVERY    ${meterID}    ${items}    ${timeout}
       
        ############     ODM DB verification  ###########
        ASSERT DELIVERY PARAMS DB UPDATED    ${meterID}    ${items}

        ${DELIVERY_param2}    Set Variable    REGISTERS_DELIVERY    INTERVALLEN_DELIVERY    PQ3_DELIVERY    PQ2_DELIVERY    PQ4_DELIVERY    PQ1_DELIVERY   
        ${DELIVERY_value2}    Set Variable    ${sla_group}    ${sla_group}    ${sla_group}    ${sla_group}    ${sla_group}    ${sla_group}    
        ${item}    Set Variable    ${DELIVERY_param2}    ${DELIVERY_value2}
       
        ASSERT DELIVERY GROUPS UPDATED IN M2M AND VSDC DB    ${meterID}    ${item}

        ############### CAPA validation     ############
        CAPA DELIVERY PARAMS UPDATED TO ACTIVE    ${meterID}    ${DELIVERY_param2}    120
       
        ########         ODM GUI verification #############
        ASSERT ODM GUI UPDATED    ${driver}    ${meterID}     ${items}

        # test EVENT DELIVERY
        # start the test
        ${correlationID}    ${response_dateTime}    Prepare_Inject_Consume_SET_Periodic_Delivery    ${PROJECT}    ${req_priority}    ELEC_SET_PERIODIC_DELIVERY    ${meterID}    ${items_event}    ${timeout}
       
        ############     ODM DB verification  ###########
        ASSERT DELIVERY PARAMS DB UPDATED    ${meterID}    ${items_event}
    
        ############### CAPA validation     ############
        CAPA DELIVERY PARAMS UPDATED TO ACTIVE    ${meterID}    ['EVENTS_DELIVERY']    120
    
        ########         ODM GUI verification #############
        ASSERT ODM GUI UPDATED    ${driver}    ${meterID}     ${items_event}
 
        #########  SLA validation  ############ 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}"

    END  


    
Open Association
    [Arguments]    ${association_name}=${EMPTY}
    ${client_name}    Run Keyword If    '${association_name}'=='${EMPTY}'    Get Config Param    Config.ini    param_Asso    defaultassociation
    ...    ELSE    set variable          ${association_name}
    
    ${res}    Connect    ${client_name}    ${Link_type}
    should be equal    ${res}    ${0}    Operation failed
  

Read From Meter
   [Arguments]    ${class_id}    ${obis}    ${attribut}
   Open Association
   #${output}    ${output2}    ReadObis    70    000060030AFF    2
   ${output}    ${output2}    ReadObis    ${class_id}    ${obis}    ${attribut}
   Close
   [Return]     ${output}    ${output2}
   
   
    

Check that the Breaker control state is connected
    ${res}    Get Breaker State    Breaker
    should be equal    ${res}[1]    ${state connected}    The Breaker state is not connected

    

Check that Breaker mode is ${mode}
    ${mode}    Convert to integer    ${mode}
    ${res}    Get BreakerMode
    should be equal    ${res}    ${mode}    The Breaker Mode is not as expected