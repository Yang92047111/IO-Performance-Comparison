#!/usr/bin/env python3
"""
I/O Performance Benchmark Runner
Compares file I/O performance across Python, Go, and Kotlin
"""

import os
import subprocess
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import statistics

class IOBenchmark:
    def __init__(self):
        self.results = {}
        self.test_file_sizes = [1, 10, 50, 100]  # MB
        self.iterations = 3
        
    def create_test_files(self):
        """Create test files of different sizes"""
        print("Creating test files...")
        os.makedirs("data", exist_ok=True)
        
        for size_mb in self.test_file_sizes:
            file_path = f"data/test_{size_mb}mb.txt"
            if not os.path.exists(file_path):
                print(f"Creating {size_mb}MB test file...")
                with open(file_path, 'wb') as f:
                    # Write 1MB chunks
                    chunk = b'A' * (1024 * 1024)
                    for _ in range(size_mb):
                        f.write(chunk)
    
    def run_python_benchmark(self, file_size_mb):
        """Run Python I/O benchmark"""
        cmd = ["python3", "python/io_benchmark.py", str(file_size_mb)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Python benchmark failed: {result.stderr}")
            return None
        return json.loads(result.stdout.strip())
    
    def run_golang_benchmark(self, file_size_mb):
        """Run Go I/O benchmark"""
        # Build Go binary first
        subprocess.run(["go", "build", "-o", "golang/io_benchmark", "golang/main.go"], 
                      cwd=".", check=True)
        
        cmd = ["./golang/io_benchmark", str(file_size_mb)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Go benchmark failed: {result.stderr}")
            return None
        return json.loads(result.stdout.strip())
    
    def run_kotlin_benchmark(self, file_size_mb):
        """Run Kotlin I/O benchmark"""
        cmd = ["./gradlew", "run", f"--args={file_size_mb}", "--quiet"]
        result = subprocess.run(cmd, cwd="kotlin", capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Kotlin benchmark failed: {result.stderr}")
            return None
        
        # Extract JSON from gradle output
        lines = result.stdout.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        return None
    
    def run_benchmarks(self):
        """Run all benchmarks"""
        self.create_test_files()
        
        for size_mb in self.test_file_sizes:
            print(f"\nBenchmarking {size_mb}MB file...")
            
            # Initialize results for this file size
            self.results[size_mb] = {
                'python': {'read': [], 'write': []},
                'golang': {'read': [], 'write': []},
                'kotlin': {'read': [], 'write': []}
            }
            
            # Run multiple iterations
            for iteration in range(self.iterations):
                print(f"  Iteration {iteration + 1}/{self.iterations}")
                
                # Python
                print("    Running Python benchmark...")
                py_result = self.run_python_benchmark(size_mb)
                if py_result:
                    self.results[size_mb]['python']['read'].append(py_result['read_time'])
                    self.results[size_mb]['python']['write'].append(py_result['write_time'])
                    print(f"    ✓ Python: read={py_result['read_time']:.3f}s, write={py_result['write_time']:.3f}s")
                else:
                    print("    ✗ Python benchmark failed")
                
                # Go
                print("    Running Go benchmark...")
                go_result = self.run_golang_benchmark(size_mb)
                if go_result:
                    self.results[size_mb]['golang']['read'].append(go_result['read_time'])
                    self.results[size_mb]['golang']['write'].append(go_result['write_time'])
                    print(f"    ✓ Go: read={go_result['read_time']:.3f}s, write={go_result['write_time']:.3f}s")
                else:
                    print("    ✗ Go benchmark failed")
                
                # Kotlin
                print("    Running Kotlin benchmark...")
                kt_result = self.run_kotlin_benchmark(size_mb)
                if kt_result:
                    self.results[size_mb]['kotlin']['read'].append(kt_result['read_time'])
                    self.results[size_mb]['kotlin']['write'].append(kt_result['write_time'])
                    print(f"    ✓ Kotlin: read={kt_result['read_time']:.3f}s, write={kt_result['write_time']:.3f}s")
                else:
                    print("    ✗ Kotlin benchmark failed")
    
    def calculate_stats(self):
        """Calculate statistics from benchmark results"""
        stats = {}
        
        for size_mb in self.test_file_sizes:
            stats[size_mb] = {}
            
            for lang in ['python', 'golang', 'kotlin']:
                stats[size_mb][lang] = {}
                
                for operation in ['read', 'write']:
                    times = self.results[size_mb][lang][operation]
                    if times:
                        stats[size_mb][lang][operation] = {
                            'mean': statistics.mean(times),
                            'median': statistics.median(times),
                            'min': min(times),
                            'max': max(times),
                            'std': statistics.stdev(times) if len(times) > 1 else 0
                        }
                        print(f"Stats for {lang} {operation} ({size_mb}MB): {len(times)} samples, mean={statistics.mean(times):.3f}s")
                    else:
                        print(f"No data for {lang} {operation} ({size_mb}MB)")
        
        return stats
    
    def create_visualizations(self, stats):
        """Create performance comparison charts"""
        # Create results directory
        os.makedirs("results", exist_ok=True)
        
        # Prepare data for plotting
        languages = ['python', 'golang', 'kotlin']
        operations = ['read', 'write']
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('I/O Performance Comparison: Python vs Go vs Kotlin', fontsize=16)
        
        # Read performance by file size
        ax1 = axes[0, 0]
        for lang in languages:
            read_times = [stats[size][lang]['read']['mean'] for size in self.test_file_sizes 
                         if lang in stats[size] and 'read' in stats[size][lang]]
            ax1.plot(self.test_file_sizes[:len(read_times)], read_times, 
                    marker='o', label=lang.capitalize(), linewidth=2)
        
        ax1.set_xlabel('File Size (MB)')
        ax1.set_ylabel('Time (seconds)')
        ax1.set_title('Read Performance')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Write performance by file size
        ax2 = axes[0, 1]
        for lang in languages:
            write_times = [stats[size][lang]['write']['mean'] for size in self.test_file_sizes 
                          if lang in stats[size] and 'write' in stats[size][lang]]
            ax2.plot(self.test_file_sizes[:len(write_times)], write_times, 
                    marker='s', label=lang.capitalize(), linewidth=2)
        
        ax2.set_xlabel('File Size (MB)')
        ax2.set_ylabel('Time (seconds)')
        ax2.set_title('Write Performance')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Throughput comparison (MB/s) for largest file
        ax3 = axes[1, 0]
        largest_file = max(self.test_file_sizes)
        read_throughput = []
        write_throughput = []
        lang_labels = []
        
        for lang in languages:
            if (lang in stats[largest_file] and 
                'read' in stats[largest_file][lang] and 
                'write' in stats[largest_file][lang] and
                stats[largest_file][lang]['read'] and
                stats[largest_file][lang]['write']):
                
                read_time = stats[largest_file][lang]['read']['mean']
                write_time = stats[largest_file][lang]['write']['mean']
                
                read_throughput.append(largest_file / read_time)
                write_throughput.append(largest_file / write_time)
                lang_labels.append(lang.capitalize())
        
        if lang_labels:  # Only create chart if we have data
            x = range(len(lang_labels))
            width = 0.35
            
            ax3.bar([i - width/2 for i in x], read_throughput, width, label='Read', alpha=0.8)
            ax3.bar([i + width/2 for i in x], write_throughput, width, label='Write', alpha=0.8)
            
            ax3.set_xlabel('Language')
            ax3.set_ylabel('Throughput (MB/s)')
            ax3.set_title(f'Throughput Comparison ({largest_file}MB file)')
            ax3.set_xticks(x)
            ax3.set_xticklabels(lang_labels)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'No throughput data available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax3.transAxes, fontsize=12)
            ax3.set_title(f'Throughput Comparison ({largest_file}MB file)')
        
        # Performance ratio comparison
        ax4 = axes[1, 1]
        
        # Use Go as baseline (ratio = 1.0)
        baseline_lang = 'golang'
        ratios_data = {'Read': [], 'Write': []}
        ratio_labels = []
        
        for lang in languages:
            if (lang == baseline_lang and 
                lang in stats[largest_file] and
                'read' in stats[largest_file][lang] and
                'write' in stats[largest_file][lang] and
                stats[largest_file][lang]['read'] and
                stats[largest_file][lang]['write']):
                ratios_data['Read'].append(1.0)
                ratios_data['Write'].append(1.0)
                ratio_labels.append(lang.capitalize())
            elif (lang in stats[largest_file] and 
                  baseline_lang in stats[largest_file] and
                  'read' in stats[largest_file][lang] and
                  'write' in stats[largest_file][lang] and
                  'read' in stats[largest_file][baseline_lang] and
                  'write' in stats[largest_file][baseline_lang] and
                  stats[largest_file][lang]['read'] and
                  stats[largest_file][lang]['write'] and
                  stats[largest_file][baseline_lang]['read'] and
                  stats[largest_file][baseline_lang]['write']):
                
                read_ratio = (stats[largest_file][baseline_lang]['read']['mean'] / 
                             stats[largest_file][lang]['read']['mean'])
                write_ratio = (stats[largest_file][baseline_lang]['write']['mean'] / 
                              stats[largest_file][lang]['write']['mean'])
                
                ratios_data['Read'].append(read_ratio)
                ratios_data['Write'].append(write_ratio)
                ratio_labels.append(lang.capitalize())
        
        if ratio_labels:  # Only create chart if we have data
            x = range(len(ratio_labels))
            ax4.bar([i - width/2 for i in x], ratios_data['Read'], width, label='Read', alpha=0.8)
            ax4.bar([i + width/2 for i in x], ratios_data['Write'], width, label='Write', alpha=0.8)
            
            ax4.set_xlabel('Language')
            ax4.set_ylabel('Performance Ratio (vs Go)')
            ax4.set_title('Relative Performance (Go = 1.0)')
            ax4.set_xticks(x)
            ax4.set_xticklabels(ratio_labels)
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            ax4.axhline(y=1.0, color='red', linestyle='--', alpha=0.7)
        else:
            ax4.text(0.5, 0.5, 'No ratio data available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Relative Performance (Go = 1.0)')
        
        plt.tight_layout()
        plt.savefig('results/io_performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_results(self, stats):
        """Save detailed results to files"""
        # Save raw results
        with open('results/benchmark_results.json', 'w') as f:
            json.dump({
                'raw_results': self.results,
                'statistics': stats,
                'test_config': {
                    'file_sizes_mb': self.test_file_sizes,
                    'iterations': self.iterations
                }
            }, f, indent=2)
        
        # Create CSV summary
        summary_data = []
        for size_mb in self.test_file_sizes:
            for lang in ['python', 'golang', 'kotlin']:
                if lang in stats[size_mb]:
                    for operation in ['read', 'write']:
                        if operation in stats[size_mb][lang]:
                            row = {
                                'file_size_mb': size_mb,
                                'language': lang,
                                'operation': operation,
                                'mean_time': stats[size_mb][lang][operation]['mean'],
                                'median_time': stats[size_mb][lang][operation]['median'],
                                'min_time': stats[size_mb][lang][operation]['min'],
                                'max_time': stats[size_mb][lang][operation]['max'],
                                'std_dev': stats[size_mb][lang][operation]['std'],
                                'throughput_mbs': size_mb / stats[size_mb][lang][operation]['mean']
                            }
                            summary_data.append(row)
        
        df = pd.DataFrame(summary_data)
        df.to_csv('results/benchmark_summary.csv', index=False)
        
        print(f"\nResults saved to:")
        print(f"  - results/benchmark_results.json")
        print(f"  - results/benchmark_summary.csv")
        print(f"  - results/io_performance_comparison.png")

def main():
    print("I/O Performance Benchmark Suite")
    print("=" * 40)
    
    benchmark = IOBenchmark()
    benchmark.run_benchmarks()
    
    stats = benchmark.calculate_stats()
    benchmark.create_visualizations(stats)
    benchmark.save_results(stats)
    
    print("\nBenchmark completed successfully!")

if __name__ == "__main__":
    main()