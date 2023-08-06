from stripe_api_client.resources import base

from stripe_api_client.utils import urljoin


class ChargesPool(
    base.ResourcePool,
    base.ListableResource,
    base.GettableResource,
    base.CreatableResource,
    base.UpdatableResource
):

    @property
    def search(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'search'), self._session
        )
    
    def capture(self, charge_id):
        return base.ActionPool(
            urljoin(self._endpoint, charge_id, 'capture'), self._session
        )