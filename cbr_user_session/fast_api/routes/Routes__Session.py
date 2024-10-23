from cbr_user_session.user_session.User_Session__Utils  import User_Session__Utils
from osbot_fast_api.api.Fast_API_Routes                 import Fast_API_Routes



class Routes__Session(Fast_API_Routes):
    tag                : str                 = 'session'
    user_session_utils : User_Session__Utils

    def session_details(self, session_id):
        return self.user_session_utils.session__details(session_id)

    def session_exists(self, session_id):
        return self.user_session_utils.session__exists(session_id)

    def session_user_id(self, session_id):
        return self.user_session_utils.session__user_id(session_id)

    def setup_routes(self):
        self.add_route_get(self.session_details)
        self.add_route_get(self.session_exists)
        self.add_route_get(self.session_user_id)