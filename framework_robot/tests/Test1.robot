*** Settings ***
Library    ../libraries/CANLibrary.py
Library    ../libraries/ECULibrary.py
Library    ../../.venv/lib/python3.12/site-packages/robot/libraries/OperatingSystem.py

*** Test Cases ***
Test CAN Communication
    Connect To CAN    vcan0
    Send CAN Message    0x123    01 02 03   
    ${CAN_LOG_FILE}=    Normalize Path    ${CURDIR}/../outputs/output.blf
    Create File    ${CAN_LOG_FILE}
    Log Can Traffic    10    ${CAN_LOG_FILE} 

Test ECU Diagnostics
    Connect To ECU    tx_id=0x7E0    rx_id=0x7E8
    ${vin}=    Read ECU Data    F190
    Should Contain    ${vin}    4D594456    # "MYVD" VIN prefix