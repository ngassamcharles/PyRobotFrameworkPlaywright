*** Settings ***
Library  Browser


*** Keywords ***
get request
    [Arguments]  ${url}
    ${response}=    HTTP    ${url}    GET
    Should Be Equal    ${response.status}    ${200}

post request
    [Arguments]  ${url}
    ${response}=    HTTP    {url}    POST
    Should Be Equal    ${response.status}    ${200}

Verifier status HTTP
    [Arguments]  ${response}  ${code}
    Should Be Equal As Numbers    ${response.status_code}    ${code}