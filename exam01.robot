*** Settings ***
Library    SeleniumLibrary
Library    BuiltIn
Library    String
Test Teardown      Close All Browsers

*** Variables ***
${URL}                      https://www.seleniumeasy.com/test/
${Browser}                  chrome
${DELAY}                    0

${table_list}               //*[@id="treemenu"]/li/ul/li[3]
${table_sort_search}        //*[@id="treemenu"]//*[contains(text(),"Table Sort & Search")]
${age_column}               //*[@id="example"]//*[contains(text(),"Age")]
${age_descending}           //*[@id="example"]//*[contains(text(),"66")]
${age_ascending}            //*[@id="example"]//*[contains(text(),"19")]
${close_popup}              //*[@id="at-cv-lightbox-close"]


*** Keywords ***
Open Selenium Page
    Open browser              ${URL}    ${Browser}
    Maximize Browser Window
    Sleep   1s
    Click Element             ${close_popup}
    Capture Page Screenshot

Select 'Table' on Menu List
    Sleep   1s
    Click Element   ${table_list}
    Capture Page Screenshot

Select 'Table Sort and Search' on Table List
    Sleep   1s
    Click Element   ${table_sort_search}
    Capture Page Screenshot

Verify 'Age' column is sorted in descending order
    Sleep   1s
    Element Should Be Visible   ${age_descending}
    Capture Page Screenshot

Click 'Age' Colunm
    Sleep   1s
    Click Element   ${age_column}
    Capture Page Screenshot

Verify 'Age column is sorted in ascending order
    Sleep   1s
    Element Should Be Visible   ${age_ascending}
    Capture Page Screenshot


*** Test Cases ***
Sorting Age
    [tags]    success
    Open Selenium Page
    Select 'Table' on Menu List
    Select 'Table Sort and Search' on Table List
    Verify 'Age' column is sorted in descending order
    Click 'Age' Colunm
    Verify 'Age column is sorted in ascending order


