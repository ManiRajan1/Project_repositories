*** Settings ***
Library    ../resources/Keywords.py

*** Test Cases ***
Basic Ignition Test
    Log To Console    Starting Robot Test
    Ignition On
    Sleep    2s
    Ignition Off