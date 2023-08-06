"""
2023-06-09 15:42:41 
Testing the splitting algorithm
"""

import unittest
from platinumtools.aws_classes.class_helpers import Utils

class EventDataIntoTimeSlotsTests(unittest.TestCase):

    def test_eventDataIntoTimeSlots(self):
        eventData = {
            "guid": "460bcde5-adce-42e1-85de-1411a69e280b",
            "user_id": 1,
            "application": "CHROME",
            "app": "mazzzystar.github.io",
            "operation": "download",
            "event_guid": "0adeb6d2-c889-4592-0b46-e43e887e4d71",
            "platform_id": 2,
            "organization_id": 1,
            "user_timezone": "US/Eastern",
            "timestamp": "2023-05-11T16:03:31.434Z",
            "end_time": "2023-05-11T16:13:31.427Z",
            "timestamp_local": "2023-05-11T12:03:31.434000-04:00",
            "end_time_local": "2023-05-11T12:13:31.427000-04:00",
            "duration": 600000,
            "title": "The Leverage of LLMs for Individuals | TL;DR",
            "url": "https://mazzzystar.github.io/images/2023-05-10/superCLUE.jpg",
            "site": "mazzzystar.github.io",
            "url_domain": "mazzzystar.github.io",
            "file_count": 0,
            "action_type": "PASSIVE",
            "staging_guid": "0adeb6d2-c889-4592-0b46-e43e887e4d71",
            "mouse_clicks": 13,
            "keystrokes": 10,
            "size": 0
        }

        expected_timeslots = [
            {
                'event_guid': '460bcde5-adce-42e1-85de-1411a69e280b', 
                'timeslot': 72, 
                'timeslot_local': 6, 
                'hour': 16, 
                'minute': 3, 
                'day': 11, 
                'month': 5, 
                'year': 2023, 
                'week': 19, 
                'weekday': 3, 
                'hour_local': 12, 
                'minute_local': 3, 
                'day_local': 11, 
                'month_local': 5, 
                'year_local': 2023, 
                'week_local': 19, 
                'weekday_local': 3, 
                'mouse_clicks': 13, 
                'staging_guid': '0adeb6d2-c889-4592-0b46-e43e887e4d71', 
                'keystrokes': 10
            }, 
            {
                'event_guid': '460bcde5-adce-42e1-85de-1411a69e280b', 
                'timeslot': 73, 
                'timeslot_local': 7, 
                'hour': 16, 
                'minute': 10, 
                'day': 11, 
                'month': 5, 
                'year': 2023, 
                'week': 19, 
                'weekday': 3, 
                'hour_local': 12, 
                'minute_local': 10, 
                'day_local': 11, 
                'month_local': 5, 
                'year_local': 2023, 
                'week_local': 19, 
                'weekday_local': 3, 
                'mouse_clicks': 13, 
                'staging_guid': '0adeb6d2-c889-4592-0b46-e43e887e4d71', 
                'keystrokes': 10
            }
        ]

        # Call the method to get the actual timeslots
        actual_timeslots = Utils.eventDataIntoTimeSlots(eventData, limit_minutes_per_slot=10)

        print(actual_timeslots)
        # Assert that the actual timeslots match the expected timeslots
        # What's important in this case is to have them splitted as the following:

        # 1. 2023-05-11T16:03
        # 2. 2023-05-11T16:10

        # Which has a cutoff there

        self.assertEqual(actual_timeslots, expected_timeslots)






