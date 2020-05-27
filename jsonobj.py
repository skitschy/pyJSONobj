"""Wrapper module to provide a simple property accessor for JSON objects."""

__version__ = '0.1.0'
__author__ = 'skitchy'

import json


def dump(obj, fp, **kwargs):
    """Serialize *obj* as a JSON formatted stream to *fp*
    with the same interface as the standard :func:`json.dump`."""
    return json.dump(unwrap(obj), fp, **kwargs)


def dumps(obj, **kwargs):
    """Serialize *obj* to a JSON formatted :class:`str`
    with the same interface as the standard :func:`json.dumps`."""
    return json.dumps(unwrap(obj), **kwargs)


def load(fp, **kwargs):
    """Deserialize *fp* to a wrapped JSON object
    with the same interface as the standard :func:`json.load`."""
    return wrap(json.load(fp, **kwargs))


def loads(s, **kwargs):
    """Deserialize *s* to a wrapped JSON object
    with the same interface as the standard :func:`json.loads`."""
    return wrap(json.loads(s, **kwargs))


def wrap(value):
    """Wrap a standard :class:`dict` or :class:`list`
    to a :class:`JSONobj` or :class:`JSONarray`.

    >>> wrap({'key': 'value'})
    JSONobj({'key': 'value'})
    >>> wrap(['foo', 'bar'])
    JSONarray(['foo', 'bar'])
    >>> wrap(('foo', 'bar'))
    JSONarray(('foo', 'bar'))
    """
    if isinstance(value, dict):
        return JSONobj(value)
    elif isinstance(value, list) or isinstance(value, tuple):
        return JSONarray(value)
    else:
        return value


def unwrap(value):
    """Unwrap a :class:`JSONobj` or :class:`JSONarray`
    to a standard :class:`dict` or :class:`list`.

    >>> unwrap(JSONobj({'key': 'value'}))
    {'key': 'value'}
    >>> unwrap(JSONarray(['foo', 'bar']))
    ['foo', 'bar']
    >>> unwrap(JSONarray(('foo', 'bar')))
    ('foo', 'bar')
    """
    if isinstance(value, JSONobj):
        return value.dict
    elif isinstance(value, JSONarray):
        return value.seq
    else:
        return value


class JSONobj:
    """Wrapper class of a JSON object for providing pseudo-attribute access
    to JSON object properties.

    Args:
        jsondict (:class:`dict`): A :class:`dict` representing a JSON object.

    >>> obj = JSONobj({'key': 'value'})
    >>> obj.key
    'value'
    >>> obj.foo = 'bar'
    >>> 'foo' in obj
    True
    >>> obj.foo = 'fiz'
    >>> obj.dict
    {'key': 'value', 'foo': 'fiz'}
    >>> del obj.foo
    >>> str(obj)
    '{"key": "value"}'

    Attributes:
        dict (:class:`dict`): The raw dict.
    """

    __slots__ = ('dict',)

    def __init__(self, jsondict={}):
        JSONobj.__dict__['dict'].__set__(self, jsondict)

    def __len__(self):
        return self.dict.__len__()

    def __contains__(self, item):
        return self.dict.__contains__(item)

    def __iter__(self):
        return self.dict.__iter__()

    def __getattr__(self, name):
        """Return the value of the *name* property."""
        return wrap(self.dict.__getitem__(name))

    def __setattr__(self, name, value):
        """Set the *name* property to *value*."""
        return self.dict.__setitem__(name, unwrap(value))

    def __delattr__(self, name):
        return self.dict.__delitem__(name)

    def __eq__(self, other):
        return self.dict.__eq__(unwrap(other))

    def __repr__(self):
        return 'jsonobj.JSONobj({!r})'.format(self.dict)

    def __str__(self):
        return json.dumps(self.dict)


class JSONarray:
    """Wrapper class of a JSON array for supporting :class:`JSONobj`.

    Args:
        jsonseq (:obj:`sequence`):
            A :class:`list` or :class:`tuple` representing a JSON array.

    >>> array = JSONarray([{'key': 'value'}])
    >>> array[0].key
    'value'
    >>> array.append(JSONobj({'foo': 'bar'}))
    >>> array.seq
    [{'key': 'value'}, {'foo': 'bar'}]
    >>> for e in array:
    ...   e
    JSONobj({'key': 'value'})
    JSONobj({'foo': 'bar'})

    Attributes:
        seq (:obj:`sequence`): The raw sequence.
    """

    __slots__ = ('seq',)

    def __init__(self, jsonseq=[]):
        self.seq = jsonseq

    def __len__(self):
        return self.seq.__len__()

    def __contains__(self, item):
        return self.seq.__contains__(unwrap(item))

    def __getitem__(self, index):
        return wrap(self.seq.__getitem__(index))

    def __setitem__(self, index, value):
        return self.seq.__setitem__(index, unwrap(value))

    def __delitem__(self, index):
        return self.seq.__delitem__(index)

    def __iter__(self):
        class Iterator:
            def __init__(self, itr):
                self.itr = itr

            def __next__(self):
                return wrap(next(self.itr))

            def __iter__(self):
                return self

        return Iterator(self.seq.__iter__())

    def __reversed__(self):
        class Iterator:
            def __init__(self, itr):
                self.itr = itr

            def __next__(self):
                return wrap(next(self.itr))

            def __iter__(self):
                return self

        return Iterator(self.seq.__reversed__())

    def index(self, value, start=0, stop=-1):
        return self.seq.index(unwrap(value), start, stop)

    def count(self, value):
        return self.seq.count(unwrap(value))

    def insert(self, index, value):
        return self.seq.insert(index, value)

    def append(self, value):
        return self.seq.append(unwrap(value))

    def clear(self):
        return self.seq.clear()

    def reverse(self):
        self.seq.reverse()

    def extend(self, values):
        if values is self:
            values = list(values.seq)
        for v in values:
            self.append(unwrap(v))

    def pop(self, index=-1):
        return wrap(self.seq.pop(index))

    def remove(self, value):
        self.seq.remove(value)

    def __iadd__(self, values):
        self.extend(values)
        return self

    def __eq__(self, other):
        return self.seq.__eq__(unwrap(other))

    def __repr__(self):
        return 'jsonobj.JSONarray({!r})'.format(self.seq)

    def __str__(self):
        return json.dumps(self.seq)
