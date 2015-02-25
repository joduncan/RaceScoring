import com.github.tototoshi.csv._
import java.io._

object Utils 
{
  def toInty(s: String):Option[Int] = {
    try {
      Some( s.toInt )
    } catch {
      case e:Exception => None
    }
  } 
}

case class RaceRow( name : String , age: Option[Int] , gender: String ) {
  //def this( name : String , age : String , gender: String ) = this( name , Utils.toInty( age ) , gender )
}

object RaceScoring {
    def main(args: Array[String]) {
	val reader   = CSVReader.open(new File("data/2015-oakbrook-ph.csv"))
        val it = reader.iterator 
        //val contents = reader.all()
        val name     = it.next
        val date     = it.next
        val url      = it.next
        val points   = it.next
	for( row <- it ) {
          val rr = RaceRow( row( 1 ) , Utils.toInty( row ( 2 ) ) , row( 3 ) ) 
          println(rr)
	} 
    }
}