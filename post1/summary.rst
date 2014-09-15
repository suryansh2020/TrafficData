Descriptive Statistics
======================

How fast does traffic move on the highway throughout the day?
-------------------------------------------------------------

Data for real time traffic monitoring is located at massdot developer data <http://www.massdot.state.ma.us/DevelopersData.aspx>. In this post, we're interested in how traffic has behaved over time. We want to know descriptive statistics on the speed of traffic.

MassDOT has kindly provided Real Time Travel Times for sections of I-93, I-90
and Route 3 in Massachusetts. That data can be accesssed in a more or less easy
fashion on github <https://github.com/hackreduce/MassDOThack/tree/master/Road_RTTM_Volume>.

What does the data look like?
-----------------------------

pair_id: Identifies a pair of bluetooth sensors in a particular direction
insert_time: The time at which the measurement was made
travel_time: The time in seconds it takes for cars to travel the road segment between the two sensors

How can this be figured out?
----------------------------

Using these things:

1) Time/date measurement was taken
2) Direction of traffic (northbound or southbound)
3) Location of traffic
4) Distance, the miles between a roadway segment

We should be able to figure to out these things:

1) descriptive stats of speed per segment over time.

We know the distance of each segment, the time cars traveled over a five
minute segment on average, and the location of those segments. I think we should
also be able to figure out the time of day the measurement was taken.

The historical data available takes too long to query in mysql so we're going
to see how this goes with hadoop and mapreduce. Unless an easier way appears
then the descriptive stats will have to be calculated from scratch without using
really nice functions available like mean().

How long will this take?
------------------------

Since I'm cheap, we're going to run this in one vagrant box with 4GB of RAM. It
will probably take awhile.



