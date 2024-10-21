from unittest import TestCase

from cbr_user_session.fast_api.routes.Routes__Session import Routes__Session
from osbot_utils.utils.Dev import pprint
from tests.integration.user_session__objs_for_tests import user_session__assert_local_stack


class test__int__Routes__Session(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()
        cls.routes_session = Routes__Session()

    def test_session_exists(self):
        with self.routes_session as _:
            assert type(_)                  is Routes__Session
            assert _.__module__             == 'cbr_user_session.fast_api.routes.Routes__Session'
            assert _.session_exists('123')  is False