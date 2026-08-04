import re
def timestamp_to_seconds(timestamp : str):
    h, m, s = map(int, timestamp.split(":"))
    return h * 3600 + m * 60 + s

def seconds_to_timestamp(seconds: float) -> str:
    total = int(seconds)

    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60

    return f"{h:02}:{m:02}:{s:02}"


