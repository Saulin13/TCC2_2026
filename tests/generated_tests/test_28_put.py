import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from other.lru_cache import put
import os
import sys




import pytest

class TestCache:
    def setup_method(self):
        # Setup a cache instance with a given capacity for testing
        self.cache = Cache(capacity=3)

    def test_put_new_key(self):
        # Test putting a new key-value pair
        self.cache.put('key1', 'value1')
        assert 'key1' in self.cache.cache
        assert self.cache.cache['key1'].val == 'value1'
        assert self.cache.num_keys == 1

    def test_put_existing_key(self):
        # Test updating an existing key-value pair
        self.cache.put('key1', 'value1')
        self.cache.put('key1', 'value2')
        assert 'key1' in self.cache.cache
        assert self.cache.cache['key1'].val == 'value2'
        assert self.cache.num_keys == 1

    def test_put_over_capacity(self):
        # Test putting key-value pairs over the cache capacity
        self.cache.put('key1', 'value1')
        self.cache.put('key2', 'value2')
        self.cache.put('key3', 'value3')
        self.cache.put('key4', 'value4')  # This should evict 'key1'

        assert 'key1' not in self.cache.cache
        assert 'key2' in self.cache.cache
        assert 'key3' in self.cache.cache
        assert 'key4' in self.cache.cache
        assert self.cache.num_keys == 3

    def test_put_eviction_order(self):
        # Test the eviction order is correct
        self.cache.put('key1', 'value1')
        self.cache.put('key2', 'value2')
        self.cache.put('key3', 'value3')
        self.cache.put('key2', 'value2_updated')  # Update key2, should be most recent
        self.cache.put('key4', 'value4')  # This should evict 'key1'

        assert 'key1' not in self.cache.cache
        assert 'key2' in self.cache.cache
        assert self.cache.cache['key2'].val == 'value2_updated'
        assert 'key3' in self.cache.cache
        assert 'key4' in self.cache.cache
        assert self.cache.num_keys == 3


Note: This test assumes the existence of a `Cache` class with a `capacity` parameter and a `DoubleLinkedListNode` class. Adjust the setup and class names according to your actual implementation.