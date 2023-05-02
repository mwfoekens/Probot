*** Test Cases ***
Test Case GroupTagA 2.1
    [Tags]      GroupingTagA        UNIT-TEST
    Sleep       4
    Log         Hello World!

Test Case NoTag/D 2.1
    [Tags]      My Tag          UNIT-TEST
    Sleep       4
    Log         Hello World!

Test Case D 2.2.3
    [Tags]      My Tag          UNIT-TEST
    Simple Keyword
    Simple Keyword

*** Keywords ***
Simple Keyword
    Sleep   4
    Log    Hello World!
