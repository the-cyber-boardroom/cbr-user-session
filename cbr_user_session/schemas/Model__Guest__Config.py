from dataclasses import dataclass

from osbot_utils.base_classes.Type_Safe     import Type_Safe
from osbot_utils.helpers.Random_Guid        import Random_Guid
from osbot_utils.helpers.Timestamp_Now      import Timestamp_Now


@dataclass
class Model__Guest__Config(Type_Safe):
    guest_id        : Random_Guid
    timestamp       : Timestamp_Now
    guest__user_name: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guest_id  = Random_Guid()
        self.timestamp = Timestamp_Now()