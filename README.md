# 🧠 LRU Cache in Python

This project implements a Least Recently Used (LRU) Cache in Python using a combination of a hash map and a doubly linked list to ensure O(1) time complexity for both get and put operations.

---

## 📌 Features

- Efficient O(1) cache operations
- Evicts least recently used items on capacity overflow
- Includes:
  - Detailed class documentation
  - Debug-friendly cache state display
  - Comprehensive test suite for all common and edge cases

---

## 📁 Structure

- Node: A node class representing each key-value pair in a doubly linked list.
- LRUCache: Cache class implementing the LRU logic.
- test_lru_cache(): Function to run tests on the LRU cache.
- display_cache_state(): Visualize the current order of items in the cache (from most to least recently used).
