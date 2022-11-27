*** Settings ***

Documentation     Inject And consume Requests and responces from The AMQ North
Library    OperatingSystem

*** Variables ***
${plateforme}    ESB
${file_name}    ADM_GET_DEVICE_CONFIGURATION
*** Keywords ***

Armed Connect request
    ${TextFileContent}=    Get File    ./Resources/xml/ArmedConnect.xml
    [Return]    ${TextFileContent}   
    
Disconnect request
    ${TextFileContent}=    Get File     ./Resources/xml/Disconnect.xml
    [Return]    ${TextFileContent} 

Connect request_EVN
    [Arguments]    ${plateforme}
    ${TextFileContent}=    Get File     ./Resources/${plateforme}/XML/MeterConnect.xml
    [Return]    ${TextFileContent}

SET_BILLING_RECORDING request EVN
    [Arguments]    ${plateforme}
    ${TextFileContent}=    Get File     ./Resources/XML_Files/${plateforme}/SET_BILLING_RECORDING.xml
    [Return]    ${TextFileContent}

SET_LP_RECORDING request EVN
    [Arguments]    ${plateforme}
    ${TextFileContent}=    Get File     ./Resources/XML_Files/${plateforme}/SET_LP_RECORDING.xml
    [Return]    ${TextFileContent}
 
GET_XML_REQUEST
    [Arguments]    ${plateforme}    ${file_name}
        
    ${TextFileContent}=    Get File    ../Resources/XML_Files/${plateforme}/${file_name}.xml
    [Return]    ${TextFileContent}

         
Disconnect request_EVN
    [Arguments]    ${plateforme}
    #${template}    Resources/EVN/XML/MeterDisconnect.xml
    ${TextFileContent}=    Get File     ../Resources/XML_Files/${plateforme}/MeterDisconnect.xml
    log    ${TextFileContent}
    [Return]    ${TextFileContent}   

SetSwitchPoint request
    ${TextFileContent}=    Get File     ./Resources/xml/SetSwitchPoint.xml
    [Return]    ${TextFileContent} 