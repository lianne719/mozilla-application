*tracking-firefox17+.py*

A python script that gets the buglist of all bugs fixed between 10-09-2012 and 11-19-2012 that were marked as tracking-firefox17+ at some point in that 6 week time. More details on `Mozilla's GNOME Women's Outreach Program 2013`_
.. _Mozilla's GNOME Women's Outreach Program 2013: https://wiki.mozilla.org/GNOME_Outreach_Winter2013

From the results obtained, the total bugs under tracking-firefox17+ at the beginning of the period and the daily fluctuation between added and removed bugs seem to be the correct number. Unfortunately, the decrement of open bugs does not match what has been expected (100+ initially, decreasing significantly during the first five weeks, then decreasing further to zero at the end). After some debugging, I found out that it is because some bugs have statuses NEW till this date, which explains why the total open bugs do not decrease to zero, so I am still trying to work out what to do next.

Installation
------------

This implementation requires bztools from::
    https://github.com/mozilla/bztools
