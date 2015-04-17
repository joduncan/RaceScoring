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
  def this( name : String , sage : String , gender: String ) = this( name , Utils.toInty( sage ) , gender )
}

case class Athlete( name : String , var age : Option[Int] , gender: String ) { 
}

object RaceScoring {

    def readCsv( fn : String ) { 
      	val reader   = CSVReader.open( new File( fn ) )
        val it       = reader.iterator 
        //val contents = reader.all()
        val name     = it.next
        val date     = it.next
        val url      = it.next
        val points   = it.next
        it.map( row => new RaceRow( row( 1 ) , row( 2 ) , row( 3 ) ) ) 
    }
  
    def main(args: Array[String]) {
        readCsv( "data/2015-oakbrook-ph.csv" ) 
    }
}