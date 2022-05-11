import pytest


@pytest.fixture
def my_fixture():
    print("run my_fixture()")
    return [1]


def test_foo(my_fixture):
    my_fixture.append(2)
    print("\nrun test_foo() after test summary")
    assert my_fixture == [1, 2]
