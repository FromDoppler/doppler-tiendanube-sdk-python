# -*- coding: utf-8 -*-
import json

from .base import ListResource, Resource, ListSubResource
from .decorators import subresources

class CategoryResource(ListResource):

    resource_name = 'categories'


class CustomerResource(ListResource):

    resource_name = 'customers'


class OrderResource(ListResource):

    resource_name = 'orders'


# @subresources(['variants', 'images'])
class ProductResource(ListResource):

    resource_name = 'products'

    def __init__(self ,http_client, store_id):
        super(ProductResource, self).__init__(http_client, store_id)
        self.images = ListSubResource(self, 'images')
        self.variants = ListSubResource(self, 'variants')


class ScriptResource(ListResource):

    resource_name = 'scripts'


class StoreResource(Resource):

    def get(self):
        """
        Get a single store.
        """
        return json.loads(self._make_request('store').content)


class WebhookResource(ListResource):

    resource_name = 'webhooks'
