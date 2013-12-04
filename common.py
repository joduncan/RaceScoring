
races_that_count = 5 

athlete_best_races = 'select race.name,max(points),min(rank) from results join race on race = race.id where athlete = ? group by race.name order by max(points) desc limit ?'
 
# a given race has a score of _n_
# each place is computed as 5/5+zero-based rank
#
def factorizer( factor ):
  factor *= 5.0
  d = 5
  while True:
    yield factor / d
    d +=1


