*** Settings ***

Documentation     ASSERT


Resource    ./AMQ_North_Interface.robot
Resource    ./StandardKeywords.robot

Library    ../../Libraries/DB_Libraries/AccessDB.py
Library    ../../Libraries/DB_Libraries/ElasticLib.py         
Library    ../../Libraries/XML_Libraries/XML_Verification_Library.py            
Library    ../../Libraries/Read_Config/Getconf.py      
Library    ../../Libraries/SELENIUM_Libraries/SeleniumLib.py 
Library    ../../Libraries/SELENIUM_Libraries/FirmwareUpgradeCampaign.py    
Library    ../../Libraries/SELENIUM_Libraries/Collect.py    
Library    ../../Libraries/XML_Libraries/Collect_Validation.py    
Library           Collections
Variables    ../../Libraries/Read_Config/ConfigVariables.py   C:\Users\g551651\Desktop\Test_auto_esb_project\system_e2e_automation_tests-SYSTEM_AUTO_ESB\Configurations\ESB_config.ini

*** Variables ***
@{DELIVERY_value}
@{Availability}
#config ELLEVIO
${PROJECT}    ESB
${odm_db_name}    odm_db
${meter_type} 


#config FLUVIUS
#${PROJECT}    FLUVIUS
#${meter_type}    ELEC_   
#${odm_db_name}    odm_db_2
*** Keywords ***
ASSERT CHECK TASK IN VSDC
    ${validation}    Check Task In Vsdc    ${DB_HOST}    ${db}    ${database_name}    ${db_user}    ${db_pass}    ${filter}    ${db_name}    ${correlationID}

ASSERT HES OPERATION DURATION
    ${validation}    HES Operation Duration    ${correlationID}
    
ASSERT HES OPERATION RETRY PAUSE
    ${result}    Operation Retry pause    ${correlationID}        
ASSERT DISPLAY CREDIT INFORMATION ON
    [Arguments]    ${meterID}   
    ${db_result}    DB Param Validation    ${PROJECT}    ${odm_db_name}    ${meterID}    ['DISPLAY_STATE', 'PREPAYMENT_STATE']    ['true','true']
    Should Be True    ${db_result}  

ASSERT DISPLAY CREDIT INFORMATION OFF
    [Arguments]    ${meterID}   
    ${db_result}    DB Param Validation    ${PROJECT}    ${odm_db_name}    ${meterID}    ['DISPLAY_STATE', 'PREPAYMENT_STATE']    ['false','false']
    Should Be True    ${db_result} 
    
CAPA DISPLAY CREDIT INFORMATION ON
    [Arguments]    ${meterID}    ${timeout} 
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue  
    ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    ${timeout}
    Log    ${message} 
    ${Capacode}    ${validation_capa}    Verify Capa    ['DISPLAY_CREDIT_INFORMATION','DISPLAY_PREPAYMENT_STATE']    ${message}    ['Active', 'Active']    ['true', 'true']
    Should Be True    ${validation_capa}  
    
CAPA DISPLAY CREDIT INFORMATION OFF
    [Arguments]    ${meterID}    ${timeout} 
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue  
    ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    ${timeout}
    Log    ${message}  
    ${Capacode}    ${validation_capa}    Verify Capa    ['DISPLAY_CREDIT_INFORMATION','DISPLAY_PREPAYMENT_STATE']    ${message}    ['Inactive', 'Inactive']    ['true', 'true']
    Should Be True    ${validation_capa} 
  
CAPA CDC CONNECTED
    [Arguments]    ${meterID}    ${timeout}
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue  
    ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    ${timeout}
    Log    ${message} 
    ${Capacode}    ${validation_capa}    Verify Capa    ['SET_CDC']    ${message}    ['Connected']    ['true']
    Should Be True    ${validation_capa} 
      
CAPA CDC DISCONNECTED
    [Arguments]    ${meterID}    ${timeout}
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue  
    ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    ${timeout}
    Log    ${message} 
    ${Capacode}    ${validation_capa}    Verify Capa    ['SET_CDC']    ${message}    ['Disconnected']    ['true']
    Should Be True    ${validation_capa} 
    
ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "${status}" AND response_dateTime "${response_dateTime}"    
    ${sla_deman_status}    Verify Sla Demand Updated    ${PROJECT}    ${correlationID}    ${response_dateTime}    ${status}
    Log    ${sla_deman_status}
    Should Be True    ${sla_deman_status} 

ASSERT DISPLAY CREDIT INFORMATION FOR METER "${meterID}" UPDATED IN ODM GUI TO ON
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${odm_url}meter/config-parameter/consult/${meterID} 
    ${validation_odm_params}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ['DISPLAY_STATE','PREPAYMENT_STATE']    ['true', 'true']
    Should Be True    ${validation_odm_params}
    Close Driver    ${driver}
ASSERT DISPLAY CREDIT INFORMATION FOR METER "${meterID}" UPDATED IN ODM GUI TO OFF
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${odm_url}meter/config-parameter/consult/${meterID} 
    ${validation_odm_params}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ['DISPLAY_STATE','PREPAYMENT_STATE']    ['false', 'false']
    Should Be True    ${validation_odm_params}
    Close Driver    ${driver}  
 
ASSERT DELIVERY PARAMS DB UPDATED
    [Arguments]    ${meterID}   ${data}
    ${db_result}    DB Param Validation    ${PROJECT}    ${odm_db_name}    ${meterID}    ${data}[0]    ${data}[1]
    Should Be True    ${db_result}

ASSERT USER PORT DB UPDATED TO true
    [Arguments]    ${meterID}   
    ${db_result}    DB Param Validation    ${PROJECT}    ${odm_db_name}    ${meterID}    ['USER_PORT']    ['true']
    Should Be True    ${db_result}

ASSERT USER PORT DB UPDATED TO false
    [Arguments]    ${meterID}   
    ${db_result}    DB Param Validation    ${PROJECT}    ${odm_db_name}    ${meterID}    ['USER_PORT']    ['false']
    Should Be True    ${db_result}    
ASSERT DB CDC PARAMS UPDATED TO "${cdc_status}" FOR METER "${meterID}"
    ${var} =  Set Variable If
    ...  "${cdc_status}"=="connected"    true
    ...  "${cdc_status}"=="disconnected"    false  
    Log    ${var} 
    ${db_result1}    DB Param Validation    ${PROJECT}    ${odm_db_name}    ${meterID}    ['CDC']    ['${var}']
    ${db_result2}    DB Param Validation    ${PROJECT}    ${odm_db_name}    ${meterID}    ['CDC']    ['${cdc_status}']
    @{items}    Create List
    Append To List    ${items}    ${db_result1}    ${db_result2}
    @{items2}    Create List
    Append To List    ${items2}    ${True}     
    List Should Contain Sub List    ${items}     ${items2}  
CAPA DELIVERY PARAMS UPDATED TO ACTIVE
    [Arguments]    ${meterID}    ${DATA}    ${timeout} 
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue  
    ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    ${timeout}
    Log    ${message} 
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List  
    @{Availability}    Create List 
    FOR    ${i}    IN RANGE   len(${DATA})
       Append To List    ${DELIVERY_value}    Active  
       Append To List    ${Availability}    true
    END
    Log    ${Availability} 
    Log    ${DELIVERY_value}
    ${Capacode}    ${validation_capa}    Verify Capa    ${DATA}    ${message}    ${DELIVERY_value}    ${Availability} 
    Should Be True    ${validation_capa} 
  
CAPA DELIVERY PARAMS UPDATED TO INACTIVE
    [Arguments]    ${meterID}    ${DATA}    ${timeout} 
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue  
    ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    ${timeout}
    Log    ${message}  
    @{DELIVERY_param}    Create List
    @{DELIVERY_value}    Create List  
    @{Availability}    Create List 
    FOR    ${i}    IN RANGE   len(${DATA})
        Append To List    ${DELIVERY_value}    Inactive  
        Append To List    ${Availability}    true
    END
    Log    ${Availability} 
    Log    ${DELIVERY_value}
    ${Capacode}    ${validation_capa}    Verify Capa    ${DATA}    ${message}    ${DELIVERY_value}    ${Availability} 
    Should Be True    ${validation_capa}  
    
CAPA PARAMS UPDATED
    [Arguments]    ${meterID}    ${DELIVERY_PARAMx}    ${DELIVERY_valuex}    ${timeout} 
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue  
    @{Availability}    Create List 
     FOR    ${i}    IN RANGE   len(${DELIVERY_PARAMx})
       Append To List    ${Availability}    true
    END
    ${code}    ${message}    consume CAPA from AMQ    ${CapaQueue}    ${meterID}    ${timeout}
    ${Capacode}    ${validation_capa}    Verify Capa    ${DELIVERY_PARAMx}    ${message}    ${DELIVERY_valuex}    ${Availability} 
    Should Be True    ${validation_capa} 
    
ASSERT ODM DELIVERY "${DELIVERY_param}" FOR METER "${meterID}" UPDATED TO "${DELIVERY_value}" IN ODM GUI
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${Current_Configuration}    Read Conf    ${PROJECT}    Current_Configuration
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${Current_Configuration}/${meterID} 
    ${validation_odm_params}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ${DELIVERY_param}    ${DELIVERY_value}
    Should Be True    ${validation_odm_params}
    Close Driver    ${driver}  
 
ASSERT ODM DELIVERY "${DELIVERY_param}" FOR METER "${meterID}" UPDATED TO "${DELIVERY_value}" IN ODM GUI HES1_6
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${Current_Configuration}    Read Conf    ${PROJECT}    Current_Configuration
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${Current_Configuration}/${meterID} 
    ${validation_odm_params}    ${fail reason}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ${DELIVERY_param}    ${DELIVERY_value}
    Should Be True    ${validation_odm_params}
    Close Driver    ${driver} 
       
ASSERT ODM CDC "${cdc_value}" FOR METER "${meterID}" UPDATED IN ODM GUI
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${odm_url}meter/config-parameter/consult/${meterID} 
    
    ${var} =  Set Variable If
    ...  "${cdc_value}"=="connected"    true
    ...  "${cdc_value}"=="disconnected"    false   
    ${validation_odm_params1}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ['CDC']    ['${var}']
    ${validation_odm_params2}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ['CDC']    ['${cdc_value}']
    Close Driver    ${driver} 
    @{items}    Create List
    Append To List    ${items}    ${validation_odm_params1}    ${validation_odm_params2}
    @{items2}    Create List
    Append To List    ${items2}    ${True}     
    List Should Contain Sub List    ${items}     ${items2}     
    
ASSERT ODM CDC "${cdc_value}" FOR METER "${meterID}" UPDATED IN ODM GUI HES1_6
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${odm_url}meter/meter-details/${meterID} 
    
    ${var} =  Set Variable If
    ...  "${cdc_value}"=="connected"    true
    ...  "${cdc_value}"=="disconnected"    false   
    ${validation_odm_params1}    ${fail reason}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ['CONTROL_STATE']    ['${var}']
    ${validation_odm_params2}    ${fail reason}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ['CONTROL_STATE']    ['${cdc_value}']
    
    @{items}    Create List
    Append To List    ${items}    ${validation_odm_params1}    ${validation_odm_params2}
    @{items2}    Create List
    Append To List    ${items2}    ${True}     
    List Should Contain Sub List    ${items}     ${items2} 
    
    ${var2} =  Set Variable If
    ...  "${cdc_value}"=="connected"    true
    ...  "${cdc_value}"=="disconnected"    false   
    ${validation_odm_params1_2}    ${fail reason_2}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ['OUTPUT_STATE']    ['${var2}']
    ${validation_odm_params2_2}    ${fail reason_2}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ['OUTPUT_STATE']    ['${cdc_value}']
    
    @{items_2}    Create List
    Append To List    ${items_2}    ${validation_odm_params1_2}    ${validation_odm_params2_2}
    @{items2_2}    Create List
    Append To List    ${items2_2}    ${True}     
    List Should Contain Sub List    ${items_2}     ${items2_2} 
    
    Close Driver    ${driver}  
    
ASSERT ODM CDC ready for connection FOR METER "${meterID}" UPDATED IN ODM GUI HES1_6
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${odm_url}meter/meter-details/${meterID} 
    ${cdc_value}    Set Variable    disconnected
    ${var} =  Set Variable If
    ...  "${cdc_value}"=="connected"    true
    ...  "${cdc_value}"=="disconnected"    false   
    ${validation_odm_params1}    ${fail reason}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ['OUTPUT_STATE']    ['${var}']
    ${validation_odm_params2}    ${fail reason}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ['OUTPUT_STATE']    ['${cdc_value}']
    
    @{items}    Create List
    Append To List    ${items}    ${validation_odm_params1}    ${validation_odm_params2}
    @{items2}    Create List
    Append To List    ${items2}    ${True}     
    List Should Contain Sub List    ${items}     ${items2} 
    
    ${var2} =  Set Variable If
    ...  "${cdc_value}"=="connected"    true
    ...  "${cdc_value}"=="disconnected"    false   
    ${validation_odm_params1_2}    ${fail reason_2}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ['CONTROL_STATE']    ['ready for connection']
    ${validation_odm_params2_2}    ${fail reason_2}    Check Config Paramete Gui Updated Hes1 6    ${PROJECT}    ${driver}    ['CONTROL_STATE']    ['ready for connection']
    
    @{items_2}    Create List
    Append To List    ${items_2}    ${validation_odm_params1_2}    ${validation_odm_params2_2}
    @{items2_2}    Create List
    Append To List    ${items2_2}    ${True}     
    List Should Contain Sub List    ${items_2}     ${items2_2} 
    
    Close Driver    ${driver} 
    
ASSERT METER LIFECYCLE FOR METER "${meterID}" UPDATED TO "${STATUS}" IN ODM GUI
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${odm_url}meter/meter-details/${meterID} 
    Log    ${odm_url}/meter/meter-details/${meterID}
    ${odm_status}    Check Meter Status Gui Updated    ${driver} 
    Should Be Equal As Strings    ${odm_status}    ${STATUS}    
    Close Driver    ${driver} 
    

ASSERT CEP DELIVERY EVENT RECEIVED FOR METER "${meterID}"
    ${cep_url}   Read Conf    ${PROJECT}    cep_url 
    ${cep_events_url}    Read Conf    ${PROJECT}    cep_events_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${driver}    Init Driver
    Open Gui    ${driver}    ${cep_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${cep_events_url}
    ${cep_notified}    Check Cep Event    ${driver}     ${meterID}    EVT_ODM.meterUpdatedSetPeriodicDelivery
    Should Be True    ${cep_notified}    
    Close Driver    ${driver}
    
ASSERT DELIVERY GROUPS UPDATED IN M2M AND VSDC DB
    [Arguments]    ${meterID}    ${items_elec}
    ${m2m_db_verif}    Verify Delivery Param In M2mFLUVIES    ${PROJECT}    ${meterID}    ${items_elec}    ${meter_type}
    Should Be True    ${m2m_db_verif} 
    ${vsdc_db_verif}    Verify Delivery Param In VsdcFLUVIES    ${PROJECT}    ${meterID}    ${items_elec}    ${meter_type}
    Should Be True    ${vsdc_db_verif} 
    
ASSERT DELIVERY GROUPS UPDATED IN ODM M2M AND VSDC P2P DB
    [Arguments]    ${meterID}    ${item}
    ${odm_db_verif}    Verify Delivery Param In Odm    ${PROJECT}    odm_db    ${meterID}    ${item}
    Should Be True    ${odm_db_verif}    
    ${m2m_db_verif}    Verify Delivery Param In M2m    ${PROJECT}    ${meterID}    ${item}
    Should Be True    ${m2m_db_verif} 
    ${vsdc_p2p_db_verif}    Verify Delivery Param In VSDC P2P    ${PROJECT}    ${meterID}    ${item}
    Should Be True    ${vsdc_p2p_db_verif} 
    
ASSERT DELIVERY GROUPS UPDATED IN ODM M2M AND VSDC PLC DB
    [Arguments]    ${meterID}    ${item}
    ${odm_db_verif}    Verify Delivery Param In Odm    ${PROJECT}    odm_db    ${meterID}    ${item}
    Should Be True    ${odm_db_verif}    
    ${m2m_db_verif}    Verify Delivery Param In M2m    ${PROJECT}    ${meterID}    ${item}
    Should Be True    ${m2m_db_verif} 
    ${vsdc_p2p_db_verif}    Verify Delivery Param In VSDC PLC    ${PROJECT}    ${meterID}    ${item}
    Should Be True    ${vsdc_p2p_db_verif} 

ASSERT MBUS DELIVERY GROUPS UPDATED IN M2M AND VSDC DB
    [Arguments]    ${GAZ_meterID}    ${item}
    ${mbus_code}    ${amr_router}    ${mbus_chanel}    ${energy_type}    Get Mbus Channel    ${PROJECT}    ${GAZ_meterID}
    ${m2m_db_verif}    Verify Delivery Param In M2mFLUVIES    ${PROJECT}    ${amr_router}    ${item}    ${energy_type}_CH${mbus_chanel}
    Should Be True    ${m2m_db_verif} 
     
    ${vsdc_db_verif}    Verify Delivery Param In VsdcFLUVIES    ${PROJECT}    ${amr_router}    ${item}    ${energy_type}_CH${mbus_chanel}
    Should Be True    ${vsdc_db_verif} 
    
ASSERT METER "${meterID}" LIFECYCLE STATUS IN ELK "${status}"
    Sleep    10s
    ${result}    Verify Param Update In Elastic   ${PROJECT}    sla_meter    meter_id    ${meterID}    lifecycle_status    ${status}
    Should Be True    ${result} 
   
ASSERT METER "${meterID}" UAA PARAMS "${params}" UPDATED IN ELK
    FOR    ${i}    IN RANGE    len(${params[0]}) 
        ${result}    Verify Param Update In Elastic    ${PROJECT}    sla_meter    meter_id    ${meterID}    ${params[0][${i}]}    ${params[1][${i}]}
        Should Be True    ${result}    
 
    END
ASSERT ACTIVATION DATES UPDATED FOR METER "${WATER_meterID}"
    ${activation_dates}    Sla Dates Updated    ${PROJECT}    ${WATER_meterID}   
    Should Be True    ${activation_dates} 
ASSERT METER "${meterID}" LIFECYCLE STATUS IN ODM "${status}"
    ${str1} =   Catenate    SEPARATOR=    '    ${meterID}    '
    ${db_status}    Select    ${PROJECT}    ${odm_db_name}    odm    odm_db_user    odm_db_pass    status    metering_meter    mrid = ${str1}
    Should Be Equal As Strings    ${db_status}    ${status} 
    
ASSERT RLC CREATED
    [Arguments]    ${meterID}
    Sleep    10s
    ${code_rlc}    Check Rlc    ${PROJECT}    ${meterID}    ${odm_db_name}     
    Should Be True    ${code_rlc}  
    
ASSERT ACTIVATION TASK STARTED ON METER "${meterID}"
    Sleep    60s
    ${code_activation}    Check Activation    ${PROJECT}    ${meterID}    ${odm_db_name}     
    Should Be True    ${code_activation} 
    
ASSERT CAPACITY_LIMIT PARAM DB UPDATED FOR METER "${meterID}" WITH CATEGORY "${meter_category}" UPDATED AND VALUE "${DELIVERY_value2}"
    ${db_result}    DB Param Validation    ${PROJECT}    ${odm_db_name}    ${meterID}    ['CAPACITY_LIMIT_VALUE_${meter_category}']    ${DELIVERY_value2}
    Should Be True    ${db_result}  
    
ASSERT CIM VALIDATION FOR REPLY "${XMLreply}" USING PROFILE "${profile}"
    ${collect_file}    Read Conf    ${PROJECT}    project_local_path
    Save Collect Response    ${PROJECT}    ${XMLreply}    ${profile}
    Sleep    2s
    ${cim_validation}    Validate Cim Collect File    ${collect_file}\\${profile}.xml    ${collect_file}\\${profile}.xsd
    Should Be True    ${cim_validation}  
    Sleep    2s  
ASSERT CIM ODR VALIDATION FOR REPLY "${XMLreply}" USING PROFILE "${profile}"
    ${collect_file}    Read Conf    ${PROJECT}    project_local_path
    Save Collect Response    ${PROJECT}    ${XMLreply}    ${profile}
    Sleep    4s
    ${cim_validation}    Validate Cim Collect File    ${collect_file}\\${profile}.xml    ${collect_file}\\ODR.xsd
    Should Be True    ${cim_validation}  
    Sleep    2s 
    
ASSERT FLAG VALID OF "${XMLreply}"
    ${flag}    Validate Flag    ${XMLreply}
    Should Be Equal As Strings    ${flag}     0   
    
ASSERT SLA SUSPEND PARAMS UPDATED ON METER "${WATER_meterID}"
    ${sla_capa}    Sla Suspend Params Updated    ${PROJECT}    ${WATER_meterID}
    Should Be True    ${sla_capa}
    
ASSERT NO TASKS FOUND IN M2M AND VSDC FOR DEVICE WITH IDS "${m2m_technical_meter_id}" AND " ${vsdc_technical_meter_id}"
    ${m2m_code}    ${m2m_reason}    Check Exixting Tasks In M2m    ${PROJECT}    ${m2m_technical_meter_id}
    Should Be Equal As Integers    200    ${m2m_code}    
    ${vsdc_code}    ${vsdc_reason}    Check Exixting Tasks In Vsdc   ${PROJECT}    ${vsdc_technical_meter_id} 
    Should Be Equal As Integers    200    ${vsdc_code} 
    
CHANGE METER "${meter_id} STATUS TO "${status}" IN ODM DB
    Change Meter Status    ${PROJECT}    ${odm_db_name}    ${meter_id}    ${status}
    Sleep    3s
    
ASSERT NO MBUS TASKS IN M2M AND VSDC FOR DEVICE "${GAZ_meterID_to_delete}"
    ${mbus_code}    ${amr_router}    ${mbus_chanel}    ${energy_type}    Get Mbus Channel    ${PROJECT}    ${GAZ_meterID_to_delete}
    ${code}    ${validation}    ${reason}    Check Task Mbus In M2m    ${PROJECT}    ${amr_router}    ${mbus_chanel}    ${energy_type}
    Should Be True    ${validation}       
    ${code}    ${validation}    ${reason}    Check Task Mbus In Vsdc    ${PROJECT}    ${amr_router}    ${mbus_chanel}    ${energy_type}
    Should Be True    ${validation}    
    
ASSERT CDC CAPA NOT SENT
    [Arguments]    ${meterID}    ${timeout}
    ${CapaQueue}   Read Conf    ${PROJECT}    CapaQueue  
    Capa_Not_Sent    ${CapaQueue}    ${meterID}    ${timeout}    ['SET_CDC']    ['Connected']    ['true'] 
    
ASSERT SLA DELIVERY PARAMS "${item_capa}" UPDATED FOR METER "${WATER_meterID}"  
    ${sla_params_updated}    Sla Delivery Params Updated    ${PROJECT}    ${WATER_meterID}    ${item_capa}
    Should Be True    ${sla_params_updated}  
Capa_Not_Sent
    [Arguments]    ${CapalQueue}    ${meterID}    ${timeout}    ${params_buffer}   ${params_values_buffer}    ${params_availability_buffer}
    ${code}    ${message}    consume CAPA from AMQ    ${CapalQueue}    ${meterID}    ${timeout}
    Log    ${message} 
    Should Be Equal As Integers    ${code}     408    
    
ASSERT ODM GUI UPDATED
    [Arguments]    ${driver}    ${WATER_meterID}    ${data}
     ${odm_url}   Read Conf    ${PROJECT}    odm_url 
     go to meter details    ${driver}    ${odm_url}meter/config-parameter/consult/${WATER_meterID} 
     ${validation_odm_params}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ${data}[0]    ${data}[1]
     Should Be True    ${validation_odm_params}
    
ASSERT ODM GUI UPDATED HES1_6
    [Arguments]    ${driver}    ${WATER_meterID}    ${data}
     ${odm_url}   Read Conf    ${PROJECT}    odm_url 
     go to meter details    ${driver}    ${odm_url}meter/config-parameter/consult/${WATER_meterID}/mdms
     ${validation_odm_params}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ${data}[0]    ${data}[1]
     Should Be True    ${validation_odm_params} 
ASSERT CDC_ODM GUI UPDATED TO "${cdc_value}" FOR METER "${meterID}" USE DRIVER "${driver}"
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    go to meter details    ${driver}    ${odm_url}meter/config-parameter/consult/${meterID} 
    
    ${var} =  Set Variable If
    ...  "${cdc_value}"=="connected"    true
    ...  "${cdc_value}"=="disconnected"    false   
    ${validation_odm_params1}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ['CDC']    ['${var}']
    ${validation_odm_params2}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ['CDC']    ['${cdc_value}']
    @{items}    Create List
    Append To List    ${items}    ${validation_odm_params1}    ${validation_odm_params2}
    @{items2}    Create List
    Append To List    ${items2}    ${True}     
    List Should Contain Sub List    ${items}     ${items2} 
    
ASSERT CAMPAIGN FIRMWARE STATUS "${status}" FOR CAMPAIGN ID "${camp_id}"
    ${odm_url}   Read Conf    ${PROJECT}    odm_url 
    ${siconia_user}   Read Conf    ${PROJECT}    siconia_user 
    ${siconia_pass}   Read Conf    ${PROJECT}    siconia_pass 
    ${driver}    Init Driver
    Open Gui    ${driver}    ${odm_url}    ${siconia_user}    ${siconia_pass}
    go to meter details    ${driver}    ${odm_url}campaign/firmware-upgrade/${camp_id}
    ${odm_camp_status}    ${reason}    Check Campaign Status Odm    ${driver}     Status    ${status}    ${camp_id}  
    Should Be True    ${odm_camp_status}   
    #${validation_odm_params}    ${fail reason}    Check Config Paramete Gui Updated    ${driver}    ['DISPLAY_STATE','PREPAYMENT_STATE']    ['false', 'false']
    #Should Be True    ${validation_odm_params}
    Close Driver    ${driver}

ASSERT CAMPAIGN FIRMWARE STATUS "${status}" FOR CAMPAIGN NAME "${name}"    
    ${final_status}    Verify Campaign Status    ${PROJECT}    ${odm_db_name}    firmware_campaign    ${name}
    Should Be Equal    ${final_status}    ${status}  
    
ASSERT SSF PARAMS ARE WELL IMPORTED IN ODM FOR SSF "${ssf_name}" USE DRIVER "${driver}" AND METER CATEGORY "${meter_type}"
    ${params}    Get Ssf Parameters    ${PROJECT}    ${ssf_name}    ${meter_type}
    ${validation}    Validate Shipment Parameters Odm Gui    ${driver}    ${PROJECT}    ${ssf_name}    ${params}    ${meter_type}
    Should Be True    ${validation}  
    ${sla_status_validation}    Verify Meters Status In Sla    ${PROJECT}     ${params}
    Should Be True    ${sla_status_validation}    
 
ASSERT SSF PARAMS ARE WELL IMPORTED IN OEM FOR SSF "${ssf_name}" USE DRIVER "${driver}"
    ${params}    Get Dc Ssf Parameters    ${PROJECT}    ${ssf_name}  
    ${validation}    Validate Shipment Parameters Oem Gui    ${driver}    ${PROJECT}    ${ssf_name}    ${params}   
    Should Be True    ${validation}  
    ${sla_status_validation}    Verify Dcs Status In Sla    ${PROJECT}     ${params}
    Should Be True    ${sla_status_validation}  
       
ASSERT ODR VALIDATION OF MONO METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
    ${result_odr_validation}    Valid ODR    ${PROJECT}    ODR_MONO    ${XMLreply}    ${profile}  
    Should Be True    ${result_odr_validation} 
 
ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
    ${result_odr_validation}    Valid ODR    ${PROJECT}    ODR_TRI    ${XMLreply}    ${profile}  
    Should Be True    ${result_odr_validation} 
    
ASSERT CHECK VSDC MAPPING FOR SSF "${ssf_name}"
    ${list_din}    ${list_ldn}    Get Meters Din Ldn From Ssf   ${PROJECT}    ${ssf_name}
    Log    ${list_din}    
    Log    ${list_ldn}
    FOR    ${i}    IN RANGE    len(${list_ldn}) 
        ${check_result}    Check Vsdc Mapping    ${PROJECT}    ${list_din}[${i}]    ${list_ldn}[${i}]
        Should Be True     ${check_result}    
    END

ASSERT CHECK M2M METER MAPPING FOR SSF "${ssf_name}"
    ${list_din}    ${list_ldn}    Get Meters Din Ldn From Ssf   ${PROJECT}    ${ssf_name}
    Log    ${list_ldn}
    FOR    ${i}    IN RANGE    len(${list_ldn}) 
        ${check_result}    Check M2m Dc Mapping    ${PROJECT}    ${list_din}[${i}]    ${list_ldn}[${i}]
        Should Be True     ${check_result}    
    END
     
ASSERT CHECK M2M DC MAPPING FOR SSF "${ssf_name}"
    ${list_din}    ${list_ldn}    Get DCs Din Ldn From Ssf   ${PROJECT}    ${ssf_name}
    Log    ${list_ldn}
    FOR    ${i}    IN RANGE    len(${list_ldn}) 
        ${check_result}    Check M2m Dc Mapping    ${PROJECT}    ${list_din}[${i}]    ${list_ldn}[${i}]
        Should Be True     ${check_result}    
    END
       
ASSERT COMPARING CIM AND M2M ODR RESULT
    [Arguments]    ${correlationID}    ${profile}    ${XMLreply}    ${meter_type}
    ${job_id}    Get Job Id From Cim    ${PROJECT}    ${correlationID}
    ${validation}    Validate Cim Odr Output    ${PROJECT}    ${job_id}    ${meter_type}    ${profile}    ${XMLreply}
    Should Be True    ${validation}  
  
ASSERT validate task stop date
    [Arguments]    ${correlationID}    ${profile}    ${XMLreply}    ${meter_type}
    ${job_id}    Get Job Id From Cim    ${PROJECT}    ${correlationID}
    ${validation}    Validate Cim Odr Output    ${PROJECT}    ${job_id}    ${meter_type}    ${profile}    ${XMLreply}
    Should Be True    ${validation} 
    
ASSERT COMPARING CIM AND M2M ODR EVENT RESULT
    [Arguments]    ${correlationID}    ${profile}    ${XMLreply}   
    ${job_id}    Get Job Id From Cim    ${PROJECT}    ${correlationID}
    ${validation}    Validate Cim Odr Event Output    ${PROJECT}    ${job_id}   ${profile}    ${XMLreply}
    Should Be True    ${validation}  
 
ASSERT COMPARING CIM AND M2M ODR LP2 RESULT
    [Arguments]    ${correlationID}    ${profile}    ${XMLreply}    ${meter_type}
    ${job_id}    Get Job Id From Cim    ${PROJECT}    ${correlationID}
    ${validation}    Validate Cim Odr LP2 Output    ${PROJECT}    ${job_id}    ${meter_type}    ${profile}    ${XMLreply}
    Should Be True    ${validation} 
   
ASSERT COMPARING CIM AND M2M ODR LP1 RESULT
    [Arguments]    ${correlationID}    ${profile}    ${XMLreply}    ${meter_type}
    ${job_id}    Get Job Id From Cim    ${PROJECT}    ${correlationID}
    ${validation}    Validate Cim Odr LP1 Output    ${PROJECT}    ${job_id}    ${meter_type}    ${profile}    ${XMLreply}
    Should Be True    ${validation} 
          
ASSERT DC CONFIG "${file}" IS "${status}"
    ${conf_db_status}    Verify Config Upload Status    ${PROJECT}    ${file}
    Should Be Equal As Strings    ${conf_db_status}    ${status}  
    

ASSERT DC CONFIG "${file}" IS UPLOADED IN SCAPE PROD
    ${conf_db_status}    Verify Config Uploaded In Scape Prod    ${PROJECT}    ${file}
    Should Be True   ${conf_db_status}   
    
ASSERT DC CONFIG "${file}" IS UPLOADED IN SCAPE QA
    ${conf_db_status}    Verify Config Uploaded In Scape Qa    ${PROJECT}    ${file}
    Should Be True   ${conf_db_status} 
    
ASSERT DC FW "${file}" IS "${status}"
    ${conf_db_status}    Verify firmware Upload Status    ${PROJECT}    ${file}
    Should Be Equal As Strings    ${conf_db_status}    ${status}  
    
ASSERT DC FIRMWARE "${file}" IS UPLOADED IN SCAPE PROD
    ${conf_db_status}    Verify Firmware Uploaded In Scape Prod    ${PROJECT}    ${file}
    Should Be True   ${conf_db_status}  
    
ASSERT DC FIRMWARE "${file}" IS UPLOADED IN SCAPE QA
    ${conf_db_status}    Verify Firmware Uploaded In Scape Qa    ${PROJECT}    ${file}
    Should Be True   ${conf_db_status}  
    
#FOR ESO 
ASSERT "${ODR_CSV}" VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
    ${result_odr_validation}    Valid ODR    ${PROJECT}    ${ODR_CSV}    ${XMLreply}    ${profile}  
    Should Be True    ${result_odr_validation} 