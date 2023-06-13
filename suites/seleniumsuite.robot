#*** Settings ***
#Library     SeleniumLibrary
#
#*** Test Cases ***
#Test Case Sel 1
##    ${options}=    Evaluate    sys.modules['selenium.webdriver'].FirefoxOptions()    sys, selenium.webdriver
##    Call Method    ${options}   add_argument  --no-sandbox
##    Call Method    ${options}   add_argument  --disable-dev-shm-usage
##    Call Method    ${options}   add_argument  --privileged
##    Call Method    ${options}   add_argument  --headless
##    Create Webdriver    FireFox      chrome_options=${options}       executable_path=/usr/local/bin/firefox
#
#    Open Browser    url=https://todomvc.com/examples/angularjs/#/    browser=headlessfirefox
#    Input Text    class:new-todo    Complete Robot Framework Training
#    Press Keys    class:new-todo    RETURN
#    Input Text    class:new-todo    Write Automated Tests
#    Press Keys    class:new-todo    RETURN
#    Input Text    class:new-todo    Take a nap
#    Press Keys    class:new-todo    RETURN
#    Capture Page Screenshot