from unittest                                       import TestCase
from osbot_utils.utils.Objects                      import __, str_to_obj
from osbot_utils.helpers.Random_Guid                import Random_Guid
from cbr_user_session.backend.guests.Temp_DB_Guest  import Temp_DB_Guest
from cbr_user_session.schemas.Model__Guest__Config  import Model__Guest__Config
from tests.integration.user_session__objs_for_tests import user_session__assert_local_stack, user_session__fast_api__client

class test__client__Routes__Guest(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()
        cls.client          = user_session__fast_api__client
        cls.db_guest        = Temp_DB_Guest().create()
        cls.guest_id        = cls.db_guest.guest_id

    @classmethod
    def tearDownClass(cls):
        assert cls.db_guest.delete() is True

    def test__guests__data(self):
        path               = f'/guest/data?guest_id={self.guest_id}'
        response           = self.client.get(path).json()
        response__status   = response.get('status')
        response__data     = response.get('data')
        guest_config       = Model__Guest__Config.from_json(response__data)
        assert response__status == 'ok'
        assert guest_config   == self.db_guest.guest_config()
        assert response__data == self.db_guest.guest_config().json()

    def test__guests__data___bad_data(self):
        path               = '/guest/data?guest_id=NOT-A-GUID'
        message_1          = "Error in data: in Random_Guid: value provided was not a Guid: NOT-A-GUID"
        response_1         = str_to_obj(self.client.get(path))
        assert response_1 == __(data=None, error=None, message = message_1, status='error')

        an_guid            = Random_Guid()
        path               = f'/guest/data?guest_id={an_guid}'
        message_2          = f"Guest with id {an_guid} not found"
        response_2         = str_to_obj(self.client.get(path))
        assert response_2 == __(data=None, error=None, message = message_2, status='error')
