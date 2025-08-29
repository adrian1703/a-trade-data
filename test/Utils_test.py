import pytest

from app.helper.Utils import Utils


class DummyClass:
    class_var = 42

    def __init__(self):
        self.foo = "bar"
        self.lst = [1, 2, 3]

    def greet(self):
        return "hello"

def run_tests():
    print("--- Test: int ---")
    Utils.inspect(123)

    print("\n--- Test: str ---")
    Utils.inspect("testing inspect")

    print("\n--- Test: float ---")

    print("\n--- Test: bool ---")
    Utils.inspect(True)

    print("\n--- Test: None ---")
    Utils.inspect(None)

    print("\n--- Test: list ---")
    Utils.inspect([1, 2, "a"])

    print("\n--- Test: tuple ---")
    Utils.inspect((1, 2, 3))

    print("\n--- Test: set ---")
    Utils.inspect({"a", "b", "c"})

    print("\n--- Test: dict ---")
    Utils.inspect({"a": 1, "b": "two", "c": [3, 4]})

    print("\n--- Test: simple object instance ---")
    obj = DummyClass()
    Utils.inspect(obj)

    print("\n--- Test: class ---")
    Utils.inspect(DummyClass)
    # more for seeing how it prints than actual test logic
    assert 1 == 1