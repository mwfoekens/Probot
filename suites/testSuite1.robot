*** Settings ***
Library     Browser
Library     ${CURDIR}/my_robot_func.py

*** Test Cases ***
Test Case D 1.1.1
    [Tags]          My Tag
    New Browser     browser=chromium    headless=True
    New Page        https://todomvc.com/examples/react/dist/
    Add New Todo "Hello"
    Add New Todo "RoboCon!"
    Take Screenshot

Test Case D 1.1.2
    [Tags]          GroupingTagB
    [Documentation]     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Open ToDo App
    Fill Text       input.new-todo      Have a nice day
    Press Keys      input.new-todo      Enter
    Take Screenshot
    Sleep           4

Test Case D 1.2.1
    [Tags]      My Tag 2
    Sleep       4
    Log         Hello World!

Test Case D 1.2.2
    [Tags]          GroupingTagA
    Open ToDo App
    Add New Todo "This one will fail"
    Get Text        span.todo-count    ==    3 items left!
    Log             This one is meant to fail

Test Case GroupTagA 1.1
    [Tags]      GroupingTagA    My Tag      Another Tag
    Sleep       4
    Log         Hello World!

Test Case GroupTagA 1.2
    [Tags]          Another Tag     Very Nice Tag        GroupingTagA
    Open ToDo App
    Fill Text       input.new-todo      Have a good time at RoboCon!
    Press Keys      input.new-todo      Enter
    Take Screenshot
    Sleep           5
    Log             Hello World!

Test Case GroupTagB 1.1
    [Tags]      GroupingTagB
    Sleep       10
    Log         Hello World!

Test Case NoTag/D 1.1
    [Tags]      Nice Tag
    Sleep       5
    Log         Hello World!

Test Case NoTag/D 1.2
    [Tags]          My Tag
    [Documentation]     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Open ToDo App
    Add New Todo "Learn Python"
    Add New Todo "Learn C#"
    Add New Todo "Learn Robot Framework"
    Take Screenshot
    Get Text        span.todo-count    ==    3 items left!
    Sleep           10
    Log             Hello World!

Test Case Not In Output XML 1
    [Tags]          Completely Different Tag
    ${rand_num}     Random Num
    ${rand_num}     Evaluate    ${rand_num} + 1
    Greet Someone    CGI
    Sleep           5
    Log             ${rand_num}

Test Case Not In Output XML 2
    [Tags]          Another Tag
    Open ToDo App
    Add New Todo "Present at RoboCon"
    Add New Todo "Have a good time"
    Take Screenshot
    Sleep           5
    Log             Hello World!

Test Case Not In Output XML 3
    [Tags]          Very Nice Tag
    Open ToDo App
    Add New Todo "Present at RoboCon"
    Take Screenshot

*** Keywords ***
Add New Todo "${todo}"
    Fill Text       input.new-todo      ${todo}
    Press Keys      input.new-todo      Enter

Open ToDo App
    [Tags]              Open ToDo App Tag
    [Documentation]     This is documentation for a keyword
    New Browser     browser=chromium    headless=True
    New Page        https://todomvc.com/examples/react/dist/