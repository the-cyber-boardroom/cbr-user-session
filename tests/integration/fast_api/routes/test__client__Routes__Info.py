from unittest                                       import TestCase
from osbot_utils.utils.Objects                      import dict_to_obj, __
from cbr_user_session.utils.Version                 import version__cbr_user_session
from tests.integration.user_session__objs_for_tests import user_session__fast_api__client, user_session__assert_local_stack

class test__client__Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()
        cls.client = user_session__fast_api__client

    def test__info__db_session(self):
        response     = self.client.get('/info/db-session')
        response_obj = dict_to_obj(response.json())
        assert response.status_code == 200
        assert response_obj         == __(bucket_exists = True                                      ,
                                          bucket_name   = 'cyber-boardroom-000011110000-server-data',
                                          local_stack   = True                                      ,
                                          session_count = response_obj.session_count                )


    def test__info__ping(self):
        response = self.client.get('/info/ping')
        assert response.status_code == 200
        assert response.json() == {"pong": "42"}

    def test__info__version(self):
        response = self.client.get('/info/version')
        assert response.status_code == 200
        assert response.json() == {"version": version__cbr_user_session}

