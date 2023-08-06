from stripe_api_client.resources import base

from stripe_api_client.utils import urljoin


class PaymentIntentsPool(
    base.ResourcePool,
    base.CreatableResource,
    base.GettableResource,
    base.ListableResource,
    base.UpdatableResource
):
    
    def confirm(self, pi_id):
        return base.ActionPool(
            urljoin(self._endpoint, pi_id, 'confirm')
        )
    
    def capture(self, pi_id):
        return base.ActionPool(
            urljoin(self._endpoint, pi_id, 'capture')
        )

    def cancel(self, pi_id):
        return base.ActionPool(
            urljoin(self._endpoint, pi_id, 'cancel')
        )        
    
    def increment_authorization(self, pi_id):
        return base.ActionPool(
            urljoin(self._endpoint, pi_id, 'increment_authorization')
        )        

    def verify_microdeposits(self, pi_id):
        return base.ActionPool(
            urljoin(self._endpoint, pi_id, 'verify_microdeposits')
        )        

    def apply_customer_balance(self, pi_id):
        return base.ActionPool(
            urljoin(self._endpoint, pi_id, 'apply_customer_balance')
        )                    

