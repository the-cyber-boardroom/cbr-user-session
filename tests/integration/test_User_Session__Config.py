from unittest                                           import TestCase
from osbot_aws.AWS_Config                               import aws_config, ENV_NAME__AWS_ACCOUNT_ID
from osbot_aws.testing.Temp__Random__AWS_Credentials    import Temp_AWS_Credentials
from osbot_utils.utils.Env                              import del_env, get_env, set_env
from osbot_utils.utils.Objects                          import __
from cbr_user_session.User_Session__Config              import USER_SESSION__DEFAULT__AWS_ACCOUNT_ID, User_Session__Config, user_session__config, ENV_NAME__USER_SESSION__USE_LOCAL_STACK
from tests.integration.user_session__objs_for_tests     import user_session__assert_local_stack


class test_User_Session__Config(TestCase):

    @classmethod
    def setUpClass(cls):
        user_session__assert_local_stack()

    def test_setup__edge_cases(self):
        user_session_config__before     = user_session__config.obj()
        use_local_stack_env__before     = get_env(ENV_NAME__USER_SESSION__USE_LOCAL_STACK)
        assert aws_config.account_id() == USER_SESSION__DEFAULT__AWS_ACCOUNT_ID

        with Temp_AWS_Credentials():
            aws_account_id      = 'abcd1234'
            user_session_config = User_Session__Config(aws_account_id=aws_account_id)

            assert aws_config.account_id()     != USER_SESSION__DEFAULT__AWS_ACCOUNT_ID
            assert user_session_config.obj()   == __(aws_account_id='abcd1234', use_local_stack=False)

            del_env(ENV_NAME__AWS_ACCOUNT_ID               )
            del_env(ENV_NAME__USER_SESSION__USE_LOCAL_STACK)
            assert user_session_config.setup() is user_session_config
            assert user_session_config.obj()   == __(aws_account_id='abcd1234', use_local_stack=False)

            assert user_session_config.reset()
            assert user_session_config.obj()   == __(aws_account_id=USER_SESSION__DEFAULT__AWS_ACCOUNT_ID, use_local_stack=False)

        assert aws_config.account_id()     == USER_SESSION__DEFAULT__AWS_ACCOUNT_ID
        assert user_session_config__before == user_session__config.obj()
        set_env(ENV_NAME__USER_SESSION__USE_LOCAL_STACK, use_local_stack_env__before)
