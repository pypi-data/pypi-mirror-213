import requests as rq

from stripe_api_client import resources
from stripe_api_client.utils import urljoin


class Client:
    BASE_URL = 'https://api.stripe.com'

    def __init__(self, api_key, account_id=None, version='v1'):
        self._session = rq.Session()

        self._session.headers = {
            'Authorization': f'Bearer {api_key}'
        }

        if account_id:
            self._session.headers.update({
                'Stripe-Account': account_id
            })

        self._base_url = urljoin(self.BASE_URL, version)
        self._resources = {
            'customers': resources.CustomersPool(
                urljoin(self._base_url, 'customers'), self._session
            ),
            'charges': resources.ChargesPool(
                urljoin(self._base_url, 'charges'), self._session
            ),
            'payment_methods': resources.PaymentMethodsPool(
                urljoin(self._base_url, 'payment_methods'), self._session
            ),
            'payment_intents': resources.PaymentIntentsPool(
                urljoin(self._base_url, 'payment_intents'), self._session
            ),
            'invoices': resources.InvoicesPool(
                urljoin(self._base_url, 'invoices'), self._session
            ),
            'subscriptions': resources.SubscriptionsPool(
                urljoin(self._base_url, 'subscriptions'), self._session
            )
        }


    @property
    def resources(self):
        return self._resources
    
    @property
    def customers(self):
        return self._resources['customers']
    
    @property
    def charges(self):
        return self._resources['charges']

    @property
    def payment_methods(self):
        return self._resources['payment_methods']        

    @property
    def payment_intents(self):
        return self._resources['payment_intents']   
    
    @property
    def invoices(self):
        return self._resources['invoices']  

    @property
    def subscriptions(self):
        return self._resources['subscriptions']           
