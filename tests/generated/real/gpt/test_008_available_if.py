import pytest
from sklearn.utils._available_if import available_if

class TestAvailableIf:
    def test_normal_case_available(self):
        class TestClass:
            def __init__(self, value):
                self.value = value

            def _is_positive(self):
                return self.value > 0

            @available_if(_is_positive)
            def positive_method(self):
                return "Positive"

        obj = TestClass(10)
        assert hasattr(obj, 'positive_method')
        assert obj.positive_method() == "Positive"

    def test_normal_case_unavailable(self):
        class TestClass:
            def __init__(self, value):
                self.value = value

            def _is_positive(self):
                return self.value > 0

            @available_if(_is_positive)
            def positive_method(self):
                return "Positive"

        obj = TestClass(-10)
        assert not hasattr(obj, 'positive_method')
        with pytest.raises(AttributeError):
            obj.positive_method()

    def test_edge_case_zero(self):
        class TestClass:
            def __init__(self, value):
                self.value = value

            def _is_non_negative(self):
                return self.value >= 0

            @available_if(_is_non_negative)
            def non_negative_method(self):
                return "Non-negative"

        obj = TestClass(0)
        assert hasattr(obj, 'non_negative_method')
        assert obj.non_negative_method() == "Non-negative"

    def test_exception_path(self):
        class TestClass:
            def __init__(self, value):
                self.value = value

            def _raise_exception(self):
                raise AttributeError("Method not available")

            @available_if(_raise_exception)
            def method(self):
                return "Should not be available"

        obj = TestClass(10)
        assert not hasattr(obj, 'method')
        with pytest.raises(AttributeError, match="Method not available"):
            obj.method()