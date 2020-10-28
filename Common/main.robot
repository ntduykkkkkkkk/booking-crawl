*** Settings ***
Resource   actions.robot

*** Keywords ***
Opening Resource's UI
    Start ${RESOURCE} UI

Get Data
    ${root_path}=   Get Root Path
    ${data}=   Read JSON   ${root_path}${/}Resources${/}setup.json
    [Return]   ${data}

Start ${resource_url} UI
    ${data}=   Get Data
    Open My Browser   ${data}

Export Global Data
    ${temp}=   Get Data
    Set Test Variable   ${data}   ${temp}