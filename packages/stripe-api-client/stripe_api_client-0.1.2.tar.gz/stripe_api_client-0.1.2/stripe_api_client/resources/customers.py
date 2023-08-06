from stripe_api_client.resources import base

from stripe_api_client.utils import urljoin


class CustomersPaymentMethodsPool(
    base.ResourcePool,
    base.GettableResource,
    base.ListableResource
):
    pass

class CustomersSourcesPool(
    base.ResourcePool,
    base.ListableResource,
    base.GettableResource,
    base.CreatableResource,
    base.UpdatableResource,
    base.DeletableResource    
):
    pass

class CustomersPool(
    base.ResourcePool,
    base.ListableResource,
    base.GettableResource,
    base.CreatableResource,
    base.UpdatableResource,
    base.DeletableResource
):

    @property
    def search(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'search'), self._session
        )
    
    def payment_methods(self, customer_id):
        return CustomersPaymentMethodsPool(
            urljoin(self._endpoint, customer_id, 'payment_methods'), self._session
        )
    
    def sources(self, customer_id):
        return CustomersSourcesPool(
            urljoin(self._endpoint, customer_id, 'sources'), self._session
        )
