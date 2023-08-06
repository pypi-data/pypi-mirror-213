from typing import List
import datetime
from dateutil import parser, tz
from platinumtools.dda_constants import *
from platinumtools.dda_models import *
from platinumtools.aws_classes.class_enhancement import *


def eventDataIntoTimeSlots(eventData: dict, limit_minutes_per_slot=10) -> List[Timeslot]:
    """
    Split the events into time slots based on the next 10th multiple of minutes.

    Args:
        eventData (dict): Event data dictionary.
        limit_minutes_per_slot (int, optional): The maximum time in minutes to split the events into. Defaults to 10.

    Returns:
        List[Timeslot]: A list of Timeslot events.
    """
    timeslots_res = []
    timeslots_event_data = []
    duration = eventData["duration"]

    if duration is not None and duration > 0:
        start_time = parser.parse(eventData["timestamp"]).astimezone(tz.UTC)
        end_time = parser.parse(eventData["end_time"]).astimezone(tz.UTC)

        while start_time < end_time:
            next_multiple_of_limit = datetime.datetime(
                start_time.year, start_time.month, start_time.day,
                start_time.hour, start_time.minute + limit_minutes_per_slot - (start_time.minute % limit_minutes_per_slot),
                tzinfo=tz.UTC
            )

            current_endtime = min(next_multiple_of_limit, end_time)

            eventDataCopy = eventData.copy()
            eventDataCopy["timestamp"] = start_time.isoformat()
            eventDataCopy["end_time"] = current_endtime.isoformat()
            timeslots_event_data.append(eventDataCopy)

            start_time = current_endtime

    if len(timeslots_event_data) > 0:
        date_formatted_events_data = Utils.date_related_population(timeslots_event_data)

        for timeslot_event_data in date_formatted_events_data:
            timeslot_event_data["event_guid"] = eventData["guid"]
            timeslot = Timeslot.from_dict(timeslot_event_data).to_dict()
            timeslots_res.append(timeslot)

    return timeslots_res
