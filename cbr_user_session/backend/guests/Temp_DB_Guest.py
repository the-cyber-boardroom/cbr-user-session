from cbr_user_session.backend.guests.S3_DB__Guest   import S3_DB__Guest
from cbr_user_session.schemas.Model__Guest__Config  import Model__Guest__Config
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from cbr_user_session.User_Session__Shared_Objects  import user_session__shared_objects
from osbot_utils.base_classes.Type_Safe             import Type_Safe

class Temp_DB_Guest(Type_Safe):
    guest_config: Model__Guest__Config

    @cache_on_self
    def db_guest(self):
        return user_session__shared_objects.db_guest()

    def __enter__(self) -> S3_DB__Guest:
        self.db_guest().create(guest_config=self.guest_config)
        return self.db_guest()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_guest().delete()
        pass

    def create(self):
        self.db_guest().create()
        return self.db_guest

    def delete(self):
        self.db_guest().delete()
        return self

    def exists(self):
        return self.db_guest().exists()