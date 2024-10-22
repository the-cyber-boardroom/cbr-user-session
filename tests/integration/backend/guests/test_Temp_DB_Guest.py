from unittest                                       import TestCase
from cbr_shared.cbr_backend.cbr.S3_DB__CBR          import S3_FOLDER__GUESTS
from cbr_user_session.backend.guests.S3_DB__Guest   import FILE_NAME__GUEST_CONFIG, S3_DB__Guest
from cbr_user_session.schemas.Model__Guest__Config  import Model__Guest__Config
from cbr_user_session.backend.guests.Temp_DB_Guest  import Temp_DB_Guest
from tests.integration.user_session__objs_for_tests import user_session__assert_local_stack


class test_Temp_DB_Guest(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()

    def test__enter__exit(self):
        guest_config = Model__Guest__Config(guest__name='some-name')
        with Temp_DB_Guest(guest_config=guest_config) as _:
            assert type(_)                   is S3_DB__Guest
            assert _.exists()                is True
            assert _.guest_config().obj()    == guest_config.obj()
            assert _.s3_key__guest__config() == f'{S3_FOLDER__GUESTS}/{_.guest_id}/{FILE_NAME__GUEST_CONFIG}'

        assert _.exists() is False