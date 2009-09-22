# Hackish parser to parse the CS York timetable (once you've already hacked it a bit manually
# Written by David Somers in 2009

# My Python is awful. Forgive me. I know nothing about it, I'm just using it because BeautifulSoup
# is nice. PLEASE make this prettier.
# Also, I haven't tested it on anything except the 2009 3rd year timetable. I just made it for
# me really...So please improve it and hand it back. Make a pull request, or whatever it is you
# do with github, I'll work it out.

from BeautifulSoup import BeautifulSoup
from icalendar import Calendar, Event, UTC
from datetime import datetime, timedelta
from pytz import timezone
from collections import defaultdict
import re

days = range(0,5)
times = range(9,20)
modules = []

def leaf( tag ):
	o = []
	t = []
	# Probably a rubbish way of doing this, too
	for text in tag.findAll( text=True ):
		text = text.strip()
		if text:
			if (len(text) == 3) and t != []:
				o.append(t)
				t = []
			t.append(text)
	if len(t) > 1:
		o.append(t)
	return o

def trow_cols( trow, time, cal, td="td" ):
    row = 0
    cols = []
    for col in trow( td ):
        data = leaf( col )
	# There's not quite enough indentation here.
	if len(data) > 0:
		for i in data:
			if len(i) > 0:
				for j in range(2, len(i)):
					# Hackish way of finding the right thing
					if i[j].startswith("LECT") or i[j].startswith("PRAC"):
						module = i[0]
						room = i[1]
						k = i[j].split(None, 1)
						type = k[0]
						weeks = k[1]
						lecturer = i[j+1]
				if module in modules:
					print "  Module:",module
					if type == "LECT":
						type = "Lecture"
					else:
						type = "Practical"
					print "  Type:",type
					print "  Time:",time
					print "  Day:",days[row]
					print "  Room:",room
					print "  Weeks:",parse_weeks(weeks)
					# I come from Erlang, I need list comprehensions
					dates = [calculate_date(x, days[row], time) for x in parse_weeks(weeks)]
					print "  Lecturer:",lecturer
					# I've guessed that this is probably OK
					datestr = "%Y%m%dT%H%M%SZ/123123123@protane.co.uk"
					for l in dates:
						event = Event()
						event.add('summary', module + " " + type)
						event.add('location', room)
						event.add('dtstart', l)
						event.add('dtend', l + timedelta(hours=1))
						event.add('dtstamp', datetime.now())
						event['uid'] = l.strftime(datestr)
						cal.add_component(event)
					print 			 
		row = row + 1
		
    return cal

def parse_weeks(weeks):
	# Remove stuff. I bet there's a nicer way to do this
	weeks = weeks.replace("au", "").replace("\"", "").replace(",", "").replace("wks", "")
	if len(weeks.split(" ")) > 1:
		return [int(x) for x in weeks.split(" ")]
	if len(weeks.split("-")) > 1:
		r = weeks.split("-")
		return range(int(r[0]), int(r[1]))
	return [int(weeks)]

def calculate_date(week, day, hour):
	date = datetime(2009, 10, 12, 0, 0)
	date = date + timedelta((7 * (week - 1)) + day)
	date = date + timedelta(hours=hour, minutes=15)
	return to_utc(date)
	
# Probably a nicer way to do this too.
def to_utc(dt):
	return timezone('Europe/London').localize(dt).astimezone(timezone('UTC'))

# Change this to wherever your timetable.html is
f = open('timetable.html', 'r')
html = f.read()
soup = BeautifulSoup(html)

table = soup.findAll("table")[0]
rows = table("tr")

cal = Calendar()
# Uh...yeah, this seems to do the trick
cal.add('prodid', '-//CompSci Calendar//jalada//')
cal.add('version', '2.0')
cal.add('calscale', 'gregorian')

foo = "notnothing"
while foo != "":
	foo=raw_input('Enter a module, blank line to finish: ')
	modules.append(foo)
	
count = 0
for row in rows:
	cal = trow_cols(row, times[count], cal)
	count = count + 1

f = open('timetable.ics', 'wb')
f.write(cal.as_string())
f.close()

print "Timetable written to timetable.ics"
