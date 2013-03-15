
athlete_best_races = 'select race.name,max(points) from results join race on race = race.id where athlete = ? group by race.name order by max(points) desc limit 5'
 
