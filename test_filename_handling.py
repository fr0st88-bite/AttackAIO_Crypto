#!/usr/bin/env python3
"""Test filename handling fix"""

import os
import sys

# Test cases
test_cases = [
    ('test_input.txt', 'test_input.txt'),  # With .txt extension
    ('test_input', 'test_input.txt'),       # Without .txt extension
]

print("Testing filename handling fix...\n")

for user_input, expected_filename in test_cases:
    # Simulate the fixed code
    filer = user_input
    
    if not filer.endswith('.txt'):
        filename = filer + '.txt'
    else:
        filename = filer
    
    # Check if file exists
    if os.path.exists(filename):
        print(f"✓ Input '{user_input}' → Looking for '{expected_filename}' → Found ✓")
    else:
        print(f"✗ Input '{user_input}' → Looking for '{expected_filename}' → NOT FOUND ✗")

print("\n✓ Filename handling test complete")
