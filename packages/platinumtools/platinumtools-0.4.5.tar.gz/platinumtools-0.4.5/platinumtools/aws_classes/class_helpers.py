from abc import ABC, abstractmethod
from typing import List
from platinumtools.dda_constants import *
from platinumtools.dda_models import *
import json, random, string

from pytz import timezone
import math, datetime, pytz
from dateutil import parser, tz
import json
from typing import List

# awsconfig_mapper import ConfigMapper



class DatabaseProvider(ABC):
    def __init__(self, credentials, settings):
        self.credentials = credentials
        self.settings = settings
        

    @abstractmethod
    def publish(self, events: List[dict]):
        print("publishing to database:", events)

    @abstractmethod
    def getOne(self, key_value, key_column: str = "guid", table_name: str = "events"):
        print("Getting source with: ", key_value, "in", key_column, "column")

class MockDatabaseProvider(DatabaseProvider):
    """Prints publishing and getters, using for debugging, also returns static examples
    Records the json for quick edition and visualization in a local file.
    """
    def __init__(self, credentials, settings):
        super().__init__(credentials, settings)
        self.db = []

    def publish(self, events: List[dict], table_name="mock_db.json"):
        self.db.extend(events)

        # Save as .. code-block:: json
        
        with open(table_name, "w") as f:
            f.write(json.dumps(self.db, indent=4))

        return super().publish(events=events)

    def getOne(self, key_value, key_column: str = "guid"):
        super().getOne(key_column)
        try:
            for(i, row) in enumerate(self.db):
                if row[key_column] == key_value:
                    return row
            return []
        except Exception as e:
            # print("key column", key_column, " : ", key_value, "not found")
            # print("Exception:", e)
            # print("self.db", len(self.db))
            for(i, row) in enumerate(self.db):
                print(i, row['guid'])
            return []


class MockStagingDatabaseProviderPrePopulated(MockDatabaseProvider):
    def __init__(self, credentials, settings):
        super().__init__(credentials, settings)
        self.db = STAGING_EVENTS_SAMPLE



class MockStagingDatabaseProviderWithChrome(MockDatabaseProvider):
    """Extension Mock Staging Database of rthe Config mapper to work better with Chrome
    """
    def __init__(self, credentials, settings):
        super().__init__(credentials, settings)
        self.db = STAGING_EVENTS_SAMPLE_WITH_CHROME


import psycopg2
    
class PostgreSQLProvider(DatabaseProvider):
    """Publishes into PostgreSQL as key and expects a body column to be published as  
    """

    def __init__(self, credentials, settings):
        """Initiates with the database credentials, and settings as the specfici tables it is looking for
        Requires:
            pandas
            psycopg2

        Args:
            credentials (dict): Credentails for database {USERNAME, PASSWORD, HOST, DB}
            settings (dict): {TABLE}
        """
        super().__init__(credentials, settings)
        # Initiate SQl connection
        self.connection = psycopg2.connect(user=credentials['USERNAME'], password=credentials['PASSWORD'], host=credentials['HOST'], database=credentials['DB'])
        self.cursor = self.connection.cursor()

    def fetchFromElse(self, fetchFrom: dict, key, elseGets):
        """Fetches value from dictionary otherwise it gets:

        Args:
            fetchFrom (dict): _description_
            key (_type_): _description_
            elseGets (_type_): _description_

        Returns:
            _type_: _description_
        """
        if key in fetchFrom:
            return fetchFrom[key]
        return elseGets
    
    def publish(self, events: List[dict], table_name="mock_db.json"):
        """Publishes
        Expected parameters to have unders settings:
        - TABLENAME
        - COLUMN_NAMES
    
        Args:
            events (List[dict]): List of events to publish.
        """

        # Fetches the proper credentials based on the environemnt


        # Update Settings"
        tablename_events= self.settings.get("TABLENAME_EVENTS", "events")
        column_names_events = self.settings.get("COLUMN_NAMES_EVENTS", [])

        tablename_timeslot = self.settings.get("TABLENAME_TIMESLOT", "timeslot")
        column_names_timeslot = self.settings.get("COLUMN_NAMES_TIMESLOT", [])
        


        # Pushes the changes into SQL
        insert_sql = f"INSERT INTO {tablename_events} ({', '.join(column_names_events)}) VALUES ({', '.join(['%s'] * len(column_names_events))})"
        # # print("Created insert_SQL:", insert_sql)
        # Execute the INSERT statement for each dictionary in the list
        # print("attepting to get rows from events:", events)

        import json
        from typing import List

        def cleanQueryArgument(queryArgument):
            # If the queryArg is a list or dict, format it into a way that is query insertable
            if isinstance(queryArgument, (dict)):
                # If the is List and the first element is a dict, then it is a list of objects
                return json.dumps(queryArgument)
            if isinstance(queryArgument, List) and len(queryArgument) >0 and isinstance(queryArgument[0], dict):
                # return an array of strings of the json
                for(i, item) in enumerate(queryArgument):
                    queryArgument[i] = cleanQueryArgument(item)
            
            return queryArgument

        for row in events:
            values = []
            for col in column_names_events:
                value = row.get(col, None)
                values.append(cleanQueryArgument(value))
            try:
                self.cursor.execute(insert_sql, values)
            except Exception as e:
                print("Exception at publish:", e, "values:", values)
        self.connection.commit()

    
    def getOne(self, key_value, key_column: str = "guid"):
        """Gets one
        Expected parameters to have under settings:
        - TABLENAME

        Args:
            source_id (str): _description_
        """
        # Get table name and other settings properties
        
        tablename= self.fetchFromElse(self.settings, "GET_TABLENAME", "event")
        row_dict = {}
        # Gets one of the sources
        self.cursor.execute(f"SELECT * FROM {tablename} WHERE {key_column} = '{key_value}'")

        row = self.cursor.fetchone()
        if row:
            row_dict = dict(zip([desc[0] for desc in self.cursor.description], row))
            # print(row_dict)
        else:
            print("No rows found")
        return row_dict

class PostgreSQLProviderTimeSlotPlusEventsPublishing(PostgreSQLProvider):
    """This improvement overwrites simple PostgreSQLProvider to be
     both Timeslot and also events to be published on publish time.
    """

    def __init__(self, credentials, settings):
        """Initiates with the database credentials, and settings as the specfici tables it is looking for
        Requires:
            pandas
            psycopg2

        Args:
            credentials (dict): Credentails for database {USERNAME, PASSWORD, HOST, DB}
            settings (dict): {TABLE}
        """
        super().__init__(credentials, settings)
        


        
    def publish(self, events: dict["events": List[dict], "timeslot": List[dict]], table_name=""):
        """Publishes
        Expected parameters to have unders settings:
        - TABLENAME
        - COLUMN_NAMES
    
        Args:
            events (List[dict]): List of events to publish.
        """

        # Fetches the proper credentials based on the environemnt


        # Update Settings"
        tablename_events= self.settings.get("TABLENAME_EVENTS", "events")
        column_names_events = self.settings.get("COLUMN_NAMES_EVENTS", [])

        tablename_timeslot = self.settings.get("TABLENAME_TIMESLOTS", "timeslot")
        column_names_timeslot = self.settings.get("COLUMN_NAMES_TIMESLOTS", [])

        self.publish_to(events["events"], column_names_events, tablename_events)
        self.publish_to(events["timeslots"], column_names_timeslot, tablename_timeslot)


    def publish_to(self, events: List[dict], column_names: List[str], tablename: str):
        """Publishes into the postgresdatabase the timeslot and events
        @param events: List of events to publish.
        @param column_names: List of column names to publish        
    
        Args:
            events (List[dict]): List of events to publish.
        """


        # Pushes the changes into SQL
        insert_sql = f"INSERT INTO {tablename} ({', '.join(column_names)}) VALUES ({', '.join(['%s'] * len(column_names))})"
        
        def cleanQueryArgument(queryArgument):
            # If the queryArg is a list or dict, format it into a way that is query insertable
            if isinstance(queryArgument, (dict)):
                # If the is List and the first element is a dict, then it is a list of objects
                return json.dumps(queryArgument)
            if isinstance(queryArgument, List) and len(queryArgument) >0 and isinstance(queryArgument[0], dict):
                # return an array of strings of the json
                for(i, item) in enumerate(queryArgument):
                    queryArgument[i] = cleanQueryArgument(item)
            
            return queryArgument

        for row in events:
            values = []
            for col in column_names:
                value = row.get(col, None)
                values.append(cleanQueryArgument(value))
            try:
                self.cursor.execute(insert_sql, values)
            except Exception as e:
                
                print("publishing to "+ tablename +"; received the following events:", events)
                # print("attributes timeslot:", Timeslot.get_attribute_keys())
                print("Insert sql created:", insert_sql)
                print("Exception at publish:", e, "values:", values)
        self.connection.commit()

       
class Utils:
    """Some random utitlities
    Requirements:
    - json
    """
    
    def date_related_population(join_events: List[dict]) -> List[dict]:
        """
        For each of the events, populate the date-related items.
        """
        for event in join_events:
            # Convert timestamp to datetime object
            timestamp: datetime.datetime = parser.parse(event['timestamp']).replace(tzinfo=pytz.utc)
            timezone_str: str = event['user_timezone']
            local_timestamp: datetime.datetime = timestamp.astimezone(timezone(timezone_str))
            event['timestamp_local'] = local_timestamp.isoformat()
            event["local_timezone"] = timezone_str

            # Extract timeslot
            timeslot = (local_timestamp.hour * 60 + local_timestamp.minute) // 10
            event['timeslot'] = timeslot
            event['timeslot_local'] = (timeslot + 6) % 24

            # Extract UTC date and time components
            event['hour'] = timestamp.hour
            event['minute'] = timestamp.minute
            event['day'] = timestamp.day
            event['month'] = timestamp.month
            event['year'] = timestamp.year
            event['week'] = timestamp.isocalendar()[1]
            event['weekday'] = timestamp.weekday()

            # Extract local date and time components
            event['hour_local'] = local_timestamp.hour
            event['minute_local'] = local_timestamp.minute
            event['day_local'] = local_timestamp.day
            event['month_local'] = local_timestamp.month
            event['year_local'] = local_timestamp.year
            event['week_local'] = local_timestamp.isocalendar()[1]
            event['weekday_local'] = local_timestamp.weekday()

            # Check if end_time is None
            if event['end_time'] is not None:
                # Convert end_time to datetime object
                endtime = parser.parse(event['end_time'])

                # Convert timestamp and end_time to the specified timezone
                local_endtime = endtime.astimezone(timezone(timezone_str))

                # Populate the timestamp_local, end_time_local, and duration fields as isoformat strings
                event['end_time_local'] = local_endtime.isoformat()
                event['duration'] = (endtime - timestamp).total_seconds() / 3600
            else:
                # If end_time is None, set the remaining fields to None as well
                event['end_time'] = None
                event['end_time_local'] = None
                event['duration'] = 0

        return join_events


    def createRandomStr(length:int  = 10):
        """Generates random string with the length indicated

        Args:
            length (int, optional): length of the random string. Defaults to 10.
        """
        # Generate a random string
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return random_string

    def escapedStrToListOfObjects(escapedStr: str):
        """Escapes String that might appear on the database or queries into a list of objects or dict

        Args:
            escapedStr (str): escaped String

        Returns:
            List: List of objects/or dict
            
        '[         {\"name\": \"Alice\", \"age\": 25, \"gender\": \"F\"},         {\"name\": \"Bob\", \"age\": 30, \"gender\": \"M\"},         {\"name\": \"Charlie\", \"age\": 35, \"gender\": \"M\"}     ]'
        ->
        [{'name': 'Alice', 'age': 25, 'gender': 'F'}, {'name': 'Bob', 'age': 30, 'gender': 'M'}, {'name': 'Charlie', 'age': 35, 'gender': 'M'}]
        """
        try:
            escapedStr = escapedStr.strip()
            return json.loads(escapedStr)
        except Exception as e:
            return []

    def NoneSafe(dictItem:dict, key:string, default=None):
        """Safely gets the value from the dictionary, if it does not exist, it returns the default

        Args:
            dictItem (dict): dictionary to get the value from
            key (string): key to get the value from
            default (string): default value to return if the key does not exist

        Returns:
            str: Value that is returned safely
        """
        # return dictItem.get(key, default)
        if key in dictItem:
            try:
                return dictItem[key]
            except Exception as e:
                # print("Exception at NoneSafe:", e
                #       , "dictItem:", type(dictItem) ,dictItem, 
                #       "key:",  type(key),key)
                pass
        return default
    
    

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


class OrganizationalQuerier(ABC):
    def __init__(self, organization_id):
        self.organization_id = organization_id
        
    def getCredential(organization_id: str, service: str):
        """Gets organization identification. 

        Args:
            organization_id (str): 
            service (str): gets ervices
        """
        pass

    def getEmployeesDenormalized(organization_id: str):
        """Gets all of the employees data in the organization

        Args:
            organization_id (str): organization string
        """
        

        pass
    def getEmployeeDenormalized(user_id: str):
        """Gets the data of the employee based on th

        Args:
            user_id (str): id of th employee which data we want to denormalize
        """
        pass

    def getEmployeeDataWhere(key: str, value: str):
        """Gets the employee data where the key is equal to the value

        Args:
            key (str): key to be searched
            value (str): value to be searched

        Returns:
            dict: employee data
        """
        return {}
    
    def isRootOrUpdateRoot(span_guid: str, event_endtime: str, event_duration: int) -> dict:
        """If the event is root returns {is_root: true, total_duration = current_duration, root_reference: span_guid}
        Otherwise: {is_root: false, total_duration = current_duration + root_duration, root_reference: root_guid}

        Args:
            span_guid (str): guid of the group span
            event_endtime (datetime): endtime of the event request
            event_duration (number): duration in seconds 

        Returns:
            dict: {is_root: bool, total_duration: number, root_reference: str}
        """
        return {}
    
    def getOrganizationParameters_salesforce(organization_id: str):
        """Gets the organization parameters for salesforce

        Args:
            organization_id (str): organization id

        Returns:
            dict: organization parameters
        """
        return {}
    
    def getOrganizationParametersByOrganizationID(organization_id: str):
        """Gets the organization parameters by organization id

        Args:
            organization_id (str): organization id

        Returns:
            dict: organization parameters
        """
        return {}
    
    def getOrganizationParametersByOrganizationGuid(organization_guid: str):
        """Gets the organization parameters by organization guid

        Args:
            organization_guid (str): organization guid

        Returns:
            dict: organization parameters
        """
        return {}
    
    def getOrganizationParameters_connectorguid(organization_name: str):
        """Gets the organization parameters by organization name

        Args:
            organization_name (str): organization name

        Returns:
            dict: organization parameters
        """
        return {}

# Sample profile of an employee, that is just used by default.

sample_profile_user_1 = {
            "organization_id": 1,
            "user_guid": "ab3c-asd1-100G",
            "user_id": 1,
            "user_team_id": [1, 2],
            "profile_id": [1],
            "user_timezone": "US/Eastern",
            "user_time_slot_split": 6,
            "user_work_hours_start": [9, 10, 11, 9, 9, 0, 0],
            "user_work_days": [0, 1, 2, 3, 4],
            "user_work_hours_end": [17, 18, 19, 17, 17, 0, 0],
            "user_escape_dates": ["2022-04-15", "2022-06-10"],
            "profile_mapping_instruction": {"instruction1": "value1", "instruction2": "value2"}
    }

sample_profile_user_2 =  {
                "organization_id": 1,
                "user_id": 2,
                "user_team_id": [1],
                "user_guid": "ab3c-asd1-561a",
                "profile_id": [1, 2],
                "user_timezone": "Asia/Tokyo",
                "user_time_slot_split": 6,
                "user_work_hours_start": [9, 10, 11, 9, 9, 0, 0],
                "user_work_days": [0, 1, 2, 3, 4],
                "user_work_hours_end": [17, 18, 19, 17, 17, 0, 0],
                "user_escape_dates": ["2022-03-01", "2022-09-01"],
                "profile_mapping_instruction": {"instruction5": "value5", "instruction6": "value6"}
            }

class MockOrganizationQuerier(OrganizationalQuerier):
    
    

    def __init__(self, organization_id):
        """
        Doesn't intiialize the database because that has been provided will be there for all.
        """

        super().__init__(organization_id)

    def getCredential(organization_id: str, service: str):
        return super().getCredential(service)
        
    def getEmployeesDenormalized(self, organization_id: str):
        return super().getEmployeesDenormalized(organization_id)

    def getOrganizationParametersByOrganizationID(organization_id: int) -> List[dict]:
        sample_organizatin_parameters = [
            sample_profile_user_1,
           sample_profile_user_2
        ]
        return sample_organizatin_parameters
    
    def getOrganizationParametersBYOrganizationGUID(organization_guid: str) -> List[dict]:
        sample_organizatin_parameters = [
            sample_profile_user_1,
           sample_profile_user_2
        ]
        return sample_organizatin_parameters

    def getOrganizationParameters_365(orgnaization_guid_365: str) -> List[dict]:
        # Here it returns as the O365 id first as the main key.

        sample_organization_parameters_365_formatted = {
        "organization_id": "8de4e5d3-49de-4b57-a209-organization",
            "nelson@o365.devcooks.com": sample_profile_user_1,
            "apolo@o365.devcooks.com": sample_profile_user_1
        }
        return sample_organization_parameters_365_formatted

    def getOrganizationParameters_salesforce(orgnaization_guid_salesforce: str) -> List[dict]:

        """Salesforce frmatted means, that it would return you with the salesforce actor id as the key.

        Returns:
            dict: It should return you the organization parameters for salesforce example.
        """

        sample_organization_parameters_salesforce_formatted = {
        "organization_id": "123e4567-e89b-12d3-a456-client",
         "nwang@platinumfilings.com": sample_profile_user_1
        }
        return sample_organization_parameters_salesforce_formatted

    def getOrganizationParameters_connectorguid(organization_guid_chrome: str) -> List[dict]:
        # Shows the connector guid first, such as chrome-extension-ddap-1 used for chome extension.
        
        return {"organization_guid": organization_guid_chrome, "user_profile": sample_profile_user_1}

    def getEmployeeDataWhere(key: str, value: str):
        """Gets the employee data where the key is equal to the value

        Args:
            key (str): key to be searched
            value (str): value to be searched

        Returns:
            dict: employee data
        """
        result_employee = sample_profile_user_1.copy()
        result_employee.key = value
        return result_employee

    def isRootOrUpdateRoot(span_guid: str, event_endtime: str, event_duration: int) -> dict:
        """If the event is root returns {is_root: false, total_duration = current_duration, root_reference: span_guid}
        Otherwise: {is_root: true, total_duration = current_duration + root_duration, root_reference: root_guid}

        Args:
            span_guid (str): guid of the group span
            event_endtime (datetime): endtime of the event request
            event_duration (number): duration in seconds 

        Returns:
            dict: {is_root: bool, total_duration: number, root_reference: str}
        """
        root_guid = {
            "ab3c-asd1-100G":
            {
                "span_guid": "ab3c-asd1-100G",
                "root_guid": "ab3c-asd1-100G",
                "root_duration": 25,
                "root_endtime": "2021-08-01T00:00:00Z"
            },
            "ab3c-asd1-123g":            
            {
                "span_guid": "ab3c-asd1-123g",
                "root_guid": "ab3c-asd1-123g",
                "root_duration": 11,
                "root_endtime": "2021-08-01T00:00:00Z"
            }
        }

        if span_guid in root_guid:
            
            root_guid[span_guid]["root_duration"] += event_duration
            root_guid[span_guid]["root_endtime"] = event_endtime

            return {
                "is_root": False,
                "total_duration": root_guid[span_guid]["root_duration"],
                "root_reference": span_guid
            }

        else:
            return {
                "is_root": True,
                "total_duration": event_duration,
                "root_reference": span_guid
            }


    