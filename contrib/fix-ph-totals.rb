#!/bin/env ruby

# example usages:
# ruby fix-ph-totals.rb race_results.csv
# fix-ph-totals.rb race_results.csv

# example incoming file contents. 12 numbered climb columns because that's how many the fastest climber completed.
#bib,name,age,sex,1,2,3,4,5,6,7,8,9,10,11,12,total
#    1,Eric Leninger,,m, 3:04,    4:12,    4:11,    4:15,    4:10,    4:19,    4:15,    4:14,    4:16,    4:21,    3:57,    3:42,   48:56
#    2,Liz Ruvalcaba,,f, 3:25,    4:29,    4:28,    4:23,    4:33,    4:21,    4:30,    4:32,    4:25,    4:18,    4:05,    4:22,   51:51
#   22,Robert Liking,,m, 3:53,    4:03,    4:09,    4:23,    4:24,    4:29,    4:37,    4:28,    4:34,    4:25,    4:27,    4:31,   52:23
#   17,Cindy Harris,,f, 4:10,    4:36,    4:39,    4:42,    4:46,    4:45,    4:43,    4:49,    4:45,    4:49,    4:54,   51:38,
#    5,David Hanley,,m, 4:58,    4:59,    4:59,    5:08,    5:17,    5:17,    5:26,    5:27,    5:11,    5:07,   51:49,,
#    4,Dave Kestel,,m, 4:21,    5:04,    5:02,    5:18,    5:21,    5:24,    5:35,    5:24,    5:29,    5:43,   52:41,,
#    3,Joshua Duncan,,m, 3:37,    5:35,    5:30,    5:35,    5:29,    5:31,    5:22,    5:30,    5:26,    5:40,   53:15,,
#   63,Rebecca Valerio,,f,20:30,   22:49,   20:49, 1:04:08,,,,,,,,,
#   62,Todd Thibodeaux,,m, 6:34,    6:34,,,,,,,,,,,


require 'csv'

ARGV.each { |file|
	racers = []
	# turn rows into ruby hashes
	CSV.foreach(file, {:headers => true}) { |row| racers << row.to_hash}

	# remove leading spaces from non-nil fields.
	racers.each { |racer| racer.keys.select{|k| racer[k]}.each { |k| racer[k].lstrip! } }

	# get all the racers that did or did not complete the max # of laps
	# this assumes the input file has the total climb time as one of the "middle" climbs
	# for slower climbers, not as the final column of data.
	speedsters, slowpokes = racers.partition { |racer| !racer["total"].nil? }

	# now to find each slower racer's total climb time.
	slowpokes.each do |slowpoke|
		# this perl-esque line selects all numeric keys, sorts them, and picks the last key with a non-nil climb time.
		# this should be the total climb time for the climber.
		# in english:
		# select all keys from this hash where the integer conversion of the (string-typed) key is greater than zero.
		# (any non-integer string implicitly converts to 0)
		# of those keys, sort them based on their numeric values
		# of the sorted keys, select only the ones that have a non-null value associated in the hash
		# of the non-null values(as sorted by related ascending climb number), take the last one

		swap_climb = slowpoke.keys.select { |k| k.to_i > 0 }.sort { |a,b| a.to_i <=> b.to_i }.select { |key| !slowpoke[key].nil? }.last

		# puts "swapping #{swap_climb} for #{slowpoke["name"]}"
		slowpoke["total"] = slowpoke[swap_climb]
		slowpoke[swap_climb] = nil
	end
	# now combine both lists and write them out to a file.
	fixed_racers = speedsters.concat(slowpokes)
	
	CSV.open(file, 'wb', {:write_headers=>true, :headers => fixed_racers[0].keys}) do |fh|
			fixed_racers.each { |racer| fh << racer }
	end
}