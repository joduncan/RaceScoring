
--import System.Environment   
--import Text.CSV

data Score   = Score   { race     :: Race , 
                         place    :: Int ,
                         points   :: Int } 

data Athlete = Athlete { aname    :: String , 
                         sex      :: String , 
                         age      :: Integer } deriving (Show,Read)
                         
data Race    = Race    { rname    :: String , 
                         date     :: String , 
                         url      :: String , 
                         rpoints  :: Int } deriving (Show,Read)

r = Race "Bop to the top" "2014-1-18" "foo" 100

al = [ Athlete "kristin frey" "f" 30 , Athlete "David Hanley" "m" 41 ]

e = (r,al) 

el = [e]

--fn = writeFile "test.hd" (show el)

go l = do
  str <- (readFile "test.hd")
  str
  --(read str)::[(Race,[Athlete])]
                   
--read_csv fn = 
--  do
--    filedata <- (readFile fn)
--    let eventT:dateT:urlT:pointsT:athletes = lines filedata 
--        r = Race eventT dateT urlT (read pointsT ) in
--        r

--go args = do 
--  csvs <- mapM read_csv args 
--  print csvs
 
--test = 
--  go ["data/2013-tulsa.csv","data/2013-aon-step-up-for-kids.csv"]
    
--main = do
--  args <- getArgs 
--  go args 