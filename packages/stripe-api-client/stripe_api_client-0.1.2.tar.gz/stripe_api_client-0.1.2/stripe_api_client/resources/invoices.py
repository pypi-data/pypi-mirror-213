from stripe_api_client.resources import base

from stripe_api_client.utils import urljoin


class UpcomingInvoicesPool(
    base.ResourcePool,
    base.ListableResource
):
    @property
    def lines(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'lines'), self._session
        )

class InvoicesPool(
    base.ResourcePool,
    base.CreatableResource,
    base.ListableResource,
    base.GettableResource,
    base.UpdatableResource,
    base.DeletableResource
):
    
    @property
    def upcoming(self):
        return base.UpcomingInvoicesPool(
            urljoin(self._endpoint, 'upcoming'), self._session
        )
    
    @property
    def search(self):
        return base.QueryPool(
            urljoin(self._endpoint, 'search'), self._session
        )    

    def finalize(self, invoice_id):
        return base.ActionPool(
            urljoin(self._endpoint, invoice_id, 'finalize'), self._session
        )
    
    def pay(self, invoice_id):
        return base.ActionPool(
            urljoin(self._endpoint, invoice_id, 'pay'), self._session
        )
    
    def send(self, invoice_id):
        return base.ActionPool(
            urljoin(self._endpoint, invoice_id, 'send'), self._session
        )
    
    def void(self, invoice_id):
        return base.ActionPool(
            urljoin(self._endpoint, invoice_id, 'void'), self._session
        )
    
    def mark_uncollectible(self, invoice_id):
        return base.ActionPool(
            urljoin(self._endpoint, invoice_id, 'mark_uncollectible'), self._session
        )
    
    def lines(self, invoice_id):
        return base.QueryPool(
            urljoin(self._endpoint, invoice_id, 'lines'), self._session
        )
