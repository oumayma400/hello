*** Settings ***

Documentation     Inject And consume Requests and responces from The AMQ North
   
Library    ../../Libraries/AMQ_Libraries/AMQ_Library.py    

*** Variables ***

${host}    172.31.12.72
${port}    8162
#61613
${queue}    MDMS_HES_CONFIG_QUEUE    
#${AMQUser}    m2m_user
#${AMQPass}    m2m_pass 

${AMQUser}    web-north    
${AMQPass}    web-north

*** Keywords ***
Inject into AMQ on Queue
    [Arguments]    ${queue}    ${XML}
    [Documentation]    Inject XML on  ${queue} queue
    Inject    ${XML}    ${queue}    ${host}    ${port}    ${AMQUser}    ${AMQPass}

Inject into AMQGUI on Queue
    [Arguments]    ${queue}    ${XML}
    [Documentation]    Inject XML on  ${queue} queue
    Inject With Gui    ${XML}    ${queue}    ${host}    ${port}    ${AMQUser}    ${AMQPass}
    
Consume from AMQ
    [Arguments]    ${queue}    ${correlationID}    ${timeout}
    [Documentation]    Consume XML with correlation ID = ${correlationID} from queue ${queue} 
    ${code}    ${XMLreply}    ${replaycode}    ${responsetime}     Consume    ${queue}    ${correlationID}    reply/correlationId     ${timeout}     ${host}    ${port}    ${AMQUser}    ${AMQPass}
    [Return]    ${code}    ${XMLreply}    ${replaycode}    ${responsetime} 

consume CAPA from AMQ
    [Arguments]    ${queue}    ${meterID}    ${timeout}
    [Documentation]    Consume Capabilities message for meter = ${meterID} from queue  ${queue} 
    ${code}  ${message}    ConsumeCapabilitiesAll    ${queue}    ${meterID}    ${timeout}    ${host}    ${port}    ${AMQUser}    ${AMQPass}
    [Return]   ${code}    ${message}    
    
Clean Queue
    [Arguments]    ${queue}
    Clean Queues   ${queue}    ${host}    ${port}    ${AMQUser}    ${AMQPass}