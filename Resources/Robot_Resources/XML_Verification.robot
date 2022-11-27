*** Settings ***

Documentation     TBD
Library    ../../Libraries/XML_Libraries/XML_Verification_Library.py        

*** Variables ***

*** Keywords ***


Get Reply Code

    [Arguments]    ${xml}     
    [Documentation]    TBD
    ${ReplyCode}    Get Value By Path    reply/replyCode    ${xml}
    [Return]        ${ReplyCode} 
    

Get Reply Text

    [Arguments]    ${xml}     
    [Documentation]    TBD
    ${ReplyText}    Get Value By Path    reply/replyText    ${xml}
    [Return]        ${ReplyText} 