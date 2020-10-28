*** Settings ***
Resource   locators.robot
Resource   ../../Common/main.robot

*** Keywords ***
Click Login Button
    Wait Until Element Is Visible   ${login_button}
    Click Element   ${login_button}

Click Normal Login Button
    Wait Until Element Is Visible   ${login_button_by_normal}
    Click Element   ${login_button_by_normal}

Put Data To Username And Password Fields
    [Arguments]   ${username}   ${password}
    Wait Until Element Is Visible   ${username_field}
    Input Text   ${username_field}   ${username}
    Wait Until Element Is Visible   ${password_field}
    Input Text   ${password_field}   ${password}

Click Submit Login Button
    Wait Until Element Is Visible   ${submit_login_button}
    Click Element   ${submit_login_button}

Switch To Library
    [Arguments]   ${url}
    Go To   ${url}
