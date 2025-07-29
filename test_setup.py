#!/usr/bin/env python3
"""
Quick test script to verify all implementations work
"""

import os
import subprocess
import sys

def test_python():
    print("Testing Python implementation...")
    # Create a small test file
    with open('data/test_1mb.txt', 'wb') as f:
        f.write(b'A' * (1024 * 1024))
    
    python_cmd = './venv/bin/python' if os.path.exists('./venv/bin/python') else 'python3'
    result = subprocess.run([python_cmd, 'python/io_benchmark.py', '1'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Python test passed")
        return True
    else:
        print(f"✗ Python test failed: {result.stderr}")
        return False

def test_golang():
    print("Testing Go implementation...")
    result = subprocess.run(['go', 'run', 'golang/main.go', '1'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Go test passed")
        return True
    else:
        print(f"✗ Go test failed: {result.stderr}")
        return False

def test_kotlin():
    print("Testing Kotlin implementation...")
    result = subprocess.run(['./gradlew', 'run', '--args=1', '--quiet'], 
                          cwd='kotlin', capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Kotlin test passed")
        return True
    else:
        print(f"✗ Kotlin test failed: {result.stderr}")
        return False

def main():
    print("I/O Benchmark Setup Test")
    print("=" * 30)
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    tests = [test_python, test_golang, test_kotlin]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Ready to run benchmarks.")
        return 0
    else:
        print("❌ Some tests failed. Check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())