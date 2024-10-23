from unittest                                           import TestCase
from cbr_shared.cbr_backend.session.Temp_DB_Session     import Temp_DB_Session
from cbr_user_session.user_session.User_Session__Utils  import User_Session__Utils
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from tests.integration.user_session__objs_for_tests     import user_session__assert_local_stack


class test_User_Session__Utils(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()
        cls.user_session_utils = User_Session__Utils()

    def setUp(self):
        self.session_id = Random_Guid()

    def test_session_exists(self):
        with self.user_session_utils as _:
            result = _.session__exists('session_id')
            assert result is False

            with Temp_DB_Session(session_id=self.session_id):
                result = _.session__exists(self.session_id)
                assert result is True