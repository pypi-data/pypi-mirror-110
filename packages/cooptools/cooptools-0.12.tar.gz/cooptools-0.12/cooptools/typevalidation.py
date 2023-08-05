import dateutil
import datetime
import pandas as pd

def float_as_currency(val: float):
    return "${:,.2f}".format(round(val, 2))


def int_tryParse(value):
    try:
        return int(value)
    except:
        return None


def date_tryParse(value):
    if type(value) == datetime.date:
        return value
    if type(value) == datetime.datetime:
        return value.date()
    if type(value) == pd.Timestamp:
        return value.to_pydatetime().date()


    try:
        casted = dateutil.parser.parse(value)
        return casted.date()
    except Exception as e:
        raise TypeError(f"Value {value} cannot be converted to a valid date. {e}")


def datestamp_tryParse(value, include_time: bool = True, include_ms: bool = True):
    try:
        if type(value) == str:
            date_stamp = dateutil.parser.parse(value)
        elif type(value) in [datetime.datetime, datetime.date]:
            date_stamp = value
        else:
            raise NotImplementedError(f"Unhandled type [{type(value)}] for datestamp parsing")


        if not include_time:
            date_stamp = datetime.datetime.combine(date_stamp, datetime.datetime.min.time())

        if not include_ms:
            date_stamp = date_stamp.replace(microsecond=0)

        return date_stamp
    except:
        return None
