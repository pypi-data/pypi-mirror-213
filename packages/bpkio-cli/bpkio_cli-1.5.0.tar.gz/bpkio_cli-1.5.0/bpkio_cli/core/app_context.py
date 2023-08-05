from typing import Optional

from bpkio_api.api import BroadpeakIoApi
from bpkio_api.models import Tenant

from bpkio_cli.core.config_provider import ConfigProvider
from bpkio_cli.core.resource_recorder import ResourceRecorder
from bpkio_cli.core.resource_trail import ResourceTrail
from bpkio_cli.core.response_handler import ResponseHandler


class AppContext:
    def __init__(self, api: BroadpeakIoApi, tenant_provider=None):
        self.api = api
        self.tenant_provider = tenant_provider
        self._tenant: Optional[Tenant] = None

        self.flags = dict()
        self.resources = ResourceTrail()
        self.cache: ResourceRecorder = None
        self.response_handler = ResponseHandler()
        self.config = ConfigProvider()

    @property
    def tenant(self):
        return self._tenant

    @tenant.setter
    def tenant(self, new_value: Tenant):
        self._tenant = new_value
        self.cache = ResourceRecorder(self.api.fqdn, new_value.id)
        self.response_handler = ResponseHandler(self.cache)

