from unittest                                       import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import __, dict_to_obj

from cbr_user_session.backend.guests.S3_DB__Guest   import S3_DB__Guest
from cbr_user_session.schemas.Model__Guest__Config import Model__Guest__Config
from tests.integration.user_session__objs_for_tests import user_session__assert_local_stack


class test_S3_DB__Guest(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()

    def setUp(self):
        self.db_guest = S3_DB__Guest()

    def test__init__(self):
        with self.db_guest as _:
            assert type(_) is S3_DB__Guest
            assert _.obj()  == __(guest_id                       = _.guest_id                        ,
                                  bucket_name__suffix            =   'server-data'                   ,
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

    def test_create(self):
        with self.db_guest as _:
            create_result = dict_to_obj(_.create())
            assert create_result                    == __(data    = __(guest__user_name = None                                  ,
                                                                       guest_id         = create_result.data.guest_id           ,
                                                                       timestamp        = create_result.data.timestamp          ),
                                                          error   = None                                                         ,
                                                          message = 'guest_user_created_ok'                                      ,
                                                          status  = 'ok'                                                         )
            assert _.s3_folder__guest_data__files() == ['guest-config.json']
            assert _.exists()                       is True
            assert _.delete()                       is True
            assert _.exists()                       is False
            assert _.s3_folder__guest_data__files() == []

    def test_exists(self):
        with self.db_guest as _:
            assert _.exists()  is False

    def test_guest_config__update(self):
        guest__user_name = 'some-name'
        with self.db_guest as _:
            assert _.exists() is False
            guest_config =  Model__Guest__Config(guest__user_name=guest__user_name)
            assert _.guest_config__update(guest_config) is True
            assert _.exists() is True
            assert guest_config.guest__user_name == guest__user_name
            assert guest_config.guest_id         == _.guest_id
            assert _.delete() is True

    def test_s3_folder__guest_data(self):
        with self.db_guest as _:
            assert _.s3_folder__guest_data() == f'{_.guest_id}'

    def test_s3_key__guest__config(self):
        with self.db_guest as _:
            assert _.s3_key__guest__config() == f'{_.guest_id}/guest-config.json'

    def test_s3_key__in__guest_folder(self):
        with self.db_guest as _:
            assert _.s3_key__in__guest_folder('file.txt') == f'{_.guest_id}/file.txt'