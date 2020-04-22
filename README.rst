nuvemshop-python
=================

.. image:: https://travis-ci.org/kmee/nuvemshop-python.png?branch=master   
   :target: https://travis-ci.org/kmee/nuvemshop-python

NuvemShop API Python Client.

Install
-------

Just ``pip install git+https://github.com/kmee/nuvemshop-python.git --upgrade --no-cache-dir``.

Usage
-----

API_KEY is your authentication token. After you've successfully authenticate:
https://github.com/tiendanube/api-docs/blob/master/resources/authentication.md

Query list of products::

    > api_key = 'API_KEY'
    > from tiendanube.client import NubeClient
    > client = NubeClient(api_key)
    > store = client.get_store(1)
    > [p.name for p in store.products.list()]
    [u'Mi primer producto',
     u'Probando publicaci\xf3n',
     u'hola',
     u'Producto de Prueba']

Query one product in particular::

    > api_key = 'API_KEY'
    > from tiendanube.client import NubeClient
    > client = NubeClient(api_key)
    > store = client.get_store(1)
    > p = store.products.get(911)
    > p.name
    u'Mi primer producto'

Query images for a given product::

    > api_key = 'API_KEY'
    > from tiendanube.client import NubeClient
    > client = NubeClient(api_key)
    > store = client.get_store(1)
    > p = store.products.get(911)
    > [i.src for i in p.images.list()]
    [u'http://example.com/image.jpg']

Add a product to the store::

    > api_key = 'API_KEY'
    > from tiendanube.client import NubeClient
    > client = NubeClient(api_key)
    > store = client.get_store(1)
    > p = store.products.add({ "name": {"pt": "My new product"} })

Update a product on the store::

    > api_key = 'API_KEY'
    > from tiendanube.client import NubeClient
    > client = NubeClient(api_key)
    > store = client.get_store(1)
    > p = store.products.update({ "id":123, "name": {"pt": "My AWESOME product"} })

Development
-----------

Running tests::

    $ python -m tests.run

