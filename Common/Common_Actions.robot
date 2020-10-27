*** Settings ***
Library    PCNLibrary
Library    String
Library    OperatingSystem
Library    DateTime
Library    Screenshot
Library    Collections

Resource  Common_Locators.robot

*** Keywords ***
Read JSON
    [Arguments]   ${absolute_path}
    ${temp}=   Get File   ${absolute_path}
    ${json_data}=   Evaluate   json.loads('''${temp}''')    json
    [Return]   ${json_data}