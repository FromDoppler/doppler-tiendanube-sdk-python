# -*- coding: utf-8 -*-
from .api import APIClient
from .resources import (CategoryResource, CustomerResource,
                        OrderResource, ProductResource,
                        StoreResource, ScriptResource,
                        WebhookResource)


class Store(object):

    def __init__(self, http_client, store_id):
        self.store = StoreResource(http_client, store_id)
        self.customers = CustomerResource(http_client, store_id)
        self.products = ProductResource(http_client, store_id)
        self.categories = CategoryResource(http_client, store_id)
        self.orders = OrderResource(http_client, store_id)
        self.scripts = ScriptResource(http_client, store_id)
        self.webhooks = WebhookResource(http_client, store_id)

    def get_info(self):
        return self.store.get()

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


class NubeClient(object):

    def __init__(self, api_key, user_agent='MyNubeApp (mynubeapp.com)'):
        self._http_client = APIClient(api_key, user_agent)

    def get_store(self, store_id):
        return Store(self._http_client, str(store_id))
