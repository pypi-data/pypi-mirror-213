import boto3
from platinumtools.aws_classes.class_enhancement import *
from platinumtools.dda_constants import *


# Configure the AWS credentials and region
# aws_access_key_id = 'YOUR_ACCESS_KEY'
# aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
# aws_region = 'us-east-1'

# # Create an SQS client
# sqs = boto3.client('sqs', region_name=aws_region,
#                     aws_access_key_id=aws_access_key_id,
#                     aws_secret_access_key=aws_secret_access_key)

sqs = boto3.client('sqs')

# Define the URL of your SQS queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/796522278827/MockQueue.fifo'



def processFromJobParameter(job_parameters):
    
    organizationDBProvider = MockOrganizationQuerier

    
    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }

    settings = {
        "TABLENAME": "event",
        "GET_TABLENAME": "staging_events",
         "COLUMN_NAMES": [
                        "user_guid",
                        "timestamp_utc",
                        "application",
                        "operation",
                        "event_guid",
                        "organization_guid",
                        "staging_guid",
                        "source_type",
                        "connector_guid",
                        "version",
                        "organization_id",
                        "user_id",
                        "user_team_id",
                        "profile_id",
                        "user_timezone",
                        "timestamp_client_local",
                        "month_number",
                        "month_name",
                        "weekday_number",
                        "weekday_name",
                        "day",
                        "hour",
                        "minute",
                        "time_slot",
                        "week_number",
                        "date",
                        "operation_type",
                        "application_type",
                        "interface_type",
                        "work_hour_type",
                        "raw_details",
                        "start_time",
                        "end_time",
                        "duration",
                        "description",
                        "title",
                        "url",
                        "attachments",
                        "action_origin",
                        "span_guid",
                        "root_reference",
                        "root_start",
                        "root_end",
                        "root_duration"
                        ]

    }
    publishingDBProvider = PostgreSQLProvider(credentials=credentials, settings=settings)

    processor = BetterCommonProcessor(
        job_parameters=job_parameters,
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
    ) 
    processor.runJobs() # Should also post at the Mock Database


# Receive and process SQS messages
def process_messages():
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,  # Maximum number of messages to retrieve
            WaitTimeSeconds=5  # Wait time for new messages in the queue
        )
        
        if 'Messages' in response:
            for message in response['Messages']:
                # And here you should start calling it => Making sure that the received message is a valid job => Having the received message as a dict.
                # Then what you want to to do is that once you receive the message, then you want to have the max number of messages here.

                job_parameter =  {"guid": message['Body'] }
                # print("Job parameter created: ", job_parameter, " from message: ", job_parameter[EVENT_GUID])
                processFromJobParameter(job_parameter)

                # Delete then the message from the queue.     
                # Delete the message from the queue
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        else:
            print('No messages in the queue.')


# Call the function to start processing messages
process_messages()
