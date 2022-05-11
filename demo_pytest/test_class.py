# Group multiple tests in a class
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")  # assertion failed


class TestClassDemoInstance:
    value = 0
    
    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1  # assertion failed here cos value is 0


class NotToRun:  # this class won't run
    def test_one(self):
        x = 1
        assert x == 1
