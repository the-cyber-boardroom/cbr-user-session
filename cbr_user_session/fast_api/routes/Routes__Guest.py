from starlette.responses import JSONResponse

from cbr_shared.cbr_backend.session.CBR__Session__Load  import COOKIE_NAME__SESSION_ID
from cbr_shared.cbr_sites.CBR__Shared_Objects           import cbr_shared_objects
from osbot_fast_api.api.Fast_API_Routes                 import Fast_API_Routes
from osbot_utils.utils.Status                           import status_ok, status_error
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self

STATUS_OK__LOGGED_IN_AS_USER                    = f"Found guest, set {COOKIE_NAME__SESSION_ID} cookie to session id, so that user is now logged in as the provided guest id"
STATUS_ERROR__FOUND_GUEST_BUT_NO_ACTIVE_SESSION = "Found guest, but there was not active session available"
STATUS_ERROR__GUEST_NOT_FOUND                   = f"Guest not found"

class Routes__Guest(Fast_API_Routes):
    tag : str = 'guest'

    @cache_on_self
    def db_guests(self):
        return cbr_shared_objects.db_guests()

    def create(self, guest_name:str=None):
        return self.db_guests().db_guest__create(guest_name)

    def data(self, guest_id:str):
        try:
            db_guest = self.db_guests().db_guest(guest_id)
            if db_guest.exists():
                return status_ok(data=db_guest.guest_data())
            else:
                return status_error(f"Guest with id {guest_id} not found")
        except Exception as error:
            return status_error(f"Error in data: {error}")

    def delete(self, guest_id:str):
        db_guest = self.db_guests().db_guest(guest_id)
        if db_guest.exists():
            if db_guest.delete():
                return status_ok("Guest deleted ok")
        return status_error(f"Error deleting guest with id: {guest_id}")


    def exists(self, guest_id:str):
        db_guest = self.db_guests().db_guest(guest_id)
        if db_guest.exists():
            return status_ok("Guest exists")
        else:
            return status_error(f"Guest with id {guest_id} not found")

    def login_as_guest(self, guest_id):
        db_guest = self.db_guests().db_guest(guest_id)
        if db_guest.exists():
            db_session = db_guest.db_session()
            if db_session.exists():
                cookie_name    = COOKIE_NAME__SESSION_ID
                cookie_value   = db_session.session_id
                json_response = JSONResponse(content=status_ok(message=STATUS_OK__LOGGED_IN_AS_USER))
                json_response.set_cookie(key=cookie_name, value=cookie_value, httponly=True)
                return json_response
            return status_error(STATUS_ERROR__FOUND_GUEST_BUT_NO_ACTIVE_SESSION)
        else:
            return status_error(STATUS_ERROR__GUEST_NOT_FOUND)

    def setup_routes(self):
        self.add_route_get(self.create           )
        self.add_route_get(self.data             )
        self.add_route_get(self.delete           )
        self.add_route_get(self.exists           )
        self.add_route_get(self.login_as_guest   )
        return self