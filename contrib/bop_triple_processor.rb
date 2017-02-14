#!/bin/env ruby

require 'csv'

# sample file format:
#1  TRIP: JUSTIN STEWART           JUSTIN STEWART           M 29   04:10.1  0:13:00.9
#                                      JUSTIN STEWART           M 29   04:22.8
#                                      JUSTIN STEWART           M 29   04:28.0
#
#2  TRIP: MATTHEW SRADERS          MATTHEW SRADERS          M 20   04:26.3  0:13:22.8
#                                  MATTHEW SRADERS          M 20   04:26.4
#                                  MATTHEW SRADERS          M 20   04:30.1

# this won't handle racers who didn't do 3 full climbs. it appears that
# the timing company doesn't put a total on the first line for those competitors,
# so I'm silently dropping them from the results.

# this will not handle "RACEDAY ENTRY" lines from older years, either. you should
# remove those before processing the results.

racer_1st_line_fields = ['first_name', 'last_name', 'sex', 'age', 1, 'total']

csv_order = ['empty', 'full_name', 'age', 'sex', 1, 2, 3, 'total']

racers = []
current_racer = nil
next_fastest_trip = 2
ARGF.each_line do |line|
	line.chomp!
	# skip empty lines.
	next if line.length == 0

	fields = line.split(' ')
	# start an entry if the line starts with their place.
	if (/\d+/.match(fields[0]) && /TRIP:/.match(fields[1]))
		puts "adding racer: #{fields[2]} #{fields[3]}"
		if !current_racer.nil?
			current_racer['full_name'] = "#{current_racer['first_name']} #{current_racer['last_name']}"
			racers << current_racer
		end
		current_racer = {}
		# this walks the current line backwards, and the racer key
		# fields forwards
		-1.downto(-6) do |idx|
			field_name = racer_1st_line_fields[idx]
			current_racer[field_name] = fields[idx]
		end
		# the first line has the fastest time and total. the next
		# two lines will have the 2nd and 3rd fastest times for the
		# racer.
		next_fastest_trip = 2
		current_racer['place'] = fields.first.to_i
	elsif (fields[0] == current_racer['first_name'] && fields[1] == current_racer['last_name'])
	    puts "adding trip #{next_fastest_trip} for #{current_racer['first_name']} #{current_racer['last_name']}"
		current_racer[next_fastest_trip] = fields.last
		next_fastest_trip += 1
	end	
end

# just in case places get wacky somewhere in the middle, save based on the incoming order of results.
CSV.open('bop-triple.csv', 'wb', {:write_headers => true, :headers => csv_order}) do |fh|
	racers.each { |racer| fh << racer }
end
