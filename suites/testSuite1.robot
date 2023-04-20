*** Settings ***
Library     Browser

*** Test Cases ***
Test Case D 1.1.1
    [Tags]          A
    New Browser     browser=chromium    headless=True
    New Page        https://todomvc.com/examples/react/#/
    Add New Todo "Hello"
    Add New Todo "CGI!"
    Take Screenshot

Test Case D 1.1.2
    [Tags]          GroupingTagB
    Open ToDo App
    Fill Text       input.new-todo      Have a nice day
    Press Keys      input.new-todo      Enter
    Take Screenshot
    Sleep           2

Test Case D 1.2.1
    [Tags]      A
    Sleep       4
    Log         Hello World!

Test Case D 1.2.2
    [Tags]      GroupingTagA
    Sleep       4
    Log         Hello World!

Test Case GroupTagA 1.1
    [Tags]      GroupingTagA    Cool Tag      Cooler Tag
    Sleep       4
    Log         Hello World!

Test Case GroupTagA 1.2
    [Tags]          Another Tag     Cooler Other Tag        GroupingTagA
    Open ToDo App
    Fill Text       input.new-todo      Hello world!
    Press Keys      input.new-todo      Enter
    Take Screenshot
    Sleep           5
    Log             Hello World!

Test Case GroupTagB 1.1
    [Tags]      GroupingTagB
    Sleep       2
    Log         Hello World!

Test Case NoTag/D 1.1
    [Tags]      B
    Sleep       5
    Log         Hello World!

Test Case NoTag/D 1.2
    [Tags]      B
    Open ToDo App
    Add New Todo "Learn Python"
    Add New Todo "Learn Java"
    Add New Todo "Learn C#"
    Take Screenshot
    Get Text        span.todo-count    ==    3 items left
    Sleep           10
    Log             Hello World!

Test Case Not In Output XML 1
    [Tags]      F
    Sleep       5
    Log         Hello World!

Test Case Not In Output XML 2
    [Tags]      F
    Open ToDo App
    Add New Todo "Do robots dream of electric sheep?"
    Add New Todo "What is reality"
    Take Screenshot
    Sleep       5
    Log         Hello World!

*** Keywords ***
Add New Todo "${todo}"
    Fill Text       input.new-todo      ${todo}
    Press Keys      input.new-todo      Enter

Open ToDo App
    New Browser     browser=chromium    headless=True
    New Page        https://todomvc.com/examples/react/#/