Hackish York CompSci Timetable Parser
=====================================

(I've no idea if it works very well)

Basically, coming into the third year I didn't want to have to work through all
the timetable AGAIN, particularly with all the different modules and so on. So I
spent a few hours hacking together this timetable parser based around
BeautifulSoup and iCalendar.


How to use it
-------------

1.  Download your timetable file (in HTML format). timetable.html here is
    the 3rd year timetable
2.  Hack it about a bit: remove all &lt;center&gt; and &lt;/center&gt; tags, the day headers
    and any other cruft around the %lt;table%gt;. Anything that isn't a 3 letter module
    needs to go (e.g. things called Talk2) or changed to a 3 letter module (the
    code relies on looking for 3 letter acronyms).
3.  Save it as timetable.html (or adjust the source code of parser.py)
4.  Install [iCalendar] [ic], a Python library that does clever things to make
    iCal files.
5.  Run csyorkttparser.py and tell it your modules.
6.  Profit!

[ic]: http://codespeak.net/icalendar/


How to help
-----------

 - Make my Python proper Python, and make it do fancier things and not be quite
   so hacky.
