
import com.bizo.mighty.csv.CSVReader

object Foo
{
	def main( args: Array[ String ] )
	{
	    val rows: Iterator[Array[String]] = CSVReader("data/2014-strat.csv")
		//println( "Hello, world!" );
		for ( row <- rows )
		    {
			for ( col <- row )
			    print( col + "," );
			println();
		    }
      
	}
}