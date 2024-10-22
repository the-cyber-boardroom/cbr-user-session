from cbr_shared.cbr_backend.cbr.S3_DB__CBR          import S3_DB__CBR
from cbr_user_session.backend.guests.S3_DB__Guest   import S3_DB__Guest

class S3_DB__Guests(S3_DB__CBR):

    def db_guest(self, guest_id):
        return S3_DB__Guest(guest_id=guest_id)

    def db_guests(self):
        for session_id in self.db_guests_ids():
            yield self.db_guest(session_id)

    def db_guests_data(self):
        all_data = {}
        for db_guest in self.db_guests():
            all_data[db_guest.guest_id] = db_guest.guest_config().json()
        return all_data

    def db_guests_ids(self):
        return self.s3_folder_list(folder=self.s3_folder_guests())


