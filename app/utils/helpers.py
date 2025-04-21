from datetime import datetime

def timestampToISOFormat(timestamp):
    if isinstance(timestamp, datetime):
        return timestamp.isoformat()
    return timestamp