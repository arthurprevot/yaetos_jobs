// Example job in scala, to show how to run a spark scala job in Yaetos. Yaetos will setup the job to be run by spark-submit. 
import org.apache.spark.sql.SparkSession
import java.nio.file._


// object LineCounter {
object Main {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder.appName("Line Counter").getOrCreate()

    val currentDirectory = Paths.get("").toAbsolutePath.toString
    println(s"### Current Directory: $currentDirectory")

    // Read the text file
    val fname = args(0)
    val textFile = spark.read.textFile(fname)
    println(s"### Args: $fname")

    // Count the number of lines
    val numLines = textFile.count()

    // Print the result
    println(s"### Number of lines in the file: $numLines")

    spark.stop()
  }
}