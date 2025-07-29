
#!/usr/bin/env python3
"""
Python I/O Benchmark
Measures file read and write performance
"""

import time
import json
import sys
import os

def benchmark_io(file_size_mb):
    """Benchmark I/O operations for given file size"""
    input_file = f'data/test_{file_size_mb}mb.txt'
    output_file = f'data/test_{file_size_mb}mb.py.out'
    
    # Ensure input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Test file {input_file} not found")
    
    # Write test (copy file)
    start_time = time.time()
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(8192)
            if not chunk:
                break
            f_out.write(chunk)
    write_time = time.time() - start_time
    
    # Read test
    start_time = time.time()
    with open(output_file, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
    read_time = time.time() - start_time
    
    # Clean up output file
    os.remove(output_file)
    
    return {
        'language': 'python',
        'file_size_mb': file_size_mb,
        'read_time': read_time,
        'write_time': write_time,
        'read_throughput_mbs': file_size_mb / read_time,
        'write_throughput_mbs': file_size_mb / write_time
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 io_benchmark.py <file_size_mb>")
        sys.exit(1)
    
    file_size_mb = int(sys.argv[1])
    result = benchmark_io(file_size_mb)
    print(json.dumps(result))

if __name__ == "__main__":
    main()
