from cbr_user_session.backend.guests.S3_DB__Guest   import S3_DB__Guest
from cbr_user_session.backend.guests.S3_DB__Guests  import S3_DB__Guests
from osbot_utils.base_classes.Type_Safe             import Type_Safe


class User_Session__Shared_Objects(Type_Safe):

    def db_guests(self) -> S3_DB__Guests:
        with S3_DB__Guests() as _:
            _.setup()
            return _

    def db_guest(self) -> S3_DB__Guest:
        with S3_DB__Guest() as _:
            _.setup()
            return _

user_session__shared_objects = User_Session__Shared_Objects()