from braze_api_client.utils import urljoin
from braze_api_client.resources import base


class UsersAliasPool(
    base.ResourcePool
):
    
    @property
    def new(self):
        return base.ActionPool(
            urljoin(self._endpoint, 'new'), self._session
        )        

class UsersPool(
    base.ResourcePool
):

    @property
    def track(self):
        return base.ActionPool(
            urljoin(self._endpoint, 'track'), self._session
        )
    
    @property
    def alias(self):
        return UsersAliasPool(
            urljoin(self._endpoint, 'alias'), self._session
        )