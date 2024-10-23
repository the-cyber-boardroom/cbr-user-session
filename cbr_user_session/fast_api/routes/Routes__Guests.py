from cbr_shared.cbr_sites.CBR__Shared_Objects       import cbr_shared_objects
from osbot_fast_api.api.Fast_API_Routes             import Fast_API_Routes
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self

class Routes__Guests(Fast_API_Routes):
    tag : str = 'guests'

    @cache_on_self
    def db_guests(self):
        return cbr_shared_objects.db_guests()

    def data(self):
        return self.db_guests().db_guests__data()

    def ids(self):
        return self.db_guests().db_guests__ids()

    def setup_routes(self):
        self.add_route_get(self.data)
        self.add_route_get(self.ids)
        return self