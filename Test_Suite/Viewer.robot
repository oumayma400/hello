*** Settings ***
Documentation     NR
Library           Remote    http://127.0.0.1:8270/    WITH NAME    remoteServer


*** Variables ***
${Link_type}      1



*** Test Cases ***



OpenAssociation   
    ${res}    Connect    Management_P0    ${Link_type}
    should be equal    ${res}    ${0}    Operation failed
    Close