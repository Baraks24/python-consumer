import pytest

@pytest.fixture(scope="function",autouse=True)
def each():
    print("before each") #execute code before each test
    yield "someValue" #pass value to each test expecting the fixture function name as input, aka DI
    print("after each") #execute code after each test, can see print from cli with -v -s but doesnt appear in html.


def test_1(each):
    print("something")
    print(each)
    assert True == True
def test_2():
    assert True == True