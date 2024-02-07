# Göteborgs filmfestival Calendar Generator

This script take an order id (or at tickets.json file) from Göteborgs filmfestival and creates calendar items for all showings.
Only one calendar item will be generated if multiple tickets are bought to the same event.

The calendar event includes the following things:
 - Title of the movie/event as the name, with any special tag included
  - A special tag can for instance be
    - DocBar
    - Meet the filmmakers
    - Award Cermony
    - Actors talk
    - etc
 - Start and end time from the event, usually start time and duration of the movie, some movies especially with special tags can sometimes be longer then the tickets specified length.
 - Location, the location from the ticket, e.g. "Draken" or "Stora Teatern"
 - Desciption with
  - Info: with a link to the movie info on goteborgfilmfestival.se program site
  - Visning: The localtion of the movie repeated
  - Special: The special tag from the title or simply "Nej" of no special is given
  - If an order id is used  instead of a tickets.json the following are also added.
    - Biljetter: A link to the tickets from the order. I have not found a way to link to one particular ticket so you may have to scroll.
    - Festivalpass: A link to the festival passes if those are bought in the same order.


## Usage
Replace `00000000-0000-0000-0000-000000000000` with your order id, this can be found after the last / in your ticket link. This is used to fetch your screenings.

```sh 
$ python gff_cal/generate.py 00000000-0000-0000-0000-000000000000
# The file gff_cal.ics will now be created and can opened with your prefered calendar application, tested on Android Google Calendar and Apple iCal/Calendar.app. 
```

## Known Limitations

If theres a special viewing filmfestival still seems to report the usual viewing time. This is a limitation from filmfestivalen and should be kept in mind if you are cutting the time between screenings short.
If you've bought your "festivalpass" separately from the tickets the link to the passes won't work, but the ticket links still will, this is because the website for the passes uses the order id.
I usually buy my pass/passes in the same order so this haven't been a problem for me, if it were a problem it would be possible to add a second order id for the passes. If you are a silver member you'll also recieve
a physical pass by mail before the festival, I belive you can also get a physical pass at the reception in Bio Draken.
For multiple short movie screenings (like startsladden) the info link doesn't work, I suspect this is because it's a bundle of events, I have note investigated this further, it might be solveable but would require special cases.

