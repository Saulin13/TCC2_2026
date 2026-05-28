import pytest
from sklearn.utils._available_if import available_if


class TestAvailableIf:
    def test_method_available_when_check_returns_true(self):
        class MyClass:
            def __init__(self, enabled):
                self.enabled = enabled
            
            def _is_enabled(self):
                return self.enabled
            
            @available_if(_is_enabled)
            def my_method(self):
                return "method called"
        
        obj = MyClass(enabled=True)
        assert hasattr(obj, "my_method")
        assert obj.my_method() == "method called"
    
    def test_method_unavailable_when_check_returns_false(self):
        class MyClass:
            def __init__(self, enabled):
                self.enabled = enabled
            
            def _is_enabled(self):
                return self.enabled
            
            @available_if(_is_enabled)
            def my_method(self):
                return "method called"
        
        obj = MyClass(enabled=False)
        assert not hasattr(obj, "my_method")
    
    def test_method_unavailable_when_check_raises_attribute_error(self):
        class MyClass:
            def __init__(self, has_attr):
                if has_attr:
                    self.required_attr = True
            
            def _check_attr(self):
                if not hasattr(self, "required_attr"):
                    raise AttributeError("required_attr not found")
                return True
            
            @available_if(_check_attr)
            def my_method(self):
                return "method called"
        
        obj = MyClass(has_attr=False)
        assert not hasattr(obj, "my_method")
    
    def test_method_becomes_available_after_state_change(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _is_even(self):
                return self.value % 2 == 0
            
            @available_if(_is_even)
            def even_method(self):
                return "even"
        
        obj = MyClass(value=1)
        assert not hasattr(obj, "even_method")
        
        obj.value = 2
        assert hasattr(obj, "even_method")
        assert obj.even_method() == "even"
    
    def test_accessing_unavailable_method_raises_attribute_error(self):
        class MyClass:
            def __init__(self, enabled):
                self.enabled = enabled
            
            def _is_enabled(self):
                return self.enabled
            
            @available_if(_is_enabled)
            def my_method(self):
                return "method called"
        
        obj = MyClass(enabled=False)
        with pytest.raises(AttributeError):
            obj.my_method()
    
    def test_multiple_methods_with_different_checks(self):
        class MyClass:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            
            def _x_positive(self):
                return self.x > 0
            
            def _y_positive(self):
                return self.y > 0
            
            @available_if(_x_positive)
            def method_x(self):
                return "x method"
            
            @available_if(_y_positive)
            def method_y(self):
                return "y method"
        
        obj = MyClass(x=1, y=-1)
        assert hasattr(obj, "method_x")
        assert not hasattr(obj, "method_y")
        assert obj.method_x() == "x method"
    
    def test_check_with_none_return_value(self):
        class MyClass:
            def _returns_none(self):
                return None
            
            @available_if(_returns_none)
            def my_method(self):
                return "method called"
        
        obj = MyClass()
        assert not hasattr(obj, "my_method")
    
    def test_check_with_truthy_non_boolean_value(self):
        class MyClass:
            def __init__(self, count):
                self.count = count
            
            def _get_count(self):
                return self.count
            
            @available_if(_get_count)
            def my_method(self):
                return "method called"
        
        obj_zero = MyClass(count=0)
        assert not hasattr(obj_zero, "my_method")
        
        obj_positive = MyClass(count=5)
        assert hasattr(obj_positive, "my_method")
        assert obj_positive.my_method() == "method called"
    
    def test_decorated_method_with_arguments(self):
        class MyClass:
            def __init__(self, enabled):
                self.enabled = enabled
            
            def _is_enabled(self):
                return self.enabled
            
            @available_if(_is_enabled)
            def my_method(self, arg1, arg2):
                return arg1 + arg2
        
        obj = MyClass(enabled=True)
        assert obj.my_method(10, 20) == 30
    
    def test_decorated_method_with_kwargs(self):
        class MyClass:
            def __init__(self, enabled):
                self.enabled = enabled
            
            def _is_enabled(self):
                return self.enabled
            
            @available_if(_is_enabled)
            def my_method(self, x=1, y=2):
                return x * y
        
        obj = MyClass(enabled=True)
        assert obj.my_method(x=3, y=4) == 12
    
    def test_check_function_receives_correct_instance(self):
        class MyClass:
            def __init__(self, value):
                self.value = value
            
            def _check_value(self):
                assert isinstance(self, MyClass)
                return self.value == 42
            
            @available_if(_check_value)
            def my_method(self):
                return "correct"
        
        obj = MyClass(value=42)
        assert hasattr(obj, "my_method")
        assert obj.my_method() == "correct"