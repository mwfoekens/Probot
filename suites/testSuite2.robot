*** Test Cases ***
Test Case GroupTagA 2.1
    [Tags]      GroupingTagA
    [Documentation]     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Sleep       4
    Log         Hello World!

Test Case NoTag/D 2.1
    [Tags]      My Tag
    Sleep       4
    Log         Hello World!

Test Case D 2.2.3
    [Tags]      My Tag
    [Documentation]     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Simple Keyword
    Simple Keyword

*** Keywords ***
Simple Keyword
    Sleep   4
    Log    Hello World!
