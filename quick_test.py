#!/usr/bin/env python3
"""
Quick test to see which benchmark implementations work
"""

import os
import subprocess
import json

def test_implementation(name, cmd, cwd=None):
    print(f"Testing {name}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=30)
        if result.returncode == 0:
            # Try to parse JSON output
            try:
                data = json.loads(result.stdout.strip())
                print(f"  ✓ {name} works: {data}")
                return True
            except json.JSONDecodeError:
                print(f"  ⚠ {name} runs but output not JSON: {result.stdout[:100]}")
                return False
        else:
            print(f"  ✗ {name} failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ {name} timed out")
        return False
    except Exception as e:
        print(f"  ✗ {name} error: {e}")
        return False

def main():
    # Create test file
    os.makedirs('data', exist_ok=True)
    test_file = 'data/test_1mb.txt'
    if not os.path.exists(test_file):
        print("Creating 1MB test file...")
        with open(test_file, 'wb') as f:
            f.write(b'A' * (1024 * 1024))
    
    print("Testing individual benchmark implementations:")
    print("=" * 50)
    
    # Test Python
    python_cmd = './venv/bin/python' if os.path.exists('./venv/bin/python') else 'python3'
    test_implementation("Python", [python_cmd, 'python/io_benchmark.py', '1'])
    
    # Test Go
    test_implementation("Go", ['go', 'run', 'golang/main.go', '1'])
    
    # Test Kotlin
    test_implementation("Kotlin", ['./gradlew', 'run', '--args=1', '--quiet'], cwd='kotlin')

if __name__ == "__main__":
    main()