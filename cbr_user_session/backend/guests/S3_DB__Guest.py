import logging

from cbr_shared.cbr_backend.cbr.S3_DB__CBR          import S3_DB__CBR
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid                import Random_Guid
from osbot_utils.utils.Http                         import url_join_safe
from osbot_utils.utils.Status                       import status_ok
from cbr_user_session.schemas.Model__Guest__Config  import Model__Guest__Config

FILE_NAME__GUEST_CONFIG = "guest-config.json"

class S3_DB__Guest(S3_DB__CBR):
    guest_id : Random_Guid

    def create(self, guest_config: Model__Guest__Config = None):
        if guest_config is None:
            guest_config = Model__Guest__Config()
        self.guest_config__update(guest_config)
        if self.exists():
            return status_ok(message="guest_user_created_ok", data=guest_config.json())

    def delete(self):
        s3_key_user_files = [self.s3_key__guest__config()]
        self.s3_files_delete(s3_key_user_files)
        return self.s3_folder__guest_data__files() == []                  # this will confirm that everything has been deleted

    def exists(self):
        return self.s3_file_exists(self.s3_key__guest__config())

    def guest_config__update(self, guest_config: Model__Guest__Config):
        if type(guest_config) is Model__Guest__Config:
            guest_config.guest_id = self.guest_id                       # make sure these always match
            return self.s3_save_data(data=guest_config.json(), s3_key=self.s3_key__guest__config())
        raise ValueError("guest_config data needs to be of type Model__Guest__Config")

    # s3 key generation

    def s3_folder__guest_data(self):
        return self.guest_id

    def s3_folder__guest_data__files(self):
        return self.s3_folder_files(self.s3_folder__guest_data())

    def s3_key__guest__config(self):
        return self.s3_key__in__guest_folder(FILE_NAME__GUEST_CONFIG)



    def s3_key__in__guest_folder(self, file_name):
        return url_join_safe(self.s3_folder__guest_data(), file_name)


