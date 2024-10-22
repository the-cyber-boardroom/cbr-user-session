from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes
from osbot_utils.utils.Status                       import status_ok, status_error
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from cbr_user_session.User_Session__Shared_Objects  import user_session__shared_objects


class Routes__Guest(Fast_API_Routes):
    tag : str = 'guest'

    @cache_on_self
    def db_guests(self):
        return user_session__shared_objects.db_guests()

    def data(self, guest_id:str):
        try:
            db_guest = self.db_guests().db_guest(guest_id)
            if db_guest.exists():
                return status_ok(data=db_guest.guest_config())
            else:
                return status_error(f"Guest with id {guest_id} not found")
        except Exception as error:
            return status_error(f"Error in data: {error}")

    def ids(self):
        return self.db_guests().db_guests_ids()

    def setup_routes(self):
        self.add_route_get(self.data)
        return self