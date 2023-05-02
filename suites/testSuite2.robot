*** Test Cases ***
Test Case GroupTagA 2.1
    [Tags]      GroupingTagA
    Sleep       4
    Log         Hello World!

Test Case NoTag/D 2.1
    [Tags]      My Tag
    Sleep       4
    Log         Hello World!

Test Case D 2.2.3
    [Tags]      My Tag
    Simple Keyword
    Simple Keyword

*** Keywords ***
Simple Keyword
    Sleep   4
    Log    Hello World!
