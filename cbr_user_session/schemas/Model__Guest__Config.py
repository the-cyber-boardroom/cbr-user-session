from dataclasses                        import dataclass
from osbot_utils.utils.Misc             import random_text, timestamp_to_str_date, timestamp_to_str_time
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Timestamp_Now  import Timestamp_Now

@dataclass
class Model__Guest__Config(Type_Safe):
    created__date   : str               = None
    created__time   : str               = None
    timestamp       : Timestamp_Now     = None
    guest__name     : str               = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.guest__name is None:
            self.guest__name = random_text('guest', lowercase=True, length=5)
        if self.timestamp        is None:
            self.timestamp        = Timestamp_Now()
        self.created__date = timestamp_to_str_date(self.timestamp)
        self.created__time = timestamp_to_str_time(self.timestamp)

