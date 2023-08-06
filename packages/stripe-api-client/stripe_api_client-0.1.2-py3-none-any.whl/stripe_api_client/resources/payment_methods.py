from stripe_api_client.resources import base

from stripe_api_client.utils import urljoin


class PaymentMethodsPool(
    base.ResourcePool,
    base.ListableResource,
    base.GettableResource,
    base.CreatableResource,
    base.UpdatableResource
):

    def attach(self, payment_method_id):
        return base.ActionPool(
            urljoin(self._endpoint, payment_method_id, 'attach'), self._session
        )
    
    def detach(self, payment_method_id):
        return base.ActionPool(
            urljoin(self._endpoint, payment_method_id, 'detach'), self._session
        )
    