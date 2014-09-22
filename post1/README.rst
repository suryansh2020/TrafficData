Descriptive Statistics
======================

What do we know about rush hour?
--------------------------------

Do we know when rush hour starts and stops? Is rush hour the same
for everyone? These are some pretty simple questions that I can't
answer. I have a rough idea, like most people, but if I had a better
idea then maybe it would be easier/simpler to avoid. The goal of post1
is to be introduced to the data while trying to answer a meaningful
question.

Data for real time traffic monitoring is located at massdot developer
data <http://www.massdot.state.ma.us/DevelopersData.aspx>. In this
post, we're interested in how traffic has behaved over time. We want
to know descriptive statistics on the speed of traffic.

MassDOT has kindly provided Real Time Travel Times for sections of
I-93, I-90 and Route 3 in Massachusetts. That data can be accesssed
in a more or less easy fashion on github <https://github.com/hackreduce/MassDOThack/tree/master/Road_RTTM_Volume>.

What does the data look like?
-----------------------------

* pair_id
  - Identifies a pair of bluetooth sensors in a certain direction
* insert_time
  - The time at which the measurement was made
* travel_time
  - The time in seconds it takes for cars to travel the
    road segment between the two sensors

How can this be figured out?
----------------------------

Using these things:

1) Time/date measurement was taken
2) Direction of traffic (northbound or southbound)
3) Location of traffic
4) Distance, the miles between a roadway segment

We should be able to figure to out these things:

1) descriptive stats of speed per segment over time.

We know the distance of each segment, the time cars traveled over a
five minute segment on average, and the location of those segments. I
think we should also be able to figure out the time of day the
measurement was taken.

The historical data available takes too long to query in mysql so
we're going to see how this goes with hadoop and mapreduce. Unless an
easier way appears then the descriptive stats will have to be
calculated from scratch without using really nice functions available
like mean().

Fortunately, an easier way did appear. This did take a long time to do
in mysql but it works just fine in R when we load it as a CSV. So
instead of trying to join things up in mysql, we'll just write some
custom scripts in Python. It would be exceedingly cumbersome in a sql
database because we're trying to mix and match with csv and xml data
types.

What to do:
-----------

At the end of the day, we're reading a csv file into some d3.js code.
Here's our csv format:

|Route,time,speed,direction|

|I-93,06:00:00 AM,65mph,SB|

Solving for CSV cells
=====================

Unfortunately, the data isn't in this format. We have to find a way to
solve for Route, time, speed, and direction.

Route
-----

1) *Account for PairID across data sources.* - Done
   * Given pair_id, match 'massdot_bluetoad_data$pair_id' with
     'pair_definitions$pair_id' to make sure no ids are unaccounted.
   * Next, group 'massdot_bluetoad_data$pair_id' and see if we can
     account for pair_routes.xml; <PairID>. If we are unable to account
     for all pair Ids then figure it out. Hopefully, it's fine.

2) Map coordinates to road names using Google Maps API
   * Collect <PairID> and <Routes> from pair_routes.xml. Match each
     <Route> in <Routes>, returns latitude and longitude, with a
     location using the Google API for reverse geocoding <https://developers.google.com/maps/documentation/geocoding/#ReverseGeocoding>.

   * This is totally going to need some work & should be addressed
     first. Instead of the Google API, we're going to use geonames.org
     <http://api.geonames.org/findNearbyStreets?> .

3) Format road names
   * We want to return a list of tuples; (pair_id, road_name). Google
     may or may not format road names how you would like so just clean
     it up if necessary.

Time
----

pass

Speed
-----

pass

Direction
---------

pass





