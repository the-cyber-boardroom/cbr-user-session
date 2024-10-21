from unittest import TestCase

from cbr_shared.cbr_backend.session.Temp_DB_Session     import Temp_DB_Session
from cbr_user_session.fast_api.routes.Routes__Session   import Routes__Session
from osbot_utils.utils.Objects                          import __
from tests.integration.user_session__objs_for_tests     import user_session__assert_local_stack


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

            with Temp_DB_Session() as temp_session:
                session_id = temp_session.session_id

                assert temp_session.exists() is True

                # Option 1: normal JSON layout
                assert temp_session.json() == { 'bucket_name__insert_account_id': True,
                                                'bucket_name__prefix': 'cyber-boardroom',
                                                'bucket_name__suffix': 'server-data',
                                                'save_as_gz': False,
                                                'server_name': 'unknown-server',
                                                'session_id': session_id,
                                                'session_kwargs__s3': { 'aws_access_key_id': None,
                                                                        'aws_secret_access_key': None,
                                                                        'endpoint_url': None,
                                                                        'region_name': None,
                                                                        'service_name': 's3'},
                                                'use_minio': False}

                # Option 2: with Json formating and alignment
                assert temp_session.json() == { 'bucket_name__insert_account_id': True                              ,
                                                'bucket_name__prefix'           : 'cyber-boardroom'                 ,
                                                'bucket_name__suffix'           : 'server-data'                     ,
                                                'save_as_gz'                    : False                             ,
                                                'server_name'                   : 'unknown-server'                  ,
                                                'session_id'                    : session_id                        ,
                                                'session_kwargs__s3'            : { 'aws_access_key_id'     : None ,
                                                                                    'aws_secret_access_key' : None ,
                                                                                    'endpoint_url'          : None ,
                                                                                    'region_name'           : None ,
                                                                                    'service_name'          : 's3' },
                                                'use_minio'                     : False                             }

                # Option 3 with Obj() data formating and alignment (with __ == SimpleNamespace)
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