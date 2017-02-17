#!/bin/env ruby

require 'csv'

# sample file format: (from 2014, 2015. 2013 is identical except using "TRIPLE:" instead of "TRIP:")
#    1  TRIP: ERIC LENINGER            ERIC LENINGER - 1        M 30   03:47.0  0:11:34.2
#                                      ERIC LENINGER - 3        M 30   03:50.8
#                                      ERIC LENINGER - 2        M 30   03:56.4
#
#    2  TRIP: GREG GROSICKI            GREG GROSICKI - 2        M 25   04:04.0  0:12:22.4
#                                      GREG GROSICKI - 3        M 25   04:04.3
#                                      GREG GROSICKI - 1        M 25   04:14.1

# this won't handle racers who didn't do 3 full climbs. it appears that
# the timing company doesn't put a total on the first line for those competitors,
# or count them as finishers, so I'm silently dropping them from the results.

# this will not handle "RACEDAY ENTRY" lines from older years, either. you should
# remove those before processing the results.

racer_1st_line_fields = ['placeholder', 'climb_number', 'sex', 'age', 'climb_time', 'total']

csv_order = ['empty', 'full_name', 'age', 'sex', 1, 2, 3, 'total']

def find_and_remove_racer_name(fields)
	names = []
	index = 0
	while (!names.include?(fields[index])) && (index < fields.length) do
		names << fields[index]
		index += 1
	end
	non_name_fields = fields
	names.each { |subname| non_name_fields.delete(subname) }
	return names, non_name_fields
end

racers = []
current_racer = nil
racer_subnames = []

ARGF.each_line do |line|
	line.chomp!
	# skip empty lines.
	next if line.length == 0

	fields = line.split(' ')
	# start an entry if the line starts with their place.
	if (/\d+/.match(fields[0]) && (/TRIP:/.match(fields[1]) || /TRIPLE:/.match(fields[1])))
		# add any existing racer before starting to save info for a new racer
		if !current_racer.nil?
			current_racer['full_name'] = racer_subnames.join(' ')
			racers << current_racer
		end
		current_racer = {}
		racer_subnames = []
		racer_subnames, remaining_fields = find_and_remove_racer_name(fields.slice(2..-1))
		puts "racer #{racer_subnames.join(' ')}: #{fields.last}"
		puts "\tclimb #{fields[-5]}: #{fields[-2]}"
		# this walks the current line backwards, and the racer key
		# fields forwards
		0.upto(racer_1st_line_fields.length-1) do |idx|
			field_name = racer_1st_line_fields[idx]
			current_racer[field_name] = remaining_fields[idx]
		end
		# this takes the '1st' climb time and associates it with the appropriately numbered climb
		climb_number = fields[-2].to_i
		current_racer[climb_number] = current_racer['climb_time']
		current_racer['place'] = fields.first.to_i
	elsif (fields[0...racer_subnames.length] == racer_subnames)
		# the first line has the fastest time and total. the next
		# two lines will have the 2nd and 3rd fastest times for the
		# racer.
		climb_number = fields.slice(racer_subnames.length..-1)[1].to_i
	    puts "\tclimb #{climb_number}: #{fields.last}"
		current_racer[climb_number] = fields.last
	end	
end

# just in case places get wacky somewhere in the middle, save based on the incoming order of results.
CSV.open('bop-triple.csv', 'wb', {:write_headers => true, :headers => csv_order}) do |fh|
	racers.each { |racer| fh << racer }
end
