# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-29

### Added
- Initial release of I/O Performance Comparison suite
- Python implementation with 8KB buffer I/O
- Go implementation with efficient byte slice handling
- Kotlin implementation with automatic resource management
- Comprehensive benchmark runner with statistical analysis
- Multiple file size testing (1MB, 10MB, 50MB, 100MB)
- Performance visualization with matplotlib
- CSV and JSON result export
- Cross-platform support (macOS, Linux, Windows)
- Automated build system with Makefile
- Virtual environment support for Python dependencies
- Quick test verification script
- Comprehensive documentation

### Features
- Multi-iteration benchmarking for statistical accuracy
- Throughput calculations (MB/s)
- Performance ratio comparisons
- Error handling and graceful failure recovery
- Clean temporary file management
- Detailed logging and progress reporting

### Technical Details
- Python: Context managers, binary I/O, JSON serialization
- Go: Structured error handling, custom JSON marshaling
- Kotlin: Resource management with `use{}`, Gson integration
- Visualization: Multiple chart types, statistical summaries
- Build: Gradle for Kotlin, Go modules, Python virtual environments