*** Settings ***

Documentation     Inject And consume Requests and responces from The AMQ North

Library    ../../Libraries/XML_Libraries/XML_Preparation_Library.py      

*** Variables ***
${meterID}    80043700621611125392485321770067
${path}    payload/requestedProfiles/type
${value}    MCC12  
*** Keywords ***

#Update requestedProfiles Xml Request
    #[Arguments]    ${xml}    ${path}    ${profilValue}
    #${XML}    Update Value By Path    ${xml}    ${path}    ${profilValue}
    #[Return]     ${XML}

DCT without params to inject

    [Arguments]    ${xml}    ${meterID}    ${path}    ${value}    
    [Documentation]    TBD
    ${XML}    ${correlationID}    Default Preparation EVN    ${meterID}    ${xml}    
    ${XML}    Update Value By Path    ${path}    ${value}    ${XML}
    [Return]     ${XML}    ${correlationID}
    

DCT with params to inject

    [Arguments]    ${xml}    ${mrid}    ${path}    ${meter_id_tag}    ${value}    ${paramName}
    [Documentation]    TBD
    ${XML}    ${correlationID}    Standard Default Preparation    ${mrid}    ${xml}    ${meter_id_tag}
    ${XML}    Update Value By Path    ${path}    ${value}    ${XML}
    ${XML}    Update Value By Param    ${XML}     ${value}    payload/meterAsset/parameter/name    payload/meterAsset/parameter/value    ${paramName}
    [Return]     ${XML}    ${correlationID}
    
Meter Update param
    
    [Arguments]    ${xml}    ${requestPriority}    ${paramName}    ${paramValue}
    #${XML}    ${correlationID}    Default Preparation EVN 2    ${mrid}    ${xml}
    ${XML}    Meter Updateparams By Param Name    ${xml}    ${paramName}    ${paramValue}
    [Return]     ${XML}

Request Update Mrid
    
    [Arguments]    ${xml}    ${mrid}    ${requestPriority}    ${meter_id_tag}
    ${XML}    ${correlationID}    Standard Default Preparation   ${mrid}    ${xml}    ${meter_id_tag}
    [Return]     ${XML}    ${correlationID}
Request Update Past Mrid
    
    [Arguments]    ${xml}    ${mrid}    ${meter_id_tag}    ${timeparam}    ${shift}
    ${XML}    ${correlationID}    Standard Default Preparation Past Date Time   ${mrid}    ${xml}    ${meter_id_tag}    ${timeparam}    ${shift}
    [Return]     ${XML}    ${correlationID}
Request Update Param
    
    [Arguments]    ${xml}    ${requestPriority}    ${paramName}    ${paramValue}
    ${XML}    Update Xml Request    ${xml}    ${paramName}    ${paramValue}
    [Return]     ${XML}

Request Update Param2
    
    [Arguments]    ${xml}    ${requestPriority}    ${paramName}    ${paramValue}
    ${XML}    Meter Updateparams By Param Name    ${xml}    ${paramName}    ${paramValue}
    [Return]     ${XML}
      
Meter Add param
    
    [Arguments]    ${project}    ${xml}    ${requestPriority}    ${paramName}    ${paramValue}
   # ${XML}    ${correlationID}    Default Preparation EVN 2    ${mrid}    ${xml}
    ${XML}    Meter Addparams By Param Name    ${project}    ${xml}    ${paramName}    ${paramValue}
    [Return]     ${XML}

Meter Delete param
    
    [Arguments]    ${xml}    ${mrid}    ${requestPriority}    ${paramName}    ${paramValue}
    ${XML}    ${correlationID}    Default Preparation EVN 2    ${mrid}    ${xml}
    ${XML}    Meter Deleteparams By Param Name    ${xml}    ${paramName}  
    [Return]     ${XML}    ${correlationID}
    

#####################
Request Update Value
    
    [Arguments]    ${value}    ${xml}   ${tag} 
    ${XML}    Update Text Message    ${value}    ${xml}   ${tag}        
    [Return]     ${XML} 
    
Request Update Mrid Intervall  
    [Arguments]    ${xml}    ${mrid}    ${requestPriority}    ${meter_id_tag}   ${starttime}    ${endtime}
    ${XML}    ${correlationID}    update Xml File With Intervall   ${mrid}    ${xml}    ${meter_id_tag}    ${starttime}    ${endtime} 
    [Return]     ${XML}    ${correlationID}