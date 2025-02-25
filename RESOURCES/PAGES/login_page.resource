*** Settings ***
Library  Browser


*** Variables ***
${USERNAME_INPUT}  \#user-name
${PASSWORD_INPUT}  \#password
${LOGIN_BUTTON}  \#login-button


*** Keywords ***
Entrer le username
    [Arguments]  ${username}
    Fill Text    ${USERNAME_INPUT}    ${username}

Entrer le password
    [Arguments]  ${password}
    Fill Text    ${PASSWORD_INPUT}    ${password}

Login
    Click    ${LOGIN_BUTTON}