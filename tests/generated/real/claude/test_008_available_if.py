import pytest
from sklearn.utils._available_if import available_if


class TestAvailableIf:
    def test_method_available_when_check_returns_true(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_positive(self):
                return self.value > 0
            
            @available_if(_check_positive)
            def get_double(self):
                return self.value * 2
        
        obj = MyClass(5)
        assert hasattr(obj, "get_double")
        assert obj.get_double() == 10
    
    def test_method_unavailable_when_check_returns_false(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_positive(self):
                return self.value > 0
            
            @available_if(_check_positive)
            def get_double(self):
                return self.value * 2
        
        obj = MyClass(-5)
        assert not hasattr(obj, "get_double")
    
    def test_method_unavailable_when_check_raises_attribute_error(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_has_attr(self):
                if not hasattr(self, "special_attr"):
                    raise AttributeError("special_attr not found")
                return True
            
            @available_if(_check_has_attr)
            def get_special(self):
                return self.special_attr
        
        obj = MyClass(5)
        assert not hasattr(obj, "get_special")
    
    def test_method_becomes_available_after_state_change(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_even(self):
                return self.value % 2 == 0
            
            @available_if(_check_even)
            def say_even(self):
                return "even"
        
        obj = MyClass(1)
        assert not hasattr(obj, "say_even")
        
        obj.value = 2
        assert hasattr(obj, "say_even")
        assert obj.say_even() == "even"
    
    def test_accessing_unavailable_method_raises_attribute_error(self):
        class MyClass:
            def __init__(self, enabled):
                self.enabled = enabled
            
            def _check_enabled(self):
                return self.enabled
            
            @available_if(_check_enabled)
            def do_something(self):
                return "done"
        
        obj = MyClass(False)
        with pytest.raises(AttributeError, match="do_something"):
            obj.do_something()
    
    def test_multiple_decorated_methods(self):
        class MyClass:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            
            def _check_x_positive(self):
                return self.x > 0
            
            def _check_y_positive(self):
                return self.y > 0
            
            @available_if(_check_x_positive)
            def method_x(self):
                return self.x
            
            @available_if(_check_y_positive)
            def method_y(self):
                return self.y
        
        obj = MyClass(5, -3)
        assert hasattr(obj, "method_x")
        assert not hasattr(obj, "method_y")
        assert obj.method_x() == 5
    
    def test_check_with_zero_returns_false(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_value(self):
                return self.value
            
            @available_if(_check_value)
            def get_value(self):
                return self.value
        
        obj = MyClass(0)
        assert not hasattr(obj, "get_value")
    
    def test_check_with_none_returns_false(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_value(self):
                return self.value
            
            @available_if(_check_value)
            def get_value(self):
                return self.value
        
        obj = MyClass(None)
        assert not hasattr(obj, "get_value")
    
    def test_check_with_empty_string_returns_false(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_value(self):
                return self.value
            
            @available_if(_check_value)
            def get_value(self):
                return self.value
        
        obj = MyClass("")
        assert not hasattr(obj, "get_value")
    
    def test_check_with_non_empty_string_returns_true(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_value(self):
                return self.value
            
            @available_if(_check_value)
            def get_value(self):
                return self.value
        
        obj = MyClass("hello")
        assert hasattr(obj, "get_value")
        assert obj.get_value() == "hello"
    
    def test_decorated_method_with_arguments(self):
        class MyClass:
            def __init__(self, enabled):
                self.enabled = enabled
            
            def _check_enabled(self):
                return self.enabled
            
            @available_if(_check_enabled)
            def add(self, a, b):
                return a + b
        
        obj = MyClass(True)
        assert obj.add(3, 4) == 7
    
    def test_decorated_method_with_kwargs(self):
        class MyClass:
            def __init__(self, enabled):
                self.enabled = enabled
            
            def _check_enabled(self):
                return self.enabled
            
            @available_if(_check_enabled)
            def greet(self, name, greeting="Hello"):
                return f"{greeting}, {name}"
        
        obj = MyClass(True)
        assert obj.greet("Alice") == "Hello, Alice"
        assert obj.greet("Bob", greeting="Hi") == "Hi, Bob"