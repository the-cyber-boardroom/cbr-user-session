from unittest                                       import TestCase
from cbr_user_session.backend.guests.S3_DB__Guest   import S3_DB__Guest
from cbr_user_session.fast_api.routes.Routes__Guest import Routes__Guest
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
        cls.routes_guest    = Routes__Guest()

    @classmethod
    def tearDownClass(cls):
        assert cls.db_guest.delete() is True

    def test__setUpClass(self):
        assert self.db_guest.exists() is True
        assert self.routes_guest.data(self.guest_id).get('status') == 'ok'

    def test__guests__create(self):
        guest_name  = 'an-guest-name'
        path__create  = f'/guest/create?guest_name={guest_name}'
        guest_config  = str_to_obj(self.client.get(path__create))
        user_id       = guest_config.user_id
        session_id    = guest_config.session_id
        guest_id      = guest_config.guest_id

        assert guest_config.guest_name == guest_name
        db_guest   = S3_DB__Guest(guest_id=guest_id)
        db_user    = db_guest.db_user()
        db_session = db_guest.db_session()

        assert db_guest  .exists()   is True
        assert db_user   .exists()   is True
        assert db_session.exists()   is True
        assert db_guest.guest_id     == guest_id
        assert db_user.user_id       == user_id
        assert db_session.session_id == session_id

        path__exists      = f'/guest/exists?guest_id={guest_id}'
        path__delete      = f'/guest/delete?guest_id={guest_id}'
        exists_response_1 = str_to_obj(self.client.get(path__exists))
        delete_response_1 = str_to_obj(self.client.get(path__delete))
        exists_response_2 = str_to_obj(self.client.get(path__exists))
        delete_response_2 = str_to_obj(self.client.get(path__delete))
        assert exists_response_1.message == 'Guest exists'
        assert delete_response_1.message == 'Guest deleted ok'
        assert exists_response_2.message == f'Guest with id {guest_id} not found'
        assert delete_response_2.message == f'Error deleting guest with id: {guest_id}'



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
