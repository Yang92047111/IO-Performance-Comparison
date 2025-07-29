# 🚀 I/O Performance Comparison: Python vs Go vs Kotlin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Go](https://img.shields.io/badge/Go-1.19+-00ADD8.svg)](https://golang.org/dl/)
[![Kotlin](https://img.shields.io/badge/Kotlin-JVM-7F52FF.svg)](https://kotlinlang.org/)

A comprehensive benchmarking suite that compares file I/O performance across Python, Go, and Kotlin implementations. This project provides detailed performance analysis with statistical rigor and beautiful visualizations.

## ✨ Features

- 🔄 **Multi-language benchmarking**: Tests Python, Go, and Kotlin I/O performance
- 📊 **Multiple file sizes**: Tests with 1MB, 10MB, 50MB, and 100MB files
- 📈 **Statistical analysis**: Multiple iterations with mean, median, min, max, and standard deviation
- 📉 **Visual comparisons**: Generates performance charts and graphs
- ⚡ **Throughput metrics**: Measures MB/s for read and write operations
- 🤖 **Automated execution**: Single command runs all benchmarks
- 🔧 **Cross-platform**: Works on macOS, Linux, and Windows

## 📁 Project Structure

```
├── benchmark_runner.py      # 🎯 Main benchmark orchestrator
├── quick_test.py            # 🧪 Quick implementation tester
├── test_setup.py           # ⚙️ Setup verification script
├── python/
│   ├── io_benchmark.py     # 🐍 Python I/O implementation
│   └── io_test.py          # 🐍 Python test runner
├── golang/
│   ├── main.go             # 🐹 Go I/O implementation
│   └── go.mod              # 🐹 Go module definition
├── kotlin/
│   └── app/
│       └── src/main/kotlin/org/example/
│           └── App.kt      # 🎯 Kotlin I/O implementation
├── data/                   # 📂 Test files (auto-generated)
├── results/                # 📊 Benchmark results (auto-generated)
├── Makefile               # 🔨 Build and run commands
├── requirements.txt       # 📦 Python dependencies
└── .gitignore             # 🚫 Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- 🐍 **Python 3.7+**
- 🐹 **Go 1.19+**
- ☕ **Java 11+** (for Kotlin)
- 🔨 **Make** (build automation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/io-performance-comparison.git
   cd io-performance-comparison
   ```

2. **Install dependencies** (creates Python virtual environment automatically)
   ```bash
   make install-deps
   ```

> **💡 Note**: On macOS/Linux, this automatically creates a Python virtual environment to avoid conflicts with system Python packages.

### 🏃‍♂️ Running Benchmarks

**Run the complete benchmark suite:**
```bash
make benchmark
```

**Test individual implementations:**
```bash
make test-individual
```

**Quick verification test:**
```bash
python3 quick_test.py
```

**Run specific language tests:**
```bash
make run-python    # 🐍 Python only
make run-go        # 🐹 Go only
make run-kotlin    # Kotlin only
```

## Benchmark Details

### Test Operations

1. **Write Test**: Copy a test file using 8KB buffer chunks
2. **Read Test**: Read the copied file using 8KB buffer chunks

### File Sizes Tested

- 1 MB
- 10 MB
- 50 MB
- 100 MB

### Metrics Collected

- **Execution Time**: Time taken for read/write operations
- **Throughput**: MB/s for each operation
- **Statistical Analysis**: Mean, median, min, max, standard deviation
- **Relative Performance**: Performance ratios compared to Go baseline

### 📊 Sample Results

Here's what you can expect from the benchmark results:

| Language | File Size | Read (MB/s) | Write (MB/s) |
|----------|-----------|-------------|--------------|
| Go       | 100MB     | 3,856       | 815          |
| Kotlin   | 100MB     | 4,054       | 802          |
| Python   | 100MB     | 4,054       | 805          |

*Results may vary based on hardware and system configuration*

### 📁 Output Files

After running benchmarks, check the `results/` directory:

- 📄 `benchmark_results.json`: Raw benchmark data with all iterations
- 📊 `benchmark_summary.csv`: Tabulated results with statistics
- 📈 `io_performance_comparison.png`: Performance visualization charts

## 🔧 Implementation Details

### 🐍 Python Implementation
- Uses built-in `open()` with binary mode
- 8KB buffer size for chunked I/O
- Context managers for proper file handling
- JSON output for benchmark results

### 🐹 Go Implementation  
- Uses `os.Open()` and `os.Create()`
- 8KB byte slice buffer
- Proper error handling and resource cleanup
- Structured JSON output with custom types

### 🎯 Kotlin Implementation
- Uses `FileInputStream`/`FileOutputStream`
- 8KB ByteArray buffer
- Automatic resource management with `use{}`
- Gson for JSON serialization

## Performance Expectations

Typical performance characteristics:

- **Go**: Generally fastest, especially for large files
- **Kotlin**: Close to Go performance, benefits from JVM optimizations
- **Python**: Slower for pure I/O, but difference narrows with larger files

Results vary based on:

- Hardware (SSD vs HDD, CPU, RAM)
- Operating system
- File system type
- System load

## Customization

### Modify Test Parameters

Edit `benchmark_runner.py`:

```python
self.test_file_sizes = [1, 10, 50, 100]  # File sizes in MB
self.iterations = 3                       # Number of test runs
```

### Change Buffer Size

Update buffer size in each implementation:

- Python: `chunk = f_in.read(8192)`
- Go: `buf := make([]byte, 8192)`
- Kotlin: `val buffer = ByteArray(8192)`

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Run `make install-deps`
2. **Permission errors**: Ensure write access to project directory
3. **Out of disk space**: Large test files require sufficient free space
4. **Java/Kotlin build errors**: Verify Java 11+ is installed

### Clean Up

Remove generated files:

```bash
make clean
```

Remove everything including virtual environment:

```bash
make clean-all
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🍴 Fork the repository**
2. **🌿 Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **✨ Add your improvements**
   - New language implementations
   - Performance optimizations
   - Better visualizations
   - Bug fixes
4. **📝 Commit your changes** (`git commit -m 'Add amazing feature'`)
5. **🚀 Push to the branch** (`git push origin feature/amazing-feature`)
6. **🔄 Submit a pull request**

### Ideas for Contributions
- 🦀 **Rust implementation**
- 🔷 **C# implementation** 
- ☕ **Java implementation**
- 📊 **More visualization options**
- 🔧 **Different I/O patterns** (async, memory-mapped, etc.)
- 🧪 **Additional test scenarios**

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who help improve this benchmark suite
- Inspired by the need for fair, comprehensive I/O performance comparisons
- Built with ❤️ for the developer community

---

**⭐ If this project helped you, please give it a star!**
