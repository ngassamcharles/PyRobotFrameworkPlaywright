*** Settings ***
Library  ${CURDIR}/../LIBRARIES/custom_keywords.py

Resource  ../RESOURCES/PAGES/login_page.resource
Resource  ../RESOURCES/custom_libs_api.resource
Resource  ../RESOURCES/config.resource
Resource  ../RESOURCES/common.resource
Resource  ../RESOURCES/api_config.resource


Suite Setup  Ouvrir Le Navigateur
Suite Teardown  Fermer Le Navigateur

*** Variables ***
${USERNAME}  standard_user
${PASSWORD}  secret_sauce


*** Test Cases ***
Test De Login UI
    Entrer le username    ${USERNAME}
    Entrer le password    ${PASSWORD}
    Login

Test API
    get request    ${API_URL}
    post request    ${API_URL}

