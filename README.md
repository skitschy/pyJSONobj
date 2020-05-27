# JSONobj

JSONobj is a Python module
for providing attribute-like access to the properties of JSON objects.


## Requirement

* Python 2.7 or above


## Installation

```sh
pip install jsonobj
```


## Basic Usage

```python
>>> import jsonobj
>>> obj = jsonobj.loads('{"prop1": "value"}')
>>> obj.prop1
'value'
>>> obj.prop1 = 'changed'
>>> obj.prop2 = ['foo', 'bar', {'fiz': 'buz'}]
>>> 'prop2' in obj
True
>>> obj.dict
{'prop1': 'changed', 'prop2': ['foo', 'bar', {'fiz': 'buz'}]}
>>> obj.prop2[2].fiz
'buz'
>>> del obj.prop1
>>> jsonobj.dumps(obj)
'{"prop2": ["foo", "bar", {"fiz": "buz"}]}'
```


## Documentation

Documentation is [available online](https://pyjsonobj.readthedocs.io/).
