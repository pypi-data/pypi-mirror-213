from .util import *

HY3_STROKE_CODES = {
    "A":"Freestyle",
    "B":"Backstroke",
    "C":"Breaststroke",
    "D":"Butterfly",
    "E":"Individual Medley",
    "F":"Freestyle Relay",
    "G":"Medley Relay"
}
HY3_STROKE_CODES_SHORT = {
    "A":"Free",
    "B":"Back",
    "C":"Breast",
    "D":"Fly",
    "E":"IM",
    "F":"Free Relay",
    "G":"Medley Relay"
}
HY3_EVENT_GENDER_CODES = {
    "M":"Men",
    "F":"Women",
    "B":"Boys",
    "G":"Girls",
    "X":"Mixed"
}
HY3_EVENT_COURSE_CODES = {
    "S":"SCM",
    "Y":"SCY",
    "L":"LCM"
}
HY3_EVENT_TYPE_CODES = {
    "P":"Prelim",
    "F":"Final",
}

def _mmddyyyy_date_to_iso_date(ds):
    if len(ds)==8:
        return ds[4:8]+"-"+ds[0:2]+"-"+ds[2:4]
    else:
        return None

def load(fo):
    # starts with A1 instead of A0
    meetinfo = {"teams":[]}
    teams = meetinfo['teams']
    rtypes = {}
    line = 0
    cur_swimmer = None
    cur_entry = None
    cur_team = None
    while ((record := fo.read(132))):
        line += 1
        try:
            rtype = record[0:2]
            if rtype == b'B1':
                meetinfo['name'] = record[2:47].decode('latin').strip()
                meetinfo['location'] = record[47:92].decode('latin').strip()
                meetinfo['startdate_str'] = record[92:100].decode('latin').strip()
                meetinfo['startdate'] = _mmddyyyy_date_to_iso_date(meetinfo['startdate_str'])
                meetinfo['enddate_str']   = record[100:108].decode('latin').strip()
                meetinfo['enddate'] = _mmddyyyy_date_to_iso_date(meetinfo['enddate_str'])
            elif rtype == b"C1":
                cur_team = {
                    "short_name":record[2:7].decode('latin').strip(),
                    "name":record[7:37].decode('latin').strip(),
                    "entries":[],
                    "swimmers":[],
                }
                teams.append(cur_team)
            elif rtype == b"D1":
                fname = record[28:48].decode('latin').strip()
                lname = record[8:28].decode('latin').strip()
                miname = record[68:69].decode('latin').strip()
                pfname = record[48:68].decode('latin').strip()
                swimmer_code = record[5:13].decode('latin').lower() # don't strip, padding is part of the key
                swimmer_gendercode = record[2:3].decode('latin')
                swimmer_id = record[69:81].decode('latin').strip()
                birthday_str = record[88:96].decode('latin')
                swimmer_age = record[97:99].decode('latin').strip()
                if swimmer_age == "":
                    swimmer_age = None
                else:
                    swimmer_age = int(swimmer_age,10)

                cur_swimmer = {"name":"{}, {}".format(lname,pfname if pfname else fname),
                    "lastname":lname,"firstname":fname,
                    "swimmer_code":swimmer_code,
                    "swimmer_id":swimmer_id,
                    "middlei":miname,
                    "birthday_str":birthday_str,
                    "birthday":_mmddyyyy_date_to_iso_date(birthday_str),
                    "age":swimmer_age,
                    "team_short_name":cur_team['short_name'],
                    "preferredname":pfname}
                cur_team['swimmers'].append(cur_swimmer)
            elif rtype == b'E1':
                strokecode = record[21:22].decode('latin')
                #print("stroke",HY3_STROKE_CODES[strokecode])
                distance = int(record[15:21].decode('latin'))
                event_gendercode = record[14:15].decode('latin')
                #print("distance",repr(record[67:71]))
                #print("event #",record[72:76])
                event_num_str = record[38:42].decode('latin').strip()
                try:
                    event_num = int(event_num_str,10)
                except ValueError:
                    #print("couldn't convert event_num, leaving as string",event_num_str)
                    event_num = None

                seed_coursecode = record[50:51].decode('latin').strip()
                if seed_coursecode in HY3_EVENT_COURSE_CODES:
                    seed_course = HY3_EVENT_COURSE_CODES[seed_coursecode]
                else:
                    seed_course = None

                #print("event #",event_num)
                # I'm not 100% sure this is the seed time field.
                # there are other time fields and I don't have a
                # good way to figure out which is what
                seed_time = record[42:50].decode('latin').strip()
                #print("possible seed time",seed_time)
                seed_time_ms = int(seed_time.replace('.',''),10)*10
                if seed_time_ms == 0:
                    seed_time_ms = None
                    seed_time = None

                cur_entry = {
                    "event":event_num,
                    "event_str":event_num_str,
                    "event_gendercode":event_gendercode,
                    "event_gender":HY3_EVENT_GENDER_CODES[event_gendercode] if event_gendercode in HY3_EVENT_GENDER_CODES else "Unknown",
                    "event_course":None,
                    "event_coursecode":None,
                    "heat":None,
                    "heat_number":None,
                    "lane":None,
                    "stroke":HY3_STROKE_CODES[strokecode],
                    "strokeshort":HY3_STROKE_CODES_SHORT[strokecode],
                    "distance":distance,
                    "seed_time":seed_time,
                    "seed_course":seed_course,
                    "seed_coursecode":seed_coursecode,
                    "seed_time_ms":seed_time_ms,
                    "seed_time_str":swimtimefmt(seed_time_ms),
                    "swimmer_codes":[cur_swimmer['swimmer_code']],
                    "relay":False,
                }
                cur_team['entries'].append(cur_entry)

            elif rtype == b'E2':

                event_type = record[2:3].decode('latin').strip()
                if event_type in HY3_EVENT_TYPE_CODES:
                    cur_entry['event_type'] = HY3_EVENT_TYPE_CODES[event_type]
                else:
                    cur_entry['event_type'] = None
                cur_entry['event_typecode'] = event_type
                cur_entry['heat'] = record[20:23].decode('latin').strip()
                cur_entry['heat_number'] = int(cur_entry['heat'],10)
                cur_entry['lane'] = record[23:26].decode('latin').strip()

                cur_entry['event_datestr'] = record[87:95].decode('latin').strip()
                cur_entry['event_date'] = _mmddyyyy_date_to_iso_date(cur_entry['event_datestr'])

                cur_entry['event_coursecode'] = record[11:12].decode('latin').strip()
                if cur_entry['event_coursecode'] in HY3_EVENT_COURSE_CODES:
                    cur_entry['event_course'] = HY3_EVENT_COURSE_CODES[cur_entry['event_coursecode']]
                else:
                    print("no course?",record)

                # results
                cur_entry['result_time'] = record[5:11].decode('latin').strip()
                if cur_entry['result_time'] == "" and cur_entry['result_time']!="0.00":
                    cur_entry['result_time'] = None
                    cur_entry['result_time_ms'] = None
                else:
                    cur_entry['result_time_ms'] = int(cur_entry['result_time'].replace('.',''),10)*10

                place = record[31:33].decode('latin').strip()
                if place == "":
                    cur_entry['place'] = None
                else:
                    cur_entry['place'] = int(place,10)
                
                #print("prelim heat #",record[124:126])
                #print("prelim lane #",record[126:128])
                #print("finals heat #",record[128:130])
                #print("finals lane #",record[130:132])
                #print(repr(record))

            elif rtype == b'F1':
                strokecode = record[21:22].decode('latin')
                #print("stroke",HY3_STROKE_CODES[strokecode])
                distance = int(record[15:21].decode('latin'))
                event_gendercode = record[14:15].decode('latin')
                #print("distance",repr(record[67:71]))
                #print("event #",record[72:76])
                relayname = record[2:11].decode('latin').strip()

                event_num_str = record[38:42].decode('latin').strip()
                try:
                    event_num = int(event_num_str,10)
                except ValueError:
                    #print("couldn't convert event_num, leaving as string",event_num_str)
                    event_num = None

                seed_coursecode = record[50:51].decode('latin').strip()
                if seed_coursecode in HY3_EVENT_COURSE_CODES:
                    seed_course = HY3_EVENT_COURSE_CODES[seed_coursecode]
                else:
                    seed_course = None

                # I'm not 100% sure this is the seed time field.
                # there are other time fields and I don't have a
                # good way to figure out which is what
                seed_time = record[42:50].decode('latin').strip()
                #print("possible seed time",seed_time)
                seed_time_ms = int(seed_time.replace('.',''),10)*10
                if seed_time_ms == 0:
                    seed_time_ms = None
                    seed_time = None

                cur_entry = {
                    "event":event_num,
                    "event_str":event_num_str,
                    "heat":None,
                    "heat_number":None,
                    "lane":None,
                    "event_gendercode":event_gendercode,
                    "event_gender":HY3_EVENT_GENDER_CODES[event_gendercode] if event_gendercode in HY3_EVENT_GENDER_CODES else "Unknown",
                    "event_course":None,
                    "event_coursecode":None,
                    "stroke":HY3_STROKE_CODES[strokecode],
                    "strokeshort":HY3_STROKE_CODES_SHORT[strokecode],
                    "distance":distance,
                    "seed_time":seed_time,
                    "seed_course":seed_course,
                    "seed_coursecode":seed_coursecode,
                    "seed_time_ms":seed_time_ms,
                    "seed_time_str":swimtimefmt(seed_time_ms),
                    "relay":True,
                    "teamname":relayname,
                    "swimmer_codes":[]
                }
                cur_team['entries'].append(cur_entry)

            elif rtype == b'F2':
                event_type = record[2:3].decode('latin').strip()
                if event_type in HY3_EVENT_TYPE_CODES:
                    cur_entry['event_type'] = HY3_EVENT_TYPE_CODES[event_type]
                else:
                    cur_entry['event_type'] = None
                cur_entry['event_typecode'] = event_type

                cur_entry['heat'] = record[20:23].decode('latin').strip()
                cur_entry['heat_number'] = int(cur_entry['heat'],10)
                cur_entry['lane'] = record[23:26].decode('latin').strip()
                #print(cur_entry['heat'])
                #print(cur_entry['lane'])

                cur_entry['event_datestr'] = record[102:110].decode('latin').strip()
                cur_entry['event_date'] = _mmddyyyy_date_to_iso_date(cur_entry['event_datestr'])
                
                cur_entry['event_coursecode'] = record[11:12].decode('latin').strip()
                if cur_entry['event_coursecode'] in HY3_EVENT_COURSE_CODES:
                    cur_entry['event_course'] = HY3_EVENT_COURSE_CODES[cur_entry['event_coursecode']]
                else:
                    print("no course?",record)

                # results
                cur_entry['result_time'] = record[5:11].decode('latin').strip()
                if cur_entry['result_time'] == "" and cur_entry['result_time']!="0.00":
                    cur_entry['result_time'] = None
                    cur_entry['result_time_ms'] = None
                else:
                    cur_entry['result_time_ms'] = int(cur_entry['result_time'].replace('.',''),10)*10

                place = record[31:33].decode('latin').strip()
                if place == "":
                    cur_entry['place'] = None
                else:
                    cur_entry['place'] = int(place,10)

            elif rtype == b'F3':
                # load swimmers
                swimmer1code = record[5:13].decode('latin').lower()
                swimmer2code = record[18:26].decode('latin').lower()
                swimmer3code = record[31:39].decode('latin').lower()
                swimmer4code = record[44:52].decode('latin').lower()
                cur_entry['swimmer_codes'] = [swimmer1code,swimmer2code,swimmer3code,swimmer4code]

            if rtype not in rtypes:
                rtypes[rtype]=0
            rtypes[rtype] = rtypes[rtype]+1
        except:
            print("exception on line",line)
            raise
    return meetinfo