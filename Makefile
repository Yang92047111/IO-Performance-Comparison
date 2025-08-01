.PHONY: all setup benchmark run-python run-go run-kotlin test-kotlin clean clean-all install-deps

all: setup benchmark

setup: install-deps
	@echo "Setting up benchmark environment..."
	@mkdir -p data results

install-deps:
	@echo "Setting up Python virtual environment..."
	@python3 -m venv venv
	@echo "Installing Python dependencies..."
	@./venv/bin/pip install -r requirements.txt
	@echo "Building Go module..."
	@cd golang && go mod tidy
	@echo "Building Kotlin project..."
	@cd kotlin && (./gradlew build -x test || gradle build -x test)

benchmark: setup
	@echo "\n=== Running I/O Performance Benchmark ==="
	@./venv/bin/python benchmark_runner.py

run-python:
	@echo "\n--- Running Python Test ---"
	@echo "Creating 10MB test file..."
	@mkdir -p data
	@python3 -c "with open('data/test_10mb.txt', 'wb') as f: f.write(b'A' * (10 * 1024 * 1024))"
	@python3 python/io_benchmark.py 10

run-go:
	@echo "\n--- Running Golang Test ---"
	@echo "Creating 10MB test file..."
	@mkdir -p data
	@python3 -c "with open('data/test_10mb.txt', 'wb') as f: f.write(b'A' * (10 * 1024 * 1024))"
	@cd golang && go run main.go 10

run-kotlin:
	@echo "\n--- Running Kotlin Test ---"
	@echo "Creating 10MB test file..."
	@mkdir -p data
	@python3 -c "with open('data/test_10mb.txt', 'wb') as f: f.write(b'A' * (10 * 1024 * 1024))"
	@cd kotlin && (./gradlew run --args="10" --quiet || gradle run --args="10" --quiet)

test-individual: setup
	@echo "\n=== Testing Individual Implementations ==="
	@echo "Creating 10MB test file..."
	@./venv/bin/python -c "with open('data/test_10mb.txt', 'wb') as f: f.write(b'A' * (10 * 1024 * 1024))"
	@make run-python
	@make run-go  
	@make run-kotlin

clean:
	@echo "Cleaning up generated files..."
	@rm -f golang/io_benchmark
	@rm -f data/*.out
	@rm -f data/test_*.txt
	@rm -rf results/
	@cd kotlin && (./gradlew clean || gradle clean)

test-kotlin:
	@echo "\n--- Running Kotlin Tests ---"
	@cd kotlin && (./gradlew test || gradle test)

clean-all: clean
	@echo "Removing virtual environment..."
	@rm -rf venv/