import argparse
import json
import pytz
from datetime import datetime
from dateutil import parser
from pprint import pprint
from icalendar import Calendar, Event
from textwrap import dedent

local_tz = pytz.timezone("Europe/Stockholm")



def main():
    if order_id is None:
        with open("./tickets.json") as tickets_file:
            data = json.load(tickets_file)
    else:
        import httpx
        data = httpx.get(f"https://api.goteborgfilmfestival.se/api/Ticket/Order/{order_id}").json()

    tickets = data["result"]
    # pprint(tickets[0])
    cal = Calendar()
    cal.add('prodid', '-//GFF Cal//hultner.se//')
    cal.add('version', '2.0')
    added_events = set()
    for ticket in tickets:
        if (event := ticket["eventKey"]) in added_events:
            continue
        cal.add_component(create_event(ticket))
        added_events.add(event)
    with open('gff_cal.ics', 'wb') as f:
        f.write(cal.to_ical())



def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary


def create_event(ticket):
    description = dedent(f"""
        Info: https://program.goteborgfilmfestival.se/program/{ticket['eventKey']}
        Visining: {ticket['location']}
        Special: {ticket.get('specialTag', "Nej")}
    """)
    if order_id is not None:
        description = description + f"\nBiljetter: https://program.goteborgfilmfestival.se/biljetter/{order_id}\n\n"
        description = description + f"Festivalpass: https://program.goteborgfilmfestival.se/festivalpass/{order_id}\n"
    start = utc_to_local(parser.isoparse(ticket['timeStart']))
    end = utc_to_local(parser.isoparse(ticket['timeEnd']))
    event = Event()
    event.add("summary", f'{ticket["title"]} {ticket.get("specialTag", "")}'.strip())
    event.add("location", ticket["location"])
    event.add("dtstart", start)
    event.add("dtend", end)
    event.add("description", description)
    # pprint(end)
    # pprint(event)
    return event


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("order")
    args = arg_parser.parse_args()
    order_id = args.order
    main()
