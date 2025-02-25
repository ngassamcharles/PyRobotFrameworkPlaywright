*** Settings ***
Resource  ../RESOURCES/PAGES/login_page.resource
Resource  ../RESOURCES/config.resource
Resource  ../RESOURCES/common.resource


Suite Setup  Ouvrir Le Navigateur
Suite Teardown  Fermer Le Navigateur

*** Variables ***
${USERNAME}  standard_user
${PASSWORD}  secret_sauce


*** Test Cases ***
Test De Login
    Entrer le username    ${USERNAME}
    Entrer le password    ${PASSWORD}
    Login

