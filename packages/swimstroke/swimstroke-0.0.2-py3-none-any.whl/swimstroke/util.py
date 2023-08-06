def swimtimefmt(time_ms):
    if time_ms is None:
        return ""
    elif time_ms>=60000:
        return "%d:%02d.%02d"%(time_ms//60000, (time_ms//1000)%60, ((time_ms//10)%100))
    else:
        return "%d.%02d"%(time_ms//1000, ((time_ms//10)%100))

def swimtime_strtoms(time_str):
    if time_str is None or len(time_str)==0: return None
    if ':' in time_str:
        minutes, rest = time_str.split(':')
    else:
        minutes = "0"
        rest = time_str
    seconds, hundreths = rest.split(".")
    return int(minutes,10)*60000 + int(seconds,10)*1000 + int(hundreths,10)*10