
import com.google.gson.Gson
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import kotlin.system.measureTimeMillis

data class BenchmarkResult(
    val language: String,
    val file_size_mb: Int,
    val read_time: Double,
    val write_time: Double,
    val read_throughput_mbs: Double,
    val write_throughput_mbs: Double
)

fun benchmarkIO(fileSizeMB: Int): BenchmarkResult {
    val inputPath = "../../data/test_${fileSizeMB}mb.txt"
    val outputPath = "../../data/test_${fileSizeMB}mb.kt.out"
    
    // Check if input file exists
    if (!File(inputPath).exists()) {
        throw IllegalArgumentException("Test file $inputPath not found")
    }

    // Write test (copy file)
    val writeTime = measureTimeMillis {
        FileInputStream(inputPath).use { fin ->
            FileOutputStream(outputPath).use { fout ->
                val buffer = ByteArray(8192)
                var length: Int
                while (fin.read(buffer).also { length = it } > 0) {
                    fout.write(buffer, 0, length)
                }
            }
        }
    } / 1000.0

    // Read test
    val readTime = measureTimeMillis {
        FileInputStream(outputPath).use { fin ->
            val buffer = ByteArray(8192)
            while (fin.read(buffer) != -1) {}
        }
    } / 1000.0

    // Clean up output file
    File(outputPath).delete()

    return BenchmarkResult(
        language = "kotlin",
        file_size_mb = fileSizeMB,
        read_time = readTime,
        write_time = writeTime,
        read_throughput_mbs = fileSizeMB / readTime,
        write_throughput_mbs = fileSizeMB / writeTime
    )
}

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        System.err.println("Usage: kotlin App <file_size_mb>")
        System.exit(1)
    }

    try {
        val fileSizeMB = args[0].toInt()
        val result = benchmarkIO(fileSizeMB)
        val gson = Gson()
        println(gson.toJson(result))
    } catch (e: Exception) {
        System.err.println("Benchmark failed: ${e.message}")
        System.exit(1)
    }
}
