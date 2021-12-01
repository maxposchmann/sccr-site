# Explanation:

I was looking at a couple of computer CFB rankings, and the following occurred to me:
 - I can use a computer.
 - I know about football.
 - My opinions are better than other people's opinions.

So of course I had to do my own ranking system. Here are my principles:
 - Games are won or lost. Point differentials are meaningless. Really, your team is better because your 8th-string QB rushed for a couple garbage time TDs?
 - Wins and losses both matter. Equally.
 - The order in which games are played doesn't matter. No late-season bias. No inertia.
 - Beating a good team is better than beating a bad team, and similarly losing to a good team isn't as bad as losing to a bad team.
 - No judgement should be involved. No adjustable paramenters. In other words, there's no seed from a preseason poll, nor should there be sorting by P5/G5 etc. The rankings themselves have to determine what is a good win.
 - The team strengths used to generate the rankings should return themselves if run through the algorithm again. Put another way, the "Alabama only has quality losses to teams that beat Alabama" problem should be addressed quantitatively.

And thus the Self-Consistent CFB Ranker (SCCR) was born. The guts of the ranking are as follows: an exponential function takes the "strength" of the opponent and uses win/loss outcome to set the sign. This nonlinear function makes signature wins and season-defining losses possible. The algorithm iterates until self-consistency of strengths. Multiple games are counted separately, rather than cancelling.

The "strength" has units of wins, and therefore is called Net Adjusted Wins (NAW), with losses negative. The algorithm is initialized with the unadjusted net wins (i.e. simply wins-losses) for each team. The inputs to the exponential are scaled by the largest magnitude NAW, so the maximum possible difference between values of FBS wins (or losses) is exp(2) = 7.389. By this win metric, a team would do much better to split a series with the best team in FBS (+2.3504 net wins) than to beat the worst team in FBS twice (+0.7358 net wins). This feels reasonably fair, and also has the benefit of converging well. However, it would be trivial to replace this NAW function with any other function that tends to converge. Please feel free to fork the project and play with whatever system you think better represents the relative values of wins.

Also (optionally) output is Average Adjusted Wins (AAW), which is NAW per game played. The NAW of the Completed Schedule (NCS) and NAW of Remaining Schedule (NRS) for each team are also output with the extended print option set to true.

One caveat about the "no inputs" thing: only FBS teams are tracked, and all non-FBS teams have NAW set to (minimum FBS NAW - 1.0).

Results are downloaded from Sports Reference (i.e. https://www.sports-reference.com/cfb/years/2021-schedule.html click on "Share & Export" then "Get table as CSV (for Excel)").

# Team Reports:

If team names are given as arguments, a report on the specified teams will be output instead of the full rankings. This includes the games played by that team, the outcomes of those games, and how they affected the computed team NAW. If games remain on the schedule, those are shown separately, along with estimated NAW changes for win/loss outcomes.

For example, California after week 13, 2021:

California (4 - 6)

|       | &numsp; &numsp; |   NAW   | &numsp; &numsp; |   AAW   | &numsp; &numsp; |   NCS   | &numsp; &numsp; |   NRS   |
|-------|-|---------|-|---------|-|---------|-|---------|
| Value | |  -4.201 | |  -0.420 | |   8.933 | |   2.047 |
| Rank  | |     100 | |     102 | |     125 | |       9 |

| Played                    | &numsp; &numsp; | Outcome    | &numsp; &numsp; |  Change  |
|---------------------------|-|------------|-|----------|
|  71 Texas Christian       | | Loss       | | -  0.997 |
|  44 Nevada                | | Loss       | | -  0.837 |
| 105 Stanford              | | Win        | | +  0.692 |
|  64 Washington State      | | Loss       | | -  0.947 |
|  20 Oregon                | | Loss       | | -  0.606 |
|  52 Oregon State          | | Win        | | +  1.132 |
| 108 Washington            | | Loss       | | -  1.523 |
|  96 Colorado              | | Win        | | +  0.754 |
| 127 Arizona               | | Loss       | | -  2.210 |
| 131 Non-FBS               | | Win        | | +  0.341 |

| Remaining                 | &numsp; &numsp; |  If Win  | &numsp; &numsp; |  If Loss |
|---------------------------|-|----------|-|----------|
|  86 USC                   | | +  0.853 | | -  1.173 |
|  45 UCLA                  | | +  1.194 | | -  0.837 |

# Examples:
## 2019
Let's take a look at the top 25 prior to bowl games for the 2019 season. I'll use the results as of December 8th to match the final CFP committee:

| Rank | &numsp; &numsp; |Team                  | &numsp; &numsp; | NAW | &numsp; &numsp; | CFP Committee Rank |
|------|-|----------------------|-|----------|-|--------------------|
|     1| |Ohio State            | |16.622| |2|
|     2| |LSU                   | |15.179| |1|
|     3| |Clemson               | |12.756| |3|
|     4| |Memphis               | |12.101| |17|
|     5| |Oklahoma              | |11.840| |4|
|     6| |Boise State           | |11.224| |19|
|     7| |Georgia               | |10.840| |5|
|     8| |Appalachian State     | |10.437| |20|
|     9| |Oregon                | |9.867| |6|
|    10| |Notre Dame            | |9.632| |15|
|    11| |Wisconsin             | |9.452| |8|
|    12| |Penn State            | |9.320| |10|
|    13| |Baylor                | |9.180| |7|
|    14| |Utah                  | |9.117| |11|
|    15| |Cincinnati            | |8.558| |21|
|    16| |Florida               | |8.429| |9|
|    17| |Michigan              | |8.099| |14|
|    18| |Auburn                | |7.988| |12|
|    19| |SMU                   | |7.937| |NR|
|    20| |Minnesota             | |7.762| |18|
|    21| |Alabama               | |7.713| |13|
|    22| |Air Force             | |7.537| |NR|
|    23| |Navy                  | |7.487| |23|
|    24| |Iowa                  | |7.092| |16|
|    25| |Florida Atlantic      | |6.777| |NR|

This ranking results in 3 of the 4 playoff selection, and Oklahoma is only edged out by Memphis by a razor-thin margin. Evidently this ranking system is not the hot-take generator I had feared. In total 4 of the top-25 teams differ from the CFP committee's list. Dropped are 8-4 USC (22), 9-4 Virginia (24), and 8-4 Oklahoma State (25). Added are 10-3 SMU, 11-2 Air Force, and 11-3 FAU. Overall this ranking prefers G5 teams with more wins over P5 teams with fewer, relative to the CFP. I agree.

So 2019 is a nice, uncontroversial year. LSU were champs, they deserved to be in the CFP, and after all bowls SCCR agrees that they were the best.

## 2017
But what about 2017? Starting with the same point (December 3rd), who should have been in the CFP?

| Rank | &numsp; &numsp; |Team                  | &numsp; &numsp; | NAW | &numsp; &numsp; | CFP Committee Rank |
|------|-|----------------------|-|----------|-|--------------------|
|     1| |Clemson               | |14.609| |1|
|     2| |Georgia               | |13.282| |3|
|     3| |Oklahoma              | |13.282| |2|
|     4| |UCF                   | |12.599| |12|
|     5| |Wisconsin             | |12.540| |6|
|     6| |Ohio State            | |12.511| |5|
|     7| |USC                   | |11.728| |8|
|     8| |Alabama               | |11.303| |4|
|     9| |Auburn                | |10.581| |7|
|    10| |Notre Dame            | |10.301| |14|

That's only a little different from the CFP as well.. According to SCCR, UCF should been given a chance to play for the title over Alabama.

Interestingly, the Colley Matrix still put UCF at 1 after bowl games, even though they didn't get to face off in the CFP. Since this ranking bears some similarity in philosophy to Colley, let's see if that's true for SCCR also.

| Rank | &numsp; &numsp; |Team                  | &numsp; &numsp; | NAW |
|------|-|----------------------|-|----------|
|     1| |Alabama               | |16.426|
|     2| |Georgia               | |16.006|
|     3| |Ohio State            | |15.099|
|     4| |Wisconsin             | |14.802|
|     5| |UCF                   | |14.489|
|     6| |Clemson               | |13.863|
|     7| |Oklahoma              | |13.681|
|     8| |Penn State            | |11.798|
|     9| |Notre Dame            | |11.595|
|    10| |Auburn                | |10.879|

Sorry UCF, but SCCR agrees that Alabama were the 2017 national champions, with their playoff victories vaulting them to the top.

# Comparison with Colley Matrix

It has come to my attention that there is already a self-consistent ranking method, the Colley Matrix (https://www.colleyrankings.com/index.html), which was part of the BCS system (prior to the CFP), and is still recognized by NCAA. No surprise that something similar has been done, as Daryl says: there's no such thing as an original sin. Anyway it seems some comparison is warranted. Please note that I am not an expert on the Colley system, but I will do my best to discuss it accurately. The similarities between the two are substantial:
- Only wins and losses are considered (no score differential).
- There is no sorting by conference or history (bias-free).
- The order in which games are played is irrelevant.
- The results are self-consistent.

However, there are also substantial differences between the two methods. First, to state the obvious, the two generate different rankings unless some miraculous coincidence has occurred. Here are some more details and examples:

## Units.

SCCR outputs NAWs with units of wins, with wins against above-average teams being worth >1 win and wins against below-average teams worth <1 win, and with losses negative and opposite to wins. Thus as of week 5 2021, 4-0 Michigan is at \#1 with 4.42142527 effective wins. Meanwhile the Colley matrix returns ratings which are more similar to win percentages. Colley also has Michigan at \#1 for the same week, with a rating of 0.92392. In the Colley system, ratings are (almost) always between 0 and 1, so even an undefeated team with the highest strength-of-schedule will show a rating <1. In SCCR NAWs average around 0, and beating an average team yields exp(0) = 1 wins. In Colley, ratings average to 0.5, i.e. an even win-loss rate.

## Strength-of-schedule adjustments for win/loss outcomes.

Both systems use the strengths of all opponents iteratively to determine the values of wins and losses. However, in Colley whether a particular game was won or lost does not affect the strength of schedule adjustment (to first order). In SCCR the win-loss state is directly accounted for in the NAW exponential function. This is best demonstrated by example. Again, let's take (the current at time of writing) week 5 2021. Rutgers is 3-1, having just lost to \#1 Michigan. In SCCR Rutgers is ranked at \#28 with NAW 1.98208119. In Colley, Rutgers is \#16 with rating 0.7713. Now, let's imagine a hypothetical in which Rutgers had beaten Michigan, but lost a previous game against Temple. In Colley, Rutgers remains at \#16 and has rating 0.7700. This is nearly identical to before. In SCCR, Rutgers rises to \#25 (a jump of 3 positions) and has NAW 2.24361296 (+0.26153177 wins). This is because in SCCR the value of beating a very good opponent outweighs the penalty of losing to a middling opponent. On the other hand, in Colley, Rutger's rating only changes at all because of the changes in the strength-of-schedule of other teams (which is why it hardly budged).

## Differing number of games completed.

As discussed in point 1, SCCR is effectively a cumulative resume rating system, while Colley is based on a rate. Therefore SCCR will prefer teams with larger numbers of games played (or more specifically, won) relative to Colley. I demonstrate this on the 2020 "regular" season (I had to use the Wayback Machine on the Colley website, and this only shows top 25 ranks and no ratings). Here are SCCR and Colley ranks for 2020 as of December 20th:

| Rank | &numsp; &numsp; |Team                  | &numsp; &numsp; | NAW | &numsp; &numsp; | Colley Team |
|------|-|----------------------|-|----------|-|-------------|
|     1| |Coastal Carolina      | |11.935| | Alabama |
|     2| |Alabama               | |11.690| | Cincinnati |
|     3| |Clemson               | |10.739| | Coastal Carolina |
|     4| |Notre Dame            | |9.867| | Clemson |
|     5| |Cincinnati            | |9.789| | Ohio State |
|     6| |Louisiana             | |9.096| | San Jose State |
|     7| |BYU                   | |8.899| | Louisiana |
|     8| |Miami (FL)            | |7.371| | Notre Dame |
|     9| |San Jose State        | |7.199| | BYU |
|    10| |Iowa State            | |6.949| | Miami |
|    11| |Oklahoma              | |6.939| | Ball State |
|    12| |Texas A&M             | |6.507| | Texas A&M |
|    13| |Ohio State            | |6.122| | Indiana |
|    14| |North Carolina        | |5.504| | Oklahoma |
|    15| |Oklahoma State        | |5.369| | Tulsa |
|    16| |Ball State            | |5.338| | Iowa State |
|    17| |North Carolina State  | |5.306| | Georgia |
|    18| |Army                  | |5.261| | USC |
|    19| |Liberty               | |5.109| | Buffalo |
|    20| |Tulsa                 | |4.851| | Colorado |
|    21| |Georgia               | |4.687| | North Carolina |
|    22| |Florida               | |4.681| | North Carolina State  |
|    23| |Marshall              | |4.633| | Army |
|    24| |Appalachian State     | |4.610| | Oklahoma State |
|    25| |Indiana               | |4.608| | Northwestern |

Notice that 6-0 Ohio State has dropped from playoff position at \#3 in the CFP rankings to \#13 here (\#5 in Colley), due to not having earned enough wins in their shortened season. They would have been replaced by the Chanticleers! Now tell me there's a better rating system.

Comparing the Colley rankings to SCCR rankings, the big gainers under Colley were B1G and PAC-12 teams like Ohio State, Indiana, USC, and Colorado, who all played shortened seasons. So as expected, SCCR prefers teams with more wins under their belt relative to Colley. While neither is intended as a predictive method, it is probably fair to say that Colley has more traits of a predictive method and SCCR comes closer to a pure resume ranker.

Note that AAW (NAW per game played) is also available within SCCR, if you prefer an efficiency metric. The top four teams by AAW in 2020 were: Cincinnati, Coastal Carolina, Alabama, and San Jose State.

## What's a win worth?

In SCCR, the answer is the same for everyone: exp({opponent NAW}/{maximum NAW}). In Colley, the answer depends on how your year has been going. Here's an example. As I write this, it is Monday morning following week 13 of 2021. Iowa sits at \#13 in SCCR with NAW of 7.42832202, and \#10 in Colley with rating 0.81598. Meanwhile Ohio is \#121 (-8.07105492) by SCCR and \#123 (0.25856) by Colley. Let's imagine these two took it upon themselves to play an unscheduled match here on Monday morning while the rest of the teams rest. Iowa wins of course. By SCCR, Iowa gains 0.54494081 to total 7.97326283 wins and moves up to \#11. Per Colley, Iowa **loses** 0.00411 rating points and drops to \#11 with 0.81187. Punished for winning!

Now suppose that instead of Iowa, it was the California Golden Bears who beat Ohio tonight. California is currently \#100 (-4.20083795) by SCCR and \#102 (0.36630) by Colley. After this hypothetical win, they gain 0.52891463 wins to move to \#96 (-3.67192332) in SCCR, and gain 0.03103 points to go to \#115 (0.39733) in Colley.

So what do we learn? In Colley, a win against a bad team can decrease your strength-of-schedule adjustment by enough to outweight the value of the win (especially if you are undefeated), while in SCCR beating a given opponent is worth (approximately) the same amount to every team. As we can see, the win value in SCCR is not identically the same because the outcome adjusts the NAWs of schedule for all teams (specifically, California beating Ohio decreases Ohio's NAW by much more than Iowa beating them would). This effect would be diminished if the example was after a complete season, but unfortunately the Colley website only allows for hypothetical games to be added to the current season-in-progress.
