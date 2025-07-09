*** Settings ***
Library    ../libraries/CANLibrary.py
Library    ../libraries/ECULibrary.py
Library    ../../.venv/lib/python3.12/site-packages/robot/libraries/OperatingSystem.py
Library    SeleniumLibrary
Test Setup    Connect To CAN    ${CAN_channel}

*** Variables ***
${CAN_channel}    vcan0   
${vin_value}    9043
${browser}    Chrome
${Login_url}    https://www.google.com


*** Test Cases ***
Test CAN Communication
    [Documentation]
    [Tags]    Smoke_testing    Regression_testing
    Send CAN Message    0x123    01 02 03   
    ${CAN_LOG_FILE}=    Normalize Path    ${CURDIR}/../outputs/output.blf
    Create File    ${CAN_LOG_FILE}
    Log Can Traffic    10    ${CAN_LOG_FILE} 

Test ECU Reset
    Send Can Message    0x7E0    11 01
    &{result}=    Receive Can Message
    Should Be Equal    ${result}[Data]    5101

Test VIN Data Read
    Send Can Message    0x7E0    22 F1 90
    &{vin}=    Receive Can Message
    Log    Vin value read is ${vin}[Data]
    Should Contain    ${vin}[Data]    ${vin_value}

# Test ECU Diagnostics
#     Connect To ECU    tx_id=0x7E0    rx_id=0x7E8
#     ${vin}=    Read ECU Data    F190
#     Should Contain    ${vin}    4D594456    # "MYVD" VIN prefix


Test Selenium Working
    [Setup]    Open Browser    ${Login_url}    ${browser}

    Wait Until Page Contains Element    css:input.gNO89b    10s
    ${elements}=    Get WebElements    css:input.gNO89b
    
    Should Not Be Empty    ${elements}
    Log    Found ${elements.__len__()} elements with the selector
    Log    First element text/value: ${elements[0].get_attribute('value')}
    
    [Teardown]    Close Browser