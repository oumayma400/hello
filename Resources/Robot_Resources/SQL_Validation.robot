*** Settings ***

Documentation     NR





Library    ../../Libraries/DB_Libraries/AccessDB.py           
 


*** Keywords ***
DB Validation
    [Arguments]    ${meterID}    ${list}
    FOR    ${i}    IN RANGE    len(${list[0]}) 
        ${str1} =   Catenate    SEPARATOR=    '    ${meterID}    _     ${list[0][${i}]}     '
        ${output}    Select    FLUVIUS    odm_db_2    odm    odm_db_user    odm_db_pass    current_value    metering_meter_config_param_info    mrid = ${str1}
        Should Be Equal    ${list[1][${i}]}    ${output}    
    END  

   
    
    