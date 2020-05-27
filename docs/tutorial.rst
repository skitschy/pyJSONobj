Tutorial
===================

.. py:module:: jsonobj

Firstly, you decode a JSON document to a :class:`JSONobj`
as with the standard :mod:`json` module.

    >>> import jsonobj
    >>> obj = jsonobj.loads('{"key1": "value1", "key2": "value2"}')

Then, you can access a property of that JSON object just like an attribute.

    >>> obj.key1
    'value1'

You can set the value of a property.

    >>> obj.key2 = 'updated'
    >>> obj
    jsonobj.JSONobj({'key1': 'value1', 'key2': 'updated'})

You can also add and delete a property.

    >>> obj.key3 = 'added'
    >>> obj
    jsonobj.JSONobj({'key1': 'value1', 'key2': 'updated', 'key3': 'added'})
    >>> del obj.key3
    >>> obj
    jsonobj.JSONobj({'key1': 'value1', 'key2': 'updated'})
    
Alternatively, you can access and modify the raw :obj:`dict`.

    >>> obj.dict
    {'key1': 'value1', 'key2': 'updated'}
    >>> obj.dict['key2'] = 'value2'
    >>> obj.key2
    'value2'
    >>> obj.dict['key3'] = 'added'
    >>> obj
    jsonobj.JSONobj({'key1': 'value1', 'key2': 'value2', 'key3': 'added'})
    >>> del obj.dict['key3']
    >>> obj
    jsonobj.JSONobj({'key1': 'value1', 'key2': 'value2'})

:class:`JSONobj` supports the :class:`Collection` interface for its properties.

    >>> len(obj)
    2
    >>> 'key1' in obj
    True
    >>> for k in obj:
    ...     print(k)
    key1
    key2

Nested objects are of course supported.

    >>> obj = jsonobj.loads('{"top1": {"foo": "bar"}}')
    >>> obj.top1.foo
    'bar'
    >>> obj.top2 = {'fiz': 'buz'}
    >>> obj.top2.fiz
    'buz'

JSON arrays in objects and objects in arrays are also supported.

    >>> obj = jsonobj.loads('[{"key": "value1"}, {"key": ["foo", "bar"]}]')
    >>> obj[0].key
    'value1'
    >>> obj[1].key[0]
    'foo'
    >>> obj.insert(1, {"fiz": "buz"})
    >>> obj[1].fiz
    'buz'

You can dump this modified JSON object as with the standard :mod:`json` module.

    >>> jsonobj.dumps(obj)
    '[{"key": "value1"}, {"fiz": "buz"}, {"key": ["foo", "bar"]}]'
