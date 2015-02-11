import com.github.tototoshi.csv._
import java.io._

object RaceScoring {
    def main(args: Array[String]) {
	val reader = CSVReader.open(new File("data/2015-oakbrook-ph.csv"))
        val contents = reader.all()
	    for( row <- contents ) {
		for( cell <- row ) {
		    print( cell + " " )
		}
		println()
	    } 
    }
}