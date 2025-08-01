package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
)

type BenchmarkResult struct {
	Language           string  `json:"language"`
	FileSizeMB         int     `json:"file_size_mb"`
	ReadTime           float64 `json:"read_time"`
	WriteTime          float64 `json:"write_time"`
	ReadThroughputMBS  float64 `json:"read_throughput_mbs"`
	WriteThroughputMBS float64 `json:"write_throughput_mbs"`
}

func benchmarkIO(fileSizeMB int) (*BenchmarkResult, error) {
	inputPath := fmt.Sprintf("../data/test_%dmb.txt", fileSizeMB)
	outputPath := fmt.Sprintf("../data/test_%dmb.go.out", fileSizeMB)

	// Check if input file exists
	if _, err := os.Stat(inputPath); os.IsNotExist(err) {
		return nil, fmt.Errorf("test file %s not found", inputPath)
	}

	// Write test (copy file)
	startTime := time.Now()
	fin, err := os.Open(inputPath)
	if err != nil {
		return nil, err
	}
	defer fin.Close()

	fout, err := os.Create(outputPath)
	if err != nil {
		return nil, err
	}
	defer fout.Close()

	buf := make([]byte, 8192)
	for {
		n, err := fin.Read(buf)
		if err != nil && err != io.EOF {
			return nil, err
		}
		if n == 0 {
			break
		}
		if _, err := fout.Write(buf[:n]); err != nil {
			return nil, err
		}
	}
	writeTime := time.Since(startTime).Seconds()

	// Read test
	startTime = time.Now()
	f, err := os.Open(outputPath)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	for {
		n, err := f.Read(buf)
		if err != nil && err != io.EOF {
			return nil, err
		}
		if n == 0 {
			break
		}
	}
	readTime := time.Since(startTime).Seconds()

	// Clean up output file
	os.Remove(outputPath)

	return &BenchmarkResult{
		Language:           "golang",
		FileSizeMB:         fileSizeMB,
		ReadTime:           readTime,
		WriteTime:          writeTime,
		ReadThroughputMBS:  float64(fileSizeMB) / readTime,
		WriteThroughputMBS: float64(fileSizeMB) / writeTime,
	}, nil
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "Usage: %s <file_size_mb>\n", os.Args[0])
		os.Exit(1)
	}

	fileSizeMB, err := strconv.Atoi(os.Args[1])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Invalid file size: %v\n", err)
		os.Exit(1)
	}

	result, err := benchmarkIO(fileSizeMB)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Benchmark failed: %v\n", err)
		os.Exit(1)
	}

	jsonOutput, err := json.Marshal(result)
	if err != nil {
		fmt.Fprintf(os.Stderr, "JSON encoding failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Println(string(jsonOutput))
}
