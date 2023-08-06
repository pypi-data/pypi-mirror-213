from .hy3 import HY3_EVENT_TYPE_CODES, HY3_STROKE_CODES, HY3_STROKE_CODES_SHORT, HY3_EVENT_COURSE_CODES
import datetime, csv, codecs
from .util import swimtime_strtoms

GENDER_CODES = {
    "M":"Men",
    "W":"Women",
    "F":"Women",
    "B":"Men",
    "G":"Women",
    "X":"Mixed",
}

def _try_int(numstr):
    try:
        return int(numstr)
    except ValueError:
        return None

def _mm_slash_dd_slash_yyyy_date_to_iso_date(ds):
    if len(ds)==10:
        return ds[6:10]+"-"+ds[0:2]+"-"+ds[3:5]
    else:
        return None

def load(fo):
    meetinfo = {}
    csvfo = csv.reader(codecs.getreader('latin')(fo),delimiter=";")

    meetinfo_line1 = next(csvfo)

    meetinfo['name'] = meetinfo_line1[0].strip()
    meetinfo['location'] = meetinfo_line1[1].strip()
    meetinfo['startdate_str'] = meetinfo_line1[2].strip()
    meetinfo['startdate'] = _mm_slash_dd_slash_yyyy_date_to_iso_date(meetinfo['startdate_str'])
    meetinfo['enddate_str']   = meetinfo_line1[3].strip()
    meetinfo['enddate'] = _mm_slash_dd_slash_yyyy_date_to_iso_date(meetinfo['enddate_str'])

    meetinfo['qualifying_age_date'] = _mm_slash_dd_slash_yyyy_date_to_iso_date(meetinfo_line1[4].strip())
    meetinfo['qualifying_date_from'] = _mm_slash_dd_slash_yyyy_date_to_iso_date(meetinfo_line1[16])
    meetinfo['qualifying_date_to'] = _mm_slash_dd_slash_yyyy_date_to_iso_date(meetinfo_line1[23])

    meetinfo['events'] = []

    eventinfo = None
    for eventinfo_line in csvfo:
        if eventinfo_line[13]=="D":
            # TODO: handle paraswimmer events. I don't know how to parse
            # these lines today.
            continue
       
        if eventinfo is None or eventinfo['event']!=eventinfo_line[0]:
            eventinfo = {
                    "event":eventinfo_line[0],
                    "event_number":_try_int(eventinfo_line[0]),
                    "date":None, #TODO: figure this out
                    "gender":GENDER_CODES[eventinfo_line[5]],
                    "gendercode":eventinfo_line[5],
                    "course":HY3_EVENT_COURSE_CODES[eventinfo_line[25]],
                    "coursecode":eventinfo_line[25],
                    "stroke":HY3_STROKE_CODES[eventinfo_line[9]],
                    "strokeshort":HY3_STROKE_CODES_SHORT[eventinfo_line[9]],
                    "distance":int(eventinfo_line[8]),
                    "relay":eventinfo_line[4]=="R",
                    "type":HY3_EVENT_TYPE_CODES[eventinfo_line[2]],
                    "eligibility":[],
                    "entries":[],
                    "num_heats":None
                }
            meetinfo['events'].append(eventinfo)
        
        if eventinfo_line[16].strip():
            eventinfo['eligibility'].append({
            "age_from":int(eventinfo_line[6]),
            "age_to":int(eventinfo_line[7]),
            "time_ms":swimtime_strtoms(eventinfo_line[16].strip()),
            "course":"LCM",
            "gendercode":eventinfo_line[5],
            "gender":GENDER_CODES[eventinfo_line[5]],
            })
        if eventinfo_line[18].strip():
            eventinfo['eligibility'].append({
            "age_from":int(eventinfo_line[6]),
            "age_to":int(eventinfo_line[7]),
            "time_ms":swimtime_strtoms(eventinfo_line[18].strip()),
            "course":"SCM",
            "gendercode":eventinfo_line[5],
            "gender":GENDER_CODES[eventinfo_line[5]],
            })
        if not (eventinfo_line[16].strip() or eventinfo_line[18].strip()):
            eventinfo['eligibility'].append({
            "age_from":int(eventinfo_line[6]),
            "age_to":int(eventinfo_line[7]),
            "time_ms":None,
            "gendercode":eventinfo_line[5],
            "gender":GENDER_CODES[eventinfo_line[5]],
            })


    return meetinfo