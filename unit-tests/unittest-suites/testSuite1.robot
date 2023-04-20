*** Settings ***
Library     Browser

*** Test Cases ***
Test Case D 1.1.1
    [Tags]      A
    New Browser     browser=chromium    headless=True
    New Page        https://todomvc.com/examples/react/#/
    Fill Text       input.new-todo      Hello
    Press Keys      input.new-todo      Enter
    Fill Text       input.new-todo      CGI!
    Press Keys      input.new-todo      Enter
    Take Screenshot

Test Case D 1.1.2
    [Tags]      GroupingTagB
    New Browser     browser=chromium    headless=True
    New Page        https://todomvc.com/examples/react/#/
    Fill Text       input.new-todo      Have a nice day
    Press Keys      input.new-todo      Enter
    Take Screenshot
    Sleep           2

Test Case D 1.2.1
    [Tags]      A
    Sleep       4
    Log         Hey

Test Case D 1.2.2
    [Tags]      GroupingTagA
    Sleep       4
    Log         Hey

Test Case GroupTagA 1.1
    [Tags]      GroupingTagA    Cool Tag      Cooler Tag
    Sleep       4
    Log         Hey

Test Case GroupTagA 1.2
    [Tags]      Another Tag     Cooler Other Tag        GroupingTagA
    Sleep       5
    Log         Hey

Test Case GroupTagB 1.1
    [Tags]      GroupingTagB
    Sleep       2
    Log         Hey

Test Case NoTag/D 1.1
    [Tags]      B
    Sleep       5
    Log         Hey

Test Case NoTag/D 1.2
    [Tags]      B
    Sleep       10
    Log         Hey

Test Case Not In Output XML 1
    [Tags]      F
    Sleep       5
    Log         Hey

Test Case Not In Output XML 2
    [Tags]      F
    Sleep       5
    Log         Hey

