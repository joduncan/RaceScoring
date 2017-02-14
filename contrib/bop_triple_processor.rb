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

# this should handle racers who only did 1 or 2 trips, but I have not verified
# that.

# this will not handle "RACEDAY ENTRY" lines from older years... yet.

racer_1st_line_fields = ['first_name', 'last_name', 'sex', 'age', 1, 'total']

csv_order = ['place','sex', 'age', 'first_name', 'last_name', 1, 2, 3, 'total']

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
		racers << current_racer if current_racer != nil
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
#		current_racer['total'] = fields[-1]
#		current_racer[1] = fields[-2]
#		current_racer['age'] = fields[-3]
#		current_racer['sex'] = fields[-4]
#		current_racer['last'] = fields[-5]
#		current_racer['first'] = fields[-6]
	elsif (fields[0] == current_racer['first_name'] && fields[1] == current_racer['last_name'])
	    puts "adding trip #{next_fastest_trip} for #{current_racer['first_name']} #{current_racer['last_name']}"
		current_racer[next_fastest_trip] = fields.last
		next_fastest_trip += 1
	end	
end

# racers.each { |racer| }
CSV.open('bop-triple.csv', 'wb', {:write_headers => true, :headers => csv_order}) do |fh|
	racers.sort { |a,b| a['place'] <=> b['place'] }.each { |racer| fh << racer }
end