*** Settings ***
Library  Collections
Library    ../.venv/lib/python3.13/site-packages/Browser/browser.py

*** Keywords ***
Verifier Element Visible
    [Arguments]  ${locator}  ${message}=L'element doit etre visible.
    Wait For Elements State  ${locator}  visible  timeout=10s  message=${message}

Verifier Texte
    [Arguments]  ${locator}  ${expected_text}  ${message}=Le texte ne correspond pas.
    Should Be Equal As Strings    Get Text  ${locator}    ${expected_text}  ${message}