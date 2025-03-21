import datetime
import json
import unittest

from mock import Mock, patch
from pytz import utc

from tiendanube.api import APIClient
from tiendanube.resources import (CustomerResource, StoreResource,
                                  ScriptResource, ProductResource,
                                  OrderResource, WebhookResource,
                                  CategoryResource)


class StoreResourceReadTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_get_store_info(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 46, 'name': 'test store'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        s = StoreResource(cli, '46')

        res = s.get()

        self.assertEqual({'id': 46, 'name': 'test store'}, res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/store',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )


class ProductResourceReadTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_list_products_base(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46, 'name': 'test prod'},
            {'id': 47, 'name': 'test prod 2'},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')

        res = p.list()

        self.assertEqual([
            {'id': 46, 'name': 'test prod'},
            {'id': 47, 'name': 'test prod 2'},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_list_products_fields(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46},
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')

        res = p.list(fields='id')

        self.assertEqual([
            {'id': 46},
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_list_products_filter(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')

        res = p.list(filters={'since_id': 47}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'fields': 'id', 'since_id': 47}
        )

    @patch('tiendanube.api.requests')
    def test_list_products_filter_date(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')

        created_at_min = datetime.datetime(2013, 1, 1, 0, 0, 0).replace(tzinfo=utc)
        res = p.list(filters={'since_id': 47, 'created_at_min': created_at_min}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'created_at_min': '2013-01-01T00:00:00+00:00', 'fields': 'id'},
        )

    @patch('tiendanube.api.requests')
    def test_get_product(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')


        res = p.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_get_product_variants(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')


        res = p.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )
        response_mock.content = json.dumps([{'id': 991, 'name': 'test prod variant'}])
        res = res.variants.list()
        self.assertEqual([{'id': 991, 'name': 'test prod variant'}], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991/variants',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_get_product_get_variant(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')


        res = p.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )
        response_mock.content = json.dumps({'id': 1, 'name': 'test prod variant'})
        res = res.variants.get(1)
        self.assertEqual({'id': 1, 'name': 'test prod variant'}, res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991/variants/1',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_get_product_images(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')


        res = p.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )
        response_mock.content = json.dumps([{'id': 991, 'name': 'test prod image'}])
        res = res.images.list()
        self.assertEqual([{'id': 991, 'name': 'test prod image'}], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991/images',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_get_product_get_image(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')


        res = p.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )
        response_mock.content = json.dumps({'id': 1, 'name': 'test prod image'})
        res = res.images.get(1)
        self.assertEqual({'id': 1, 'name': 'test prod image'}, res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991/images/1',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )


class CustomerResourceReadTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_list_customer_base(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46, 'name': 'test cust'},
            {'id': 47, 'name': 'test cust 2'},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CustomerResource(cli, '46')

        res = c.list()

        self.assertEqual([
            {'id': 46, 'name': 'test cust'},
            {'id': 47, 'name': 'test cust 2'},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/customers',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_list_customers_fields(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46},
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CustomerResource(cli, '46')

        res = c.list(fields='id')

        self.assertEqual([
            {'id': 46},
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/customers',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'fields': 'id'},
        )

    @patch('tiendanube.api.requests')
    def test_list_customers_filter(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CustomerResource(cli, '46')

        res = c.list(filters={'since_id': 47}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/customers',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'fields': 'id'},
        )

    @patch('tiendanube.api.requests')
    def test_list_customers_filter_date(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CustomerResource(cli, '46')

        created_at_min = datetime.datetime(2013, 1, 1, 0, 0, 0).replace(tzinfo=utc)
        res = c.list(filters={'since_id': 47, 'created_at_min': created_at_min}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/customers',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'created_at_min': '2013-01-01T00:00:00+00:00', 'fields': 'id'},
        )

    @patch('tiendanube.api.requests')
    def test_get_customer(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CustomerResource(cli, '46')


        res = c.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/customers/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )


class OrderResourceReadTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_list_orders_base(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46, 'name': 'test order'},
            {'id': 47, 'name': 'test order 2'},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        o = OrderResource(cli, '46')

        res = o.list()

        self.assertEqual([
            {'id': 46, 'name': 'test order'},
            {'id': 47, 'name': 'test order 2'},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/orders',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_list_orders_fields(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46},
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        o = OrderResource(cli, '46')

        res = o.list(fields='id')

        self.assertEqual([
            {'id': 46},
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/orders',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_list_orders_filter(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        o = OrderResource(cli, '46')

        res = o.list(filters={'since_id': 47}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/orders',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'fields': 'id'},
        )

    @patch('tiendanube.api.requests')
    def test_list_orders_filter_date(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        o = OrderResource(cli, '46')

        created_at_min = datetime.datetime(2013, 1, 1, 0, 0, 0).replace(tzinfo=utc)
        res = o.list(filters={'since_id': 47, 'created_at_min': created_at_min}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/orders',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'created_at_min': '2013-01-01T00:00:00+00:00', 'fields': 'id'},
        )

    @patch('tiendanube.api.requests')
    def test_get_order(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        o = OrderResource(cli, '46')


        res = o.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/orders/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )


class ScriptResourceReadTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_list_scripts_base(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46, 'src': 'test script'},
            {'id': 47, 'src': 'test script 2'},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        s = ScriptResource(cli, '46')

        res = s.list()

        self.assertEqual([
            {'id': 46, 'src': 'test script'},
            {'id': 47, 'src': 'test script 2'},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/scripts',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_list_scripts_fields(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46},
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        s = ScriptResource(cli, '46')

        res = s.list(fields='id')

        self.assertEqual([
            {'id': 46},
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/scripts',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_list_scripts_filter(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        s = ScriptResource(cli, '46')

        res = s.list(filters={'since_id': 47}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/scripts',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_list_scripts_filter_date(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        s = ScriptResource(cli, '46')

        created_at_min = datetime.datetime(2013, 1, 1, 0, 0, 0).replace(tzinfo=utc)
        res = s.list(filters={'since_id': 47, 'created_at_min': created_at_min}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/scripts',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'created_at_min': '2013-01-01T00:00:00+00:00', 'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_get_script(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        s = ScriptResource(cli, '46')


        res = s.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/scripts/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )


class WebhookResourceReadTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_list_webhooks_base(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46, 'src': 'test webh'},
            {'id': 47, 'src': 'test webh 2'},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        w = WebhookResource(cli, '46')

        res = w.list()

        self.assertEqual([
            {'id': 46, 'src': 'test webh'},
            {'id': 47, 'src': 'test webh 2'},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/webhooks',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_list_webhooks_fields(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46},
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        w = WebhookResource(cli, '46')

        res = w.list(fields='id')

        self.assertEqual([
            {'id': 46},
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/webhooks',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_list_webhooks_filter(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        w = WebhookResource(cli, '46')

        res = w.list(filters={'since_id': 47}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/webhooks',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_list_webhooks_filter_date(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        w = WebhookResource(cli, '46')

        created_at_min = datetime.datetime(2013, 1, 1, 0, 0, 0).replace(tzinfo=utc)
        res = w.list(filters={'since_id': 47, 'created_at_min': created_at_min}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/webhooks',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'created_at_min': '2013-01-01T00:00:00+00:00', 'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_get_webhook(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        w = WebhookResource(cli, '46')


        res = w.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/webhooks/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )


class CategoryResourceReadTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_list_categories_base(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46, 'name': 'test cat'},
            {'id': 47, 'name': 'test cat 2'},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CategoryResource(cli, '46')

        res = c.list()

        self.assertEqual([
            {'id': 46, 'name': 'test cat'},
            {'id': 47, 'name': 'test cat 2'},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/categories',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )

    @patch('tiendanube.api.requests')
    def test_list_categories_fields(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 46},
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CategoryResource(cli, '46')

        res = c.list(fields='id')

        self.assertEqual([
            {'id': 46},
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/categories',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'fields': 'id'},
        )

    @patch('tiendanube.api.requests')
    def test_list_categories_filter(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CategoryResource(cli, '46')

        res = c.list(filters={'since_id': 47}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/categories',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'fields': 'id'},
        )

    @patch('tiendanube.api.requests')
    def test_list_categories_filter_date(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps([
            {'id': 47},
        ])
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CategoryResource(cli, '46')

        created_at_min = datetime.datetime(2013, 1, 1, 0, 0, 0).replace(tzinfo=utc)
        res = c.list(filters={'since_id': 47, 'created_at_min': created_at_min}, fields='id')

        self.assertEqual([
            {'id': 47},
        ], res)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/categories',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params={'since_id': 47, 'created_at_min': '2013-01-01T00:00:00+00:00', 'fields': 'id'}
        )

    @patch('tiendanube.api.requests')
    def test_get_category(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.content = json.dumps({'id': 991, 'name': 'test prod'})
        requests_mock.get.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CategoryResource(cli, '46')


        res = c.get(991)

        self.assertEqual(991, res.id)

        requests_mock.get.assert_called_with(
            url='https://api.tiendanube.com/v1/46/categories/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent'},
            params=None
        )


class ProductResourceWriteTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_add_product(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 201
        response_mock.text = json.dumps(
            {'id': 46, 'name': 'test prod'},
        )
        requests_mock.post.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')

        res = p.add({'id': 46, 'name': 'test prod'})

        self.assertEqual(
            {'id': 46, 'name': 'test prod'}
        , res)

        requests_mock.post.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 46, 'name': 'test prod'})
        )

    @patch('tiendanube.api.requests')
    def test_update_product(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = json.dumps(
            {'id': 991, 'name': 'test prod'},
        )
        requests_mock.put.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        p = ProductResource(cli, '46')

        p.update({'id': 991, 'name': 'test prod updated'})

        requests_mock.put.assert_called_with(
            url='https://api.tiendanube.com/v1/46/products/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 991, 'name': 'test prod updated'})
        )


class CustomerResourceWriteTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_add_customer(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 201
        response_mock.text = json.dumps(
            {'id': 46, 'name': 'test cust'},
        )
        requests_mock.post.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CustomerResource(cli, '46')

        res = c.add({'id': 46, 'name': 'test cust'})

        self.assertEqual(
            {'id': 46, 'name': 'test cust'}
        , res)

        requests_mock.post.assert_called_with(
            url='https://api.tiendanube.com/v1/46/customers',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 46, 'name': 'test cust'})
        )

    @patch('tiendanube.api.requests')
    def test_update_customer(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = json.dumps(
            {'id': 991, 'name': 'test cust'},
        )
        requests_mock.put.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CustomerResource(cli, '46')

        c.update({'id': 991, 'name': 'test cust updated'})

        requests_mock.put.assert_called_with(
            url='https://api.tiendanube.com/v1/46/customers/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 991, 'name': 'test cust updated'})
        )


class OrderResourceWriteTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_add_order(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 201
        response_mock.text = json.dumps(
            {'id': 46, 'name': 'test order'},
        )
        requests_mock.post.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        o = OrderResource(cli, '46')

        res = o.add({'id': 46, 'name': 'test order'})

        self.assertEqual(
            {'id': 46, 'name': 'test order'}
        , res)

        requests_mock.post.assert_called_with(
            url='https://api.tiendanube.com/v1/46/orders',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 46, 'name': 'test order'})
        )

    @patch('tiendanube.api.requests')
    def test_update_order(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = json.dumps(
            {'id': 991, 'name': 'test order'},
        )
        requests_mock.put.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        o = OrderResource(cli, '46')

        o.update({'id': 991, 'name': 'test order updated'})

        requests_mock.put.assert_called_with(
            url='https://api.tiendanube.com/v1/46/orders/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 991, 'name': 'test order updated'})
        )

class ScriptResourceWriteTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_add_script(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 201
        response_mock.text = json.dumps(
            {'id': 46, 'name': 'test script'},
        )
        requests_mock.post.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        s = ScriptResource(cli, '46')

        res = s.add({'id': 46, 'name': 'test script'})

        self.assertEqual(
            {'id': 46, 'name': 'test script'}
        , res)

        requests_mock.post.assert_called_with(
            url='https://api.tiendanube.com/v1/46/scripts',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 46, 'name': 'test script'})
        )

    @patch('tiendanube.api.requests')
    def test_update_script(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = json.dumps(
            {'id': 991, 'name': 'test script'},
        )
        requests_mock.put.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        s = ScriptResource(cli, '46')

        s.update({'id': 991, 'name': 'test script updated'})

        requests_mock.put.assert_called_with(
            url='https://api.tiendanube.com/v1/46/scripts/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 991, 'name': 'test script updated'})
        )

class WebhookResourceWriteTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_add_webhook(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 201
        response_mock.text = json.dumps(
            {'id': 46, 'name': 'test webhook'},
        )
        requests_mock.post.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        w = WebhookResource(cli, '46')

        res = w.add({'id': 46, 'name': 'test webhook'})

        self.assertEqual(
            {'id': 46, 'name': 'test webhook'}
        , res)

        requests_mock.post.assert_called_with(
            url='https://api.tiendanube.com/v1/46/webhooks',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 46, 'name': 'test webhook'})
        )

    @patch('tiendanube.api.requests')
    def test_update_webhook(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = json.dumps(
            {'id': 991, 'name': 'test web'},
        )
        requests_mock.put.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        w = WebhookResource(cli, '46')

        w.update({'id': 991, 'name': 'test web updated'})

        requests_mock.put.assert_called_with(
            url='https://api.tiendanube.com/v1/46/webhooks/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 991, 'name': 'test web updated'})
        )

class CategoryResourceWriteTest(unittest.TestCase):

    @patch('tiendanube.api.requests')
    def test_add_category(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 201
        response_mock.text = json.dumps(
            {'id': 46, 'name': 'test category'},
        )
        requests_mock.post.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CategoryResource(cli, '46')

        res = c.add({'id': 46, 'name': 'test category'})

        self.assertEqual(
            {'id': 46, 'name': 'test category'}
        , res)

        requests_mock.post.assert_called_with(
            url='https://api.tiendanube.com/v1/46/categories',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 46, 'name': 'test category'})
        )

    @patch('tiendanube.api.requests')
    def test_update_category(self, requests_mock):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = json.dumps(
            {'id': 991, 'name': 'test cat'},
        )
        requests_mock.put.return_value = response_mock
        cli = APIClient('test_api_key', 'test user agent')
        c = CategoryResource(cli, '46')

        c.update({'id': 991, 'name': 'test cat updated'})

        requests_mock.put.assert_called_with(
            url='https://api.tiendanube.com/v1/46/categories/991',
            headers={'Authentication': 'bearer test_api_key', 'User-Agent': 'test user agent', 'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({'id': 991, 'name': 'test cat updated'})
        )
