from osbot_utils.utils.Status                       import status_ok, status_error
from cbr_user_session.schemas.Model__Guest__Config  import Model__Guest__Config
from osbot_utils.utils.Str                          import str_safe
from cbr_shared.cbr_backend.cbr.S3_DB__CBR          import S3_DB__CBR
from cbr_user_session.backend.guests.S3_DB__Guest   import S3_DB__Guest

class S3_DB__Guests(S3_DB__CBR):

    def db_guest(self, guest_id):
        return S3_DB__Guest(guest_id=guest_id)

    def db_guest__create(self, guest_name):
        try:
            guest_name   = str_safe(guest_name)
            db_guest     = S3_DB__Guest()
            guest_config =  Model__Guest__Config(guest__name=guest_name)
            if db_guest.create(guest_config):
                return status_ok(data=db_guest.guest_config())
            return status_error(f"Error creating guest with name: {guest_name}")
        except Exception as error:
            return status_error(f"Error in creating guest: {error}")

    def db_guests(self):
        for session_id in self.db_guests__ids():
            yield self.db_guest(session_id)

    def db_guests__data(self):
        all_data = {}
        for db_guest in self.db_guests():
            all_data[db_guest.guest_id] = db_guest.guest_config().json()
        return all_data

    def db_guests__delete(self):
        deleted_guests = []
        for db_guest in self.db_guests():
            db_guest.delete()
            deleted_guests.append(db_guest.guest_id)
        return deleted_guests

    def db_guests__ids(self):
        return self.s3_folder_list(folder=self.s3_folder_guests())


