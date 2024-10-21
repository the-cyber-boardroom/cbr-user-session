from osbot_utils.base_classes.Type_Safe import Type_Safe

from cbr_user_session.backend.guests.S3_DB__Guest import S3_DB__Guest


class Temp_DB_Guest(Type_Safe):
    db_guest : S3_DB__Guest

    def __enter__(self):
        return self.create()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()
        pass

    def create(self):
        self.db_guest.create()
        return self.db_guest

    def delete(self):
        self.db_guest.delete()
        return self

    def exists(self):
        return self.db_guest.exists()