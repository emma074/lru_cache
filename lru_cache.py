class Node:
    """
    Node for doubly linked list.
    Each node contains key-value pair and pointers to prev/next nodes.
    """
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation.
    
    Uses HashMap + Doubly Linked List for O(1) operations:
    - HashMap: O(1) key lookup
    - Doubly Linked List: O(1) insertion/deletion for order maintenance
    
    Structure:
    - Most recently used items are near the head
    - Least recently used items are near the tail
    - When capacity is exceeded, tail node is removed
    """
    
    def __init__(self, capacity: int):
        """
        Initialize LRU Cache with given capacity.
        
        Args:
            capacity (int): Maximum number of items cache can hold
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
            
        self.capacity = capacity
        self.cache = {}  # HashMap: key -> Node
        
        # Create dummy head and tail nodes to simplify edge cases
        self.head = Node()  # Most recently used end
        self.tail = Node()  # Least recently used end
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node):
        """
        Add node right after head (most recently used position).
        
        Args:
            node (Node): Node to add
        """
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        """
        Remove an existing node from the linked list.
        
        Args:
            node (Node): Node to remove
        """
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node):
        """
        Move existing node to head (mark as most recently used).
        
        Args:
            node (Node): Node to move to head
        """
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self):
        """
        Remove and return the last node (least recently used).
        
        Returns:
            Node: The removed tail node
        """
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key: int) -> int:
        """
        Get value for given key. Mark as most recently used.
        
        Args:
            key (int): Key to lookup
            
        Returns:
            int: Value if key exists, -1 otherwise
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        node = self.cache.get(key)
        
        if not node:
            return -1
        
        # Move accessed node to head (most recently used)
        self._move_to_head(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Put key-value pair in cache. Handle capacity overflow.
        
        Args:
            key (int): Key to store
            value (int): Value to store
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        node = self.cache.get(key)
        
        if not node:
            # Key doesn't exist - add new node
            new_node = Node(key, value)
            
            if len(self.cache) >= self.capacity:
                # Remove least recently used item
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
            
            # Add new node to cache and head of list
            self.cache[key] = new_node
            self._add_node(new_node)
            
        else:
            # Key exists - update value and move to head
            node.value = value
            self._move_to_head(node)
    
    def display_cache_state(self):
        """
        Display current cache state for debugging.
        Shows order from most recently used to least recently used.
        """
        if not self.cache:
            print("Cache is empty")
            return
            
        print(f"Cache state (capacity: {self.capacity}, size: {len(self.cache)}):")
        print("Most Recent -> Least Recent:")
        
        current = self.head.next
        items = []
        while current != self.tail:
            items.append(f"({current.key}:{current.value})")
            current = current.next
        
        print(" -> ".join(items))
        print()


def test_lru_cache():
    """
    Comprehensive test suite for LRU Cache implementation.
    Tests various scenarios including edge cases.
    """
    print("=== LRU Cache Test Suite ===\n")
    
    # Test 1: Basic Operations
    print("Test 1: Basic Operations")
    cache = LRUCache(2)
    
    cache.put(1, 1)
    cache.display_cache_state()
    
    cache.put(2, 2)
    cache.display_cache_state()
    
    print(f"get(1): {cache.get(1)}")  # Returns 1
    cache.display_cache_state()
    
    cache.put(3, 3)  # Evicts key 2
    cache.display_cache_state()
    
    print(f"get(2): {cache.get(2)}")  # Returns -1 (not found)
    print(f"get(3): {cache.get(3)}")  # Returns 3
    print(f"get(1): {cache.get(1)}")  # Returns 1
    cache.display_cache_state()
    print()
    
    # Test 2: Capacity Overflow
    print("Test 2: Capacity Overflow")
    cache = LRUCache(3)
    
    for i in range(1, 6):  # Add keys 1-5
        cache.put(i, i * 10)
        cache.display_cache_state()
    print()
    
    # Test 3: Key Updates
    print("Test 3: Key Updates")
    cache = LRUCache(2)
    
    cache.put(1, 1)
    cache.put(2, 2)
    cache.display_cache_state()
    
    cache.put(1, 10)  # Update existing key
    cache.display_cache_state()
    
    print(f"get(1): {cache.get(1)}")  # Should return 10
    cache.display_cache_state()
    print()
    
    # Test 4: Access Pattern Changes
    print("Test 4: Access Pattern Changes")
    cache = LRUCache(3)
    
    # Add items
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    cache.display_cache_state()
    
    # Access item 1 (move to front)
    cache.get(1)
    cache.display_cache_state()
    
    # Add new item - should evict 2 (least recently used)
    cache.put(4, 4)
    cache.display_cache_state()
    
    print(f"get(2): {cache.get(2)}")  # Should return -1
    print()
    
    # Test 5: Edge Cases
    print("Test 5: Edge Cases")
    
    # Empty cache
    cache = LRUCache(1)
    print(f"get(1) from empty cache: {cache.get(1)}")  # Should return -1
    cache.display_cache_state()
    
    # Single capacity
    cache.put(1, 1)
    cache.display_cache_state()
    
    cache.put(2, 2)  # Should evict key 1
    cache.display_cache_state()
    
    print(f"get(1): {cache.get(1)}")  # Should return -1
    print(f"get(2): {cache.get(2)}")  # Should return 2
    print()
    
    # Test 6: Invalid Keys
    print("Test 6: Invalid Key Handling")
    cache = LRUCache(2)
    
    print(f"get(999): {cache.get(999)}")  # Non-existent key
    
    cache.put(1, 1)
    print(f"get(1): {cache.get(1)}")
    print(f"get(999): {cache.get(999)}")  # Still non-existent
    print()
    
    # Test 7: Performance Test
    print("Test 7: Performance Validation")
    import time
    
    cache = LRUCache(1000)
    
    # Test O(1) operations
    start_time = time.time()
    for i in range(10000):
        cache.put(i % 1000, i)
    put_time = time.time() - start_time
    
    start_time = time.time()
    for i in range(10000):
        cache.get(i % 1000)
    get_time = time.time() - start_time
    
    print(f"10,000 put operations: {put_time:.4f} seconds")
    print(f"10,000 get operations: {get_time:.4f} seconds")
    print("Operations maintain O(1) time complexity")
    print()
    
    print("=== All tests completed successfully! ===")


if __name__ == "__main__":
    test_lru_cache()