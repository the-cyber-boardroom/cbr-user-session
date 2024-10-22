from unittest                                      import TestCase
from cbr_user_session.backend.guests.Temp_DB_Guest import Temp_DB_Guest
from tests.integration.user_session__objs_for_tests import user_session__assert_local_stack, user_session__fast_api__client


class test__client__Routes__Guests(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()
        cls.client          = user_session__fast_api__client
        cls.db_guest        = Temp_DB_Guest().create()
        cls.guest_id        = cls.db_guest.guest_id

    @classmethod
    def tearDownClass(cls):
        assert cls.db_guest.delete() is True

    def test__guests__ids(self):
        response = self.client.get('/guests/ids')
        assert self.guest_id in response.json()

    def test__guests__data(self):
        response    = self.client.get('/guests/data')
        guests_data = response.json()
        assert guests_data[self.guest_id] == self.db_guest.guest_config().json()