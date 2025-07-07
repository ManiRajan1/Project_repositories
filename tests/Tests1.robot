*** Settings ***
Library    ../resources/Keywords.py
Library    ../.venv/lib/python3.12/site-packages/robot/libraries/OperatingSystem.py

*** Keywords ***
Send CAN Message
    [Arguments]    ${can_id}    ${data}
    Log    Sending ID: ${can_id}, Data: ${data}

Configure ECU
    [Arguments]    ${baudrate}=500000    ${timeout}=2
    Log    Baudrate: ${baudrate}, Timeout: ${timeout}


*** Test Cases ***
Basic Ignition Test
    [Documentation]     This is a test file of Robot
    Set Test Variable    ${echo message}    "Hello"    #setting a variable in test
    
    Log To Console    Starting Robot Test
    Ignition On
    Sleep    2s
    Signal In    10
    Sleep    2s
    Ignition Off