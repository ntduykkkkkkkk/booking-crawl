*** Settings ***
Resource   single_step.robot

*** Keywords ***
Log in to Wattpad
    [Arguments]   ${data}
    Click Login Button
    Click Normal Login Button
    Put Data To Username And Password Fields    ${data['username']}   ${data['password']}
    Click Submit Login Button
