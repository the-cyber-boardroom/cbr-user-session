from unittest                                               import TestCase
from cbr_shared.cbr_backend.guests.S3_DB__Guest             import S3_DB__Guest
from cbr_shared.cbr_backend.guests.Temp_DB_Guest            import Temp_DB_Guest
from cbr_shared.cbr_sites.CBR__Shared__Constants            import COOKIE_NAME__CBR__SESSION_ID__USER, COOKIE_NAME__CBR__SESSION_ID__PERSONA, COOKIE_NAME__CBR__SESSION_ID__ACTIVE
from cbr_shared.schemas.data_models.Model__Guest__Config    import Model__Guest__Config
from cbr_user_session.fast_api.routes.Routes__Guest         import Routes__Guest, STATUS_OK__LOGGED_IN_AS_USER, STATUS_OK__LOGGED_IN_AS_PERSONA, STATUS_OK__LOGGED_OUT_ALL, STATUS_OK__LOGGED_OUT_GUEST, STATUS_OK__LOGGED_OUT_PERSONA
from osbot_utils.utils.Http                                 import parse_cookies
from osbot_utils.utils.Objects                              import __, str_to_obj
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from osbot_utils.utils.Status                               import status_ok
from tests.integration.user_session__objs_for_tests         import user_session__assert_local_stack, user_session__fast_api__client

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

    def test__guest__create(self):
        guest_name  = 'an-guest-name'
        path__create  = f'/guest/create?guest_name={guest_name}'
        guest_config  = str_to_obj(self.client.post(path__create))
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
        exists_response_1 = str_to_obj(self.client.get   (path__exists))
        delete_response_1 = str_to_obj(self.client.delete(path__delete))
        exists_response_2 = str_to_obj(self.client.get   (path__exists))
        delete_response_2 = str_to_obj(self.client.delete(path__delete))
        assert exists_response_1.message == 'Guest exists'
        assert delete_response_1.message == 'Guest deleted ok'
        assert exists_response_2.message == f'Guest with id {guest_id} not found'
        assert delete_response_2.message == f'Error deleting guest with id: {guest_id}'



    def test__guest__data(self):
        path               = f'/guest/data?guest_id={self.guest_id}'
        response           = self.client.get(path).json()
        response__status   = response.get('status')
        response__data     = response.get('data')
        guest_config       = Model__Guest__Config.from_json(response__data)
        assert response__status      == 'ok'
        assert guest_config.guest_id == self.guest_id

    def test__guest__data___bad_data(self):
        path               = '/guest/data?guest_id=NOT-A-GUID'
        message_1          = "Error in data: in Random_Guid: value provided was not a Guid: NOT-A-GUID"
        response_1         = str_to_obj(self.client.get(path))
        assert response_1 == __(data=None, error=None, message = message_1, status='error')

        an_guid            = Random_Guid()
        path               = f'/guest/data?guest_id={an_guid}'
        message_2          = f"Guest with id {an_guid} not found"
        response_2         = str_to_obj(self.client.get(path))
        assert response_2 == __(data=None, error=None, message = message_2, status='error')

    def test__guest__login_as_guest(self):
        session_id  = self.db_guest.db_session__id()
        path        = f'/guest/login-as-guest?guest_id={self.guest_id}'
        response  = self.client.post(path)
        assert response.json() == status_ok(message=STATUS_OK__LOGGED_IN_AS_USER)
        assert response.headers.get('set-cookie') == (f"{COOKIE_NAME__CBR__SESSION_ID__USER  }={session_id}; Path=/;, "
                                                      f"{COOKIE_NAME__CBR__SESSION_ID__ACTIVE}={session_id}; Path=/;")

    def test__guest__login_as_persona(self):
        session_id  = self.db_guest.db_session__id()
        path        = f'/guest/login-as-persona?persona_id={self.guest_id}'
        response  = self.client.post(path)
        assert response.json() == status_ok(message=STATUS_OK__LOGGED_IN_AS_PERSONA)
        assert response.headers.get('set-cookie') == (f"{COOKIE_NAME__CBR__SESSION_ID__PERSONA}={session_id}; Path=/;, "
                                                      f"{COOKIE_NAME__CBR__SESSION_ID__ACTIVE }={session_id}; Path=/;")


    # Add these new test methods to the test__client__Routes__Guest class:
    def test__guest__logout_all(self):
        # First login as both guest and persona
        response_1              = self.client.post(f'/guest/login-as-guest?guest_id={self.guest_id}')
        response_2              = self.client.post(f'/guest/login-as-persona?persona_id={self.guest_id}')
        cbr_session_id_user     = response_1.headers.get('cbr-session-id-user'   )
        cbr_session_id_persona  = response_2.headers.get('cbr-session-id-persona')
        response_1__set_cookie  = response_1.headers.get('set-cookie').replace(';,', ';')
        response_2__set_cookie  = response_2.headers.get('set-cookie').replace(';,', ';') # hack so that parse_cookies is able to recognise the cookies

        cookies_1              = parse_cookies(response_1__set_cookie, include_empty=False)
        cookies_2              = parse_cookies(response_2__set_cookie, include_empty=False)

        assert cbr_session_id_user    == self.db_guest.db_session__id()
        assert cbr_session_id_persona == self.db_guest.db_session__id()


        assert cookies_1 == { COOKIE_NAME__CBR__SESSION_ID__ACTIVE : { 'httponly': False                  ,
                                                                       'path'    : '/'                   ,
                                                                       'secure'  : False                 ,
                                                                       'value'   : cbr_session_id_user   },
                              COOKIE_NAME__CBR__SESSION_ID__USER   : { 'httponly': False                  ,
                                                                       'path'    : '/'                   ,
                                                                       'secure'  : False                 ,
                                                                       'value'   : cbr_session_id_user   }}

        assert cookies_2 == { COOKIE_NAME__CBR__SESSION_ID__ACTIVE : { 'httponly': False                  ,
                                                                       'path'    : '/'                    ,
                                                                       'secure'  : False                  ,
                                                                       'value'   : cbr_session_id_persona},
                              COOKIE_NAME__CBR__SESSION_ID__PERSONA: { 'httponly': False                  ,
                                                                       'path'    : '/'                    ,
                                                                       'secure'  : False                  ,
                                                                       'value'   : cbr_session_id_persona }}
        # Then logout all
        path       = '/guest/logout-all'
        response_3 = self.client.post(path)
        assert response_3.json() == status_ok(message=STATUS_OK__LOGGED_OUT_ALL)

        # Check that all cookies are deleted
        response_3__set_cookie = response_3.headers.get('set-cookie').replace(';,', ';')
        cookies                = parse_cookies(response_3__set_cookie, include_empty=False)
        assert cookies == { COOKIE_NAME__CBR__SESSION_ID__ACTIVE  : { 'httponly': False                                                            ,
                                                                      'max-age' : '0'                                                              ,
                                                                      'path'    : '/'                                                              ,
                                                                      'secure'  : False                                                            ,
                                                                      'value'   : ''                                                               },
                            COOKIE_NAME__CBR__SESSION_ID__PERSONA : { 'httponly': False                                                            ,
                                                                      'max-age' : '0'                                                              ,
                                                                      'path'    : '/'                                                              ,
                                                                      'secure'  : False                                                            ,
                                                                      'value'   : ''                                                               },
                            COOKIE_NAME__CBR__SESSION_ID__USER    : { 'httponly': False                                                            ,
                                                                      'max-age' : '0'                                                              ,
                                                                      'path'    : '/'                                                              ,
                                                                      'secure'  : False                                                            ,
                                                                      'value'   : ''                                                               }}


    def test__guest__logout_guest(self):
        # First login as guest
        self.client.get(f'/guest/login-as-guest?guest_id={self.guest_id}')

        # Then logout guest
        path = '/guest/logout-guest'
        response = self.client.post(path)

        assert response.json() == status_ok(message=STATUS_OK__LOGGED_OUT_GUEST)

        # Check that only guest cookie is deleted
        cookies = parse_cookies(response.headers.get('set-cookie'),include_empty=False)
        expires = cookies.get(COOKIE_NAME__CBR__SESSION_ID__USER).get('expires')
        assert cookies == { COOKIE_NAME__CBR__SESSION_ID__USER: { 'expires' : expires,
                                                                  'httponly': False  ,
                                                                  'max-age' : '0'    ,
                                                                  'path'    : '/'    ,
                                                                  'samesite': 'lax'  ,
                                                                  'secure'  : False  ,
                                                                  'value'   : ''     }}

    def test__guest__logout_persona(self):
        # First login as persona
        self.client.get(f'/guest/login-as-persona?persona_id={self.guest_id}')

        # Then logout persona
        path = '/guest/logout-persona'
        response = self.client.post(path)

        assert response.json() == status_ok(message=STATUS_OK__LOGGED_OUT_PERSONA)

        # Check that only persona cookie is deleted
        cookies = parse_cookies(response.headers.get('set-cookie'),include_empty=False)
        expires = cookies.get(COOKIE_NAME__CBR__SESSION_ID__PERSONA).get('expires')
        assert cookies == { COOKIE_NAME__CBR__SESSION_ID__PERSONA: { 'expires' : expires,
                                                                     'httponly': False  ,
                                                                     'max-age' : '0'    ,
                                                                     'path'    : '/'    ,
                                                                     'samesite': 'lax'  ,
                                                                     'secure'  : False  ,
                                                                     'value'   : ''     }}


