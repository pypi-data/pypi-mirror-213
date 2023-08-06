import pytest
from platinumtools.aws_classes.class_enhancement import *
from platinumtools.dda_constants import *




# def common_processor_using_mock():

#     publisher_credentials = {}
#     publisher_settings = {}

#     organizationDBProvider = MockOrganizationQuerier
#     publishingDBProvider = MockStagingDatabaseProviderWithChrome(credentials=publisher_credentials, settings=publisher_settings)
#     processor = BetterCommonProcessor(
#         job_parameters={"guid": "387a26ff-ceed-5015-a6c9-a2cad90329c0" },
#         organization_provider=organizationDBProvider,
#         publishingDBProvider=publishingDBProvider
#     ) # Should expect for transformation Strategies to be automatically updated

#     return processor

# # def test_picks_chrome_enhancement_instantiation(common_processor_using_mock):
# #     processor = common_processor_using_mock
# #     processor.runJobs() # Should also post at the Mock Database


# def test_picks_salesforce_enhancement():
    
#     organizationDBProvider = MockOrganizationQuerier
#     publishingDBProvider = MockStagingDatabaseProviderWithChrome(credentials={}, settings={})
#     processor = BetterCommonProcessor(
#         job_parameters={"guid": "f27ecb0c-975d-dbac-82af-152b68e89902" },
#         organization_provider=organizationDBProvider,
#         publishingDBProvider=publishingDBProvider
#     ) # Should expect for transformation Strategies to be automatically updated
    
#     processor.runJobs() # Should also post at the Mock Database


def test_picks_real_job():
    
    organizationDBProvider = MockOrganizationQuerier
    
    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }

    settings = {
        "GET_TABLENAME": "staging_events",
        "TABLENAME_EVENTS": "event",
        "COLUMN_NAMES_EVENTS": Event.get_attribute_keys(),
        "TABLENAME_TIMESLOTS": "timeslot",
        "COLUMN_NAMES_TIMESLOTS": Timeslot.get_attribute_keys()
    }
    publishingDBProvider = PostgreSQLProviderTimeSlotPlusEventsPublishing(credentials=credentials, settings=settings)
    mockingDBProvide = MockDatabaseProvider(credentials=credentials, settings=settings)

    processor = ConnecToGUIDHarcodedDictBasedCommonProcessor(
        job_parameters={"guid": "387a26ff-ceed-5015-a6c9-afa"},
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
        # publishingDBProvider=mockingDBProvide
    ) 
    
    processor.runJobs() # Should also post at the Mock Database