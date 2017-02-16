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

# does not handle names like "GEORGE BURNHAM SR." or "RICKY BOBBY NASCAR III".
# look in bop_triple_processor.v1.rb for code that can do that.

racer_1st_line_fields = ['sex', 'age', 1, 'total']

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
	puts "names: #{names}"
	puts "non name fields: #{non_name_fields}"
	return [names, non_name_fields]
end

racers = []
current_racer = nil
next_fastest_trip = 2
racer_subnames = []

ARGF.each_line do |line|
	line.chomp!
	# skip empty lines.
	next if line.length == 0

	fields = line.split(' ')
	# start an entry if the line starts with their place.
	if (/\d+/.match(fields[0]) && /TRIP:/.match(fields[1]))
		# add any existing racer before starting to save info for a new racer
		if !current_racer.nil?
			current_racer['full_name'] = racer_subnames.join(' ')
			racers << current_racer
		end
		current_racer = {}
		racer_subnames = []
		racer_subnames, remaining_fields = find_and_remove_racer_name(fields.slice(2..-1))
		puts "racer #{racer_subnames.join(' ')}: #{fields.last}"
		puts "\tfastest climb: #{fields[-2]}"
		puts "remaining fields: #{remaining_fields}"
		0.upto(racer_1st_line_fields.length-1) do |idx|
			field_name = racer_1st_line_fields[idx]
			current_racer[field_name] = remaining_fields[idx]
		end
		# the first line has the fastest time and total. the next
		# two lines will have the 2nd and 3rd fastest times for the
		# racer.
		next_fastest_trip = 2
		current_racer['place'] = fields.first.to_i
	elsif (fields[0...racer_subnames.length] == racer_subnames)
	    puts "\tnext fastest climb: #{fields.last}"
		current_racer[next_fastest_trip] = fields.last
		next_fastest_trip += 1
	end	
end

# just in case places get wacky somewhere in the middle, save based on the incoming order of results.
CSV.open('bop-triple.csv', 'wb', {:write_headers => true, :headers => csv_order}) do |fh|
	racers.each { |racer| fh << racer }
end
