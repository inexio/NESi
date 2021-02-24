from nesi.devices.softbox.base_resources.route import Route, RouteCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class HuaweiRoute(Route):
    """Represents logical route resource."""

    sub_mask = base.Field('sub_mask')

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class HuaweiRouteCollection(RouteCollection):
    """Represent a collection of logical routes."""

    @property
    def _resource_type(self):
        return HuaweiRoute
