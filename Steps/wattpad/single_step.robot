*** Settings ***
Resource   locators.robot

*** Keywords ***
Click Login Button
    Wait Until Element Is Visible   ${login_button}
    Click Element   ${login_button}

Click Normal Login Button
    Wait Until Element Is Visible   ${login_button_by_normal}
    Click Element   ${login_button_by_normal}

Put Data To Username And Password Fields
    [Arguments]   ${login_username}   ${login_password}
    Wait Until Element Is Visible   ${username}
    Input Text   ${username}
    Wait Until Element Is Visible   ${password}
    Input Text   ${login_password}

Click Submit Login Button
    Wait Until Element Is Visible   ${submit_login_button}
    Click Element   ${submit_login_button}

Switch To Library
    [Arguments]   ${url}
    Go To   ${url}
