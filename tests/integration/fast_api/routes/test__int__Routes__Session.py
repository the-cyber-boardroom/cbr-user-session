from unittest                                           import TestCase

from cbr_shared.cbr_backend.session.CBR__Session__Load import COOKIE_NAME__SESSION_ID
from cbr_shared.cbr_backend.session.Temp_DB_Session     import Temp_DB_Session
from cbr_user_session.fast_api.routes.Routes__Session   import Routes__Session
from osbot_fast_api.utils.Fast_API__Request import Fast_API__Request
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.utils.Objects                          import __
from tests.integration.user_session__objs_for_tests     import user_session__assert_local_stack


class test__int__Routes__Session(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()
        cls.routes_session = Routes__Session()

    def test_session_exists(self):
        session_id = Random_Guid()
        with Temp_DB_Session(session_id=session_id) as temp_session:
            with self.routes_session as _:
                assert _.session_exists(session_id) is True
                with Fast_API__Request().set_cookie(COOKIE_NAME__SESSION_ID,session_id) as request:
                    assert _.current_session(request) == temp_session.session_config().json()


    def test__behaviour_of__Temp_DB_Session(self):
        with self.routes_session as _:
            assert type(_)                  is Routes__Session
            assert _.__module__             == 'cbr_user_session.fast_api.routes.Routes__Session'

            with Temp_DB_Session() as temp_session:
                session_id = temp_session.session_id
                assert temp_session.exists() is True
                assert temp_session.obj() == __(session_id                     = session_id                     ,

                                                bucket_name__suffix            = 'server-data'                  ,
                                                bucket_name__prefix            = 'cyber-boardroom'              ,
                                                bucket_name__insert_account_id = True                           ,
                                                save_as_gz                     = False                          ,
                                                server_name                    ='unknown-server'                ,
                                                session_kwargs__s3             = __(service_name        = 's3' ,
                                                                                  aws_access_key_id     = None ,
                                                                                  aws_secret_access_key = None ,
                                                                                  endpoint_url          = None ,
                                                                                  region_name           = None ),
                                                use_minio                     = False                           )
            assert temp_session.exists() is False