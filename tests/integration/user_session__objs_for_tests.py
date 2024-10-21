from cbr_user_session.fast_api.User_Session__Fast_API import User_Session__Fast_API
from osbot_aws.testing.Temp__Random__AWS_Credentials import Temp_AWS_Credentials
from osbot_utils.utils.Env                           import set_env
from osbot_local_stack.local_stack.Local_Stack       import Local_Stack
from osbot_utils.context_managers.capture_duration   import capture_duration

CBR_SESSION__TEST__AWS_ACCOUNT_ID        = '000011110000'

def setup_env_vars():
    Temp_AWS_Credentials().set_vars()
    set_env('AWS_ACCOUNT_ID'  , CBR_SESSION__TEST__AWS_ACCOUNT_ID) # todo: move this to the Temp_AWS_Credentials class

with capture_duration() as duration:
    setup_env_vars()
    fast_api__local_stack           = Local_Stack().activate()
    user_session__fast_api          = User_Session__Fast_API().setup()
    user_session__fast_api__app     = user_session__fast_api.app()
    user_session__fast_api__client  = user_session__fast_api.client()

assert duration.seconds < 1         # make sure the setup time is less than 1 second

def user_session__assert_local_stack():
    assert fast_api__local_stack.is_local_stack_configured_and_available() is True