*** Test Cases ***
Test Case GroupTagA 2.1
    [Tags]      GroupingTagA
    Sleep       4
    Log         Hello World!

Test Case NoTag/D 2.1
    [Tags]      A
    Sleep       4
    Log         Hello World!

Test Case D 2.2.3
    [Tags]      A
    Simple Keyword
    Simple Keyword

*** Keywords ***
Simple Keyword
    Sleep   4
    Log    Hello World!
