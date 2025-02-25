*** Settings ***
Library  Browser
Resource  config.resource

*** Keywords ***
Ouvrir Le Navigateur
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
    New Page    ${URL}

Fermer Le Navigateur
    Close Browser
