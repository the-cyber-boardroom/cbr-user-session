from unittest                                       import TestCase
from cbr_shared.cbr_backend.users.DB_User           import DB_User
from cbr_shared.cbr_backend.session.DB_Session      import DB_Session
from cbr_user_session.User_Session__Shared_Objects  import user_session__shared_objects
from cbr_user_session.backend.guests.Temp_DB_Guest  import Temp_DB_Guest
from osbot_utils.utils.Objects                      import __
from cbr_user_session.backend.guests.S3_DB__Guest   import S3_DB__Guest
from tests.integration.user_session__objs_for_tests import user_session__assert_local_stack


class test_S3_DB__Guest(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()

    def setUp(self):
        self.db_guests   = user_session__shared_objects.db_guests()
        self.db_guest    = self.db_guests.db_guest()
        self.db_guest_id = self.db_guest.guest_id

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

    def test_db_session(self):
        with Temp_DB_Guest() as _:
            assert type(_.db_session()) is DB_Session
            assert type(_.db_user   ()) is DB_User

            assert _             .exists() is True
            assert _.db_session().exists() is True
            assert _.db_user   ().exists() is True

        assert _             .exists() is False
        assert _.db_session().exists() is False
        assert _.db_user   ().exists() is False

        # pprint(_          .s3_folder_files__all())
        # pprint(_.db_user().s3_folder_files__all())
        # _.bucket_delete_all_files()
        # _.db_user().bucket_delete_all_files()


    def test_create(self):
      with self.db_guest as _:
        assert _.create()                       is True                         # create guest

        assert _.s3_folder__guest_data__files()  == ['guest-config.json']
        assert _.exists()                        is True
        assert _.db_user   ().exists()           is True
        assert _.db_session().exists()           is True
        assert _.guest_config().guest_id         == _.guest_id
        assert _.guest_config().user_id          == _.db_user().user_id
        assert _.guest_config().session_id       == _.db_session().session_id

        assert _.delete()                        is True                     # delete guest
        assert _.delete()                        is False
        assert _.exists()                        is False
        assert _.db_user   ().exists()           is False
        assert _.db_session().exists()           is False
        assert _.s3_folder__guest_data__files()  == []
        assert _.guest_config(reload_cache=True) is None

    def test_exists(self):
        with self.db_guest as _:
            assert _.exists()  is False

    def test_s3_folder__guest_data(self):
        with self.db_guest as _:
            assert _.s3_folder__guest_data() == f'guests/{_.guest_id}'

    def test_s3_key__guest__config(self):
        with self.db_guest as _:
            assert _.s3_key__guest__config() == f'guests/{_.guest_id}/guest-config.json'

    def test_s3_key__in__guest_folder(self):
        with self.db_guest as _:
            assert _.s3_key__in__guest_folder('file.txt') == f'guests/{_.guest_id}/file.txt'