*** Settings ***
Resource    ../Resources/Robot_Resources/Assert.robot
Resource    ../Resources/Robot_Resources/StandardKeywords.robot

Library    ../Libraries/Log_Parser_Libraries/VSDC_P2P_Parser.py    
Library  DateTime
Variables    ../Libraries/Read_Config/ConfigVariables.py   C:\Users\g551651\Desktop\Test_auto_esb_project\system_e2e_automation_tests-SYSTEM_AUTO_ESB\Configurations\ESB_config.ini
#*** Variables ***

#${RequestQueue}    MDMS_CONFIG_QUEUE   

#${meterID}    	80043700621611125392485321770067

#${ReadsQueue}    MDMS_HES_METER_READINGS_QUEUE
#${ReadsQueueResponse}    HES_MDMS_METER_READS_REPLY_AUTO
#${timeout}    120
#${projct}    ESB

#${ssf_name}    AMMSAG00001234567-00010-253907323-0.20220107145013_Meter_amm.xml
#${ssf_remote_path}    /var/sharedFolder/AM/busOdmSharedFolder/ShipmentFile/
*** Test Cases ***

clean_amq
    ${assetQueueResponse}    Read Conf    ${projct}    assetQueueResponse
    ${controlQueueResponse}    Read Conf    ${projct}    controlQueueResponse
    ${readsQueueResponse}    Read Conf    ${projct}    readsQueueResponse
    
    ${out}    Clean Queue    ${assetQueueResponse}
    ${out1}    Clean Queue    ${controlQueueResponse}
    ${out2}    Clean Queue    ${ReadsQueueResponse}

    
TC_SYS-192_EVN:Import_SSF_New_Meter
    ${odm_url}   Read Conf    ESB    odm_url 
    ${driver}    Init Driver
    Given login to page    ${driver}    ${odm_url}
    When clean db without kms   ${ssf_name}    ${ssf_remote_path}
    sleep  10s
    Then Import New Ssf    ${driver}    ESB    ${ssf_name}
    #Then Import New Ssf    ${driver}    C:\\Users\\g361355\\Desktop\\ROBOT_ECLIPSE\\E2E-AUTO-SICONIA\\Resources\\SSF_Files\\EVN\\SSFSAG9363266741-57854-7709328713-863728532411874-19309-253800628-0.20210621145548_PLC.xml
    And verify_ssf_import_ok_standard    ${ssf_name}
    Close Driver    ${driver}



SOLESB-5136:ODR_P14_MAXIMUM_DEBIT1+RESET
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_P14_MAXIMUM_DEBIT1
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 
        
        #flag validation
        # ASSERT FLAG VALID OF "${XMLreply}"
        
        #cim result validation
        #ASSERT CIM ODR VALIDATION FOR REPLY "${XMLreply}" USING PROFILE "${profile}"
        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END



SOLESB-5134:MCC01_REGISTER
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    MCC01_REGISTER
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
SOLESB-5379
    [documentation]   ADM_Get_Device_Configuration_MCC12
    [Tags]    sanity    MCC11
    ${value}    Set Variable    MCC11
    ${project}    Set Variable    ESB
    ${RequestQueue}    Set Variable    MDMS_HES_CONFIG_QUEUE
    ${ResponseQueue}    Set Variable    HES_MDMS_CONFIG_REPLY_QUEUE
    ${meterID}    Set Variable    800437006216111392485321770126
    ${path}    Set Variable    payload/requestedProfiles/type                   
    Log    TEST STARTED
    ${correlationID}    Prepare_Inject_Consume_Message    ${project}    ${RequestQueue}    ${meterID}    ADM_GET_DEVICE_CONFIGURATION    ${path}    ${value}
    Log    ${correlationID}
    ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ResponseQueue}    ${correlationID}    350
    Log    ${XMLreply}   
    Log    ${XMLreply} 
    Log    ${replaycode}                            
    ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}"
    ${validation}    ASSERT CHECK TASK IN VSDC
    Should Be True    ${validation}
    ${validation}    ASSERT HES OPERATION DURATION       
    Should Be True    ${validation}
    ${result}     ASSERT HES OPERATION RETRY PAUSE
    Should Be True    ${result}    
                     
       
    
SOLESB-5131:MCC01_INTERVAL
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    MCC01_INTERVAL
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END

SOLESB-5124:MCC16_REGISTER
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    MCC16_REGISTER
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END

SOLESB-5121:MCC16_INTERVAL
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    MCC16_INTERVAL
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
   
SOLESB-5129:MCC12_REGISTER
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    MCC12_REGISTER
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
     
SOLESB-5126:MCC12_INTERVAL
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    MCC12_INTERVAL
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
    

SOLESB-5120:ODR_DEBIT1_MONTHLY
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_DEBIT1_MONTHLY
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
    

SOLESB-5118:ODR_A14_DEBIT1
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_A14_DEBIT1
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
    

    
SOLESB-5116:ODR_A23_DEBIT1
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_A23_DEBIT1
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
    

SOLESB-5114:ODR_A14_TOU_123_DEBIT1
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_A14_TOU_123_DEBIT1
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
    
SOLESB-5112:ODR_P14_MAXIMUM_DEBIT1
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_P14_MAXIMUM_DEBIT1
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
    
SOLESB-5110:ODR_POWER_QUALITY_REGISTERS
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_POWER_QUALITY_REGISTERS
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
    
SOLESB-5020:On_Demand_Read_ODR_CIM_EVENTS_Events_Data_retrieval

    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_CIM_EVENTS
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END

SOLESB-5016:On_Demand_Read_ODR_CIM_STD_EVENTS_Events_Data_retrieval
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_CIM_STD_EVENTS
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
    
SOLESB-5014:On_Demand_Read_ODR_CIM_VQ1_EVENTS_Events_Data_retrieval
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_CIM_VQ1_EVENTS
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
 
SOLESB-5012:On_Demand_Read_ODR_CIM_FRAUD_EVENTS_Events_Data_retrieval
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_CIM_FRAUD_EVENTS
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END

SOLESB-5010:On_Demand_Read_ODR_CIM_DISCONNECT_EVENTS_Events_Data_retrieval
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_CIM_DISCONNECT_EVENTS
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
   
SOLESB-5006:On_Demand_Read_ODR_CIM_ACCESS_EVENTS_Events_Data_retrieval
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_CIM_ACCESS_EVENTS
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 

    END
  
SOLESB-5001:On_Demand_Read_ODR_CURRENTL1AVERAGE_INST_Instantaneous_Data_retrieval
    [Tags]    sanity    INST
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_CURRENTL1AVERAGE_INST
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END
 
SOLESB-4999:On_Demand_Read_ODR_VOLTAGEL1AVERAGE_INST_Instantaneous_Data_retrieval
    [Tags]    sanity    INST
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_VOLTAGEL1AVERAGE_INST
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END 
    
SOLESB-4997:On_Demand_Read_ODR_P14_MAXIMUM_INST_Instantaneous_Data_retrieval
    [Tags]    sanity    INST
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_P14_MAXIMUM_INST
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END   
    
SOLESB-4995:On_Demand_Read_ODR_A14_TOU_123_INST_Instantaneous_Data_retrieval
    [Tags]    sanity    INST
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_A14_TOU_123_INST
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END   
  
SOLESB-4993:On_Demand_Read_ODR_A23_INST_Instantaneous_Data_retrieval
    [Tags]    sanity    INST
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_A23_INST
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END  
 
SOLESB-4991:On_Demand_Read_ODR_A14_INST_Instantaneous_Data_retrieval
    [Tags]    sanity    INST
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_A14_INST
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END              
  
SOLESB-4988:On_Demand_Read_ODR_ALL_INST_Instantaneous_Data_retrieval
    [Tags]    sanity    INST
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_ALL_INST
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END   
   
SOLESB-4978:On_Demand_Read_PQC_ODR_Nominal_case
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_PQC
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END   
        
    END  
  
SOLESB-4974:On_Demand_Read_LP2_ODR_Nominal_case
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    LP2_ODR
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END   
 
SOLESB-4972:On_Demand_Read_LP1_ODR_Nominal_case
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    LP1_ODR
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END  


SOLESB-4917:ODR_ALL_ANALYSIS
    [Tags]    sanity    prio2
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_ALL_ANALYSIS
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END  
        
        
SOLESB-4686:ODR_All_BILLING
    [Tags]    sanity    
    #PRECONDITION 
    Log    DATASET PREPARATION
    @{req_priority}    Create List
    @{rexec_priority}    Create List
    @{Recovery_Priority}    Create List
    @{end_date_shift}    Create List
    Append To List    ${req_priority}    1
    Append To List    ${rexec_priority}    7
    Append To List    ${Recovery_Priority}    5
    Append To List    ${end_date_shift}    5
 
    ${collect_file}    Read Conf    ${projct}    project_local_path
    ${profile}    Set Variable    ODR_BILLING_READ 
    
    Log    TEST STARTED
    FOR    ${i}    IN RANGE   len(${req_priority})
        #prepare and inject the message into activemq
        ${correlationID}    Prepare_Inject_ODR_Message    ${meterID}    ELEC_ODR    ${profile}    ${req_priority}[${i}]
        
        # m2m parameters validation
        ${result}    Validate ExecPriority And Reqenddate Per Minute    ${projct}    ODR    ${correlationID}    ${rexec_priority}[${i}]    ${Recovery_Priority}[${i}]    ${end_date_shift}[${i}]
        Should Be True    ${result}  
        
        #consume the response
        ${code}    ${XMLreply}    ${replaycode}    ${response_dateTime}    Consume from AMQ    ${ReadsQueueResponse}    ${correlationID}    120
        Log    ${XMLreply} 
        Should Be Equal As Integers    0    ${replaycode} 

        ASSERT ODR VALIDATION OF TRI METER FOR XML "${XMLreply}" AND PROFILE "${profile}"
        # SLA demand validation 
        ASSERT SLA DEMAND WITH CORRELATION_ID "${correlationID}" UPDATED WITH STATUS "SUCCESS" AND response_dateTime "${response_dateTime}" 
    END 







parsing
    
    ${CurrentDate}=  Get Current Date  result_format=%Y-%m-%d %H:%M:%S.%f
    Log    ${CurrentDate}
    ${out}    Vsdc Push On Connectivity    ESB    ${CurrentDate}    SAG1020121770002    1
    Log    ${out}
    
parsing2
    
    ${CurrentDate}=  Get Current Date  result_format=%Y-%m-%d %H:%M:%S.%f
    Log    ${CurrentDate}
    ${out}    Vsdc Push On Interval    ESB    ${CurrentDate}    SAG1020121770002    1
    Log    ${out}