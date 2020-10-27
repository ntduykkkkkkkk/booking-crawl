*** Settings ***
Resource   ../Common/Common.robot

Suite Setup
Suite Teardown   Close Browser

Test Setup  Run Keywords   Get Current Tag   Set Data   Select Library

