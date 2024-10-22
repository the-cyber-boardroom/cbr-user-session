from unittest                                           import TestCase
from cbr_shared.aws.s3.S3_DB_Base                       import S3_DB_Base
from cbr_shared.cbr_backend.cbr.S3_DB__CBR              import S3_DB__CBR
from osbot_aws.aws.s3.S3__DB_Base                       import S3__DB_Base
from cbr_user_session.User_Session__Shared_Objects      import user_session__shared_objects
from cbr_user_session.backend.guests.Temp_DB_Guest      import Temp_DB_Guest
from osbot_utils.base_classes.Type_Safe                 import Type_Safe
from osbot_utils.utils.Objects                          import __, base_types
from cbr_user_session.backend.guests.S3_DB__Guests      import S3_DB__Guests
from tests.integration.user_session__objs_for_tests     import user_session__assert_local_stack


class test_S3_DB__Guests(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()
        cls.db_guests = user_session__shared_objects.db_guests()

    def test_setUpClass(self):
        with self.db_guests  as _:
            assert type(_)              is S3_DB__Guests
            assert base_types(_)        == [S3_DB__CBR, S3_DB_Base, S3__DB_Base, Type_Safe, object]              # todo: S3_DB_Base, S3__DB_Base need refactoring since that is a legacy situation)
            assert _.obj()              == __(bucket_name__suffix            =   'server-data'                   ,
                                              bucket_name__prefix            =   'cyber-boardroom'               ,
                                              bucket_name__insert_account_id = True                              ,
                                              save_as_gz                     = False                             ,
                                              server_name                    = 'unknown-server'                  ,
                                              session_kwargs__s3             = __(service_name          ='s3'    ,
                                                                                  aws_access_key_id     = None  ,
                                                                                  aws_secret_access_key = None  ,
                                                                                  endpoint_url          = None  ,
                                                                                  region_name           = None  ),
                                              use_minio                      = False                             )
            assert _.s3_bucket()        == 'cyber-boardroom-000011110000-server-data'
            assert _.s3_folder_guests() == 'guests'

    def test_db_guests_data(self):
        with self.db_guests as _:
            with Temp_DB_Guest() as guest_1:
                guests_data = _.db_guests_data()
                assert guests_data[guest_1.guest_id] == guest_1.guest_config().json()

    def test_db_guests_ids(self):
        with self.db_guests as _:
            with Temp_DB_Guest() as guest_1:
                assert guest_1.guest_id in _.db_guests_ids()


