import sys
from .helpers import load, get_events
from .util import swimtimefmt

meetinfo = load(sys.argv[1])
#print(repr(meetinfo.))

for event in get_events(meetinfo):
    print(event['event_number'],event['stroke'],event['distance'],event['course'],event['date'])
    for entry in event['entries']:
        #print(repr(entry))
        if entry['relay']:
            print(" * relay - ",entry['heat'],entry['lane'],entry['teamname'],', '.join([e['name'] for e in entry['swimmers']]),entry['event_type'])
        else:
            print(" * ",entry['heat'],entry['lane'],entry['swimmers'][0]['name'],swimtimefmt(entry['seed_time_ms']),entry['event_type'])

