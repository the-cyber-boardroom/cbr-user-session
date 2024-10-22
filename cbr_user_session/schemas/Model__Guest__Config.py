from dataclasses import dataclass
from osbot_utils.base_classes.Type_Safe     import Type_Safe
from osbot_utils.helpers.Timestamp_Now      import Timestamp_Now


@dataclass
class Model__Guest__Config(Type_Safe):
    timestamp       : Timestamp_Now     = None
    guest__user_name: str               = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.timestamp is None:
            self.timestamp = Timestamp_Now()