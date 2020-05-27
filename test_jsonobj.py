import unittest
from io import StringIO

import jsonobj


class Test_jsonobj(unittest.TestCase):
    def test_loads(self):
        o = jsonobj.loads('[{"key1": "value1"}, {"key2": "value2"}]')
        self.assertEqual(o[0], dict(key1='value1'))
        self.assertEqual(o[1], dict(key2='value2'))
        self.assertEqual(o[0].key1, 'value1')
        self.assertEqual(o[1].key2, 'value2')

    def test_load(self):
        o = jsonobj.load(StringIO('[{"key1": "value1"}, {"key2": "value2"}]'))
        self.assertEqual(o[0], dict(key1='value1'))
        self.assertEqual(o[1], dict(key2='value2'))
        self.assertEqual(o[0].key1, 'value1')
        self.assertEqual(o[1].key2, 'value2')

    def test_dumps(self):
        jsonstr = '[{"key1": "value1"}, {"key2": "value2"}]'
        o = jsonobj.loads(jsonstr)
        self.assertEqual(jsonobj.dumps(o), jsonstr)

    def test_dump(self):
        jsonstr = '[{"key1": "value1"}, {"key2": "value2"}]'
        o = jsonobj.loads(jsonstr)
        io = StringIO()
        jsonobj.dump(o, io)
        self.assertEqual(io.getvalue(), jsonstr)


class TestJSONobj(unittest.TestCase):
    def test_len(self):
        obj = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        self.assertEqual(len(obj), 2)

    def test_contains(self):
        obj = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        self.assertIn('key1', obj)
        self.assertIn('key2', obj)
        self.assertNotIn('key3', obj)

    def test_iter(self):
        obj = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        array = [e for e in obj]
        self.assertEqual(array, ['key1', 'key2'])

    def test_getattr(self):
        obj = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        self.assertEqual(obj.key1, 'value1')
        self.assertIsInstance(obj.key2, jsonobj.JSONobj)
        self.assertEqual(obj.key2.foo, 'bar')
        with self.assertRaises(KeyError):
            obj.key3

    def test_setattr(self):
        obj = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        obj.key1 = 'update'
        self.assertEqual(obj.key1, 'update')
        obj.key3 = 'new'
        self.assertEqual(obj.key3, 'new')

    def test_delattr(self):
        obj = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        del obj.key1
        self.assertNotIn('key1', obj)

    def test_eq(self):
        obj1 = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        obj2 = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        obj3 = jsonobj.JSONobj({'key0': 'value0', 'key2': {'foo': 'bar'}})
        self.assertEqual(obj1, obj2)
        self.assertEqual(obj1, {'key1': 'value1', 'key2': {'foo': 'bar'}})
        self.assertNotEqual(obj1, obj3)

    def test_repr(self):
        obj = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        self.assertEqual(eval(repr(obj)), obj)

    def test_str(self):
        obj = jsonobj.JSONobj({'key1': 'value1', 'key2': {'foo': 'bar'}})
        self.assertEqual(str(obj),
                         '{"key1": "value1", "key2": {"foo": "bar"}}')


class TestJSONarray(unittest.TestCase):
    def test_len(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        self.assertEqual(len(array), 2)

    def test_contains(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        self.assertIn('value1', array)
        self.assertIn({'foo': 'bar'}, array)
        self.assertIn(jsonobj.JSONobj({'foo': 'bar'}), array)
        self.assertNotIn('value2', array)

    def test_getitem(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        self.assertEqual(array[0], 'value1')
        self.assertIsInstance(array[1], jsonobj.JSONobj)
        with self.assertRaises(IndexError):
            array[2]

    def test_setitem(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        array[0] = 'update'
        self.assertEqual(array[0], 'update')

    def test_delitem(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        del array[0]
        self.assertNotIn('value1', array)
        self.assertEqual(len(array), 1)
        
    def test_iter(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        a = [e for e in array]
        self.assertEqual(a[0], 'value1')
        self.assertIsInstance(a[1], jsonobj.JSONobj)
        self.assertEqual(a[1], jsonobj.JSONobj({'foo': 'bar'}))

    def test_reversed(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        r = [e for e in reversed(array)]
        self.assertEqual(r[1], 'value1')
        self.assertIsInstance(r[0], jsonobj.JSONobj)
        self.assertEqual(r[0], jsonobj.JSONobj({'foo': 'bar'}))

    def test_index(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        self.assertEqual(array.index('value1'), 0)
        with self.assertRaises(ValueError):
            array.index('value2')

    def test_count(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        self.assertEqual(array.count('value1'), 1)
        self.assertEqual(array.count(jsonobj.JSONobj({'foo': 'bar'})), 1)
        self.assertEqual(array.count('value2'), 0)

    def test_insert(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        array.insert(0, 'insert')
        self.assertEqual(array[0], 'insert')
        self.assertEqual(array[1], 'value1')
        self.assertEqual(len(array), 3)

    def test_append(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        array.append('append')
        self.assertEqual(array[2], 'append')
        self.assertEqual(len(array), 3)

    def test_clear(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        array.clear()
        self.assertEqual(len(array), 0)

    def test_reverse(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        array.reverse()
        self.assertEqual(array[1], 'value1')
        self.assertEqual(array[0], {'foo': 'bar'})

    def test_extend(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        array.extend(array)
        self.assertEqual(array[2], 'value1')
        self.assertEqual(array[3], {'foo': 'bar'})
        self.assertEqual(len(array), 4)
        array.extend(jsonobj.JSONarray([{'key': 'value'}]))
        self.assertEqual(array.seq[4], {'key': 'value'})
        self.assertEqual(len(array), 5)

    def test_pop(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        pop = array.pop()
        self.assertEqual(pop, {'foo': 'bar'})
        self.assertIsInstance(pop, jsonobj.JSONobj)
        self.assertEqual(len(array), 1)
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        self.assertEqual(array.pop(0), 'value1')
        self.assertEqual(array[0], {'foo': 'bar'})
        self.assertEqual(len(array), 1)

    def test_remove(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        array.remove('value1')
        self.assertEqual(array[0], {'foo': 'bar'})
        self.assertEqual(len(array), 1)

    def test_iadd(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        array += array
        self.assertEqual(array[2], 'value1')
        self.assertEqual(array[3], {'foo': 'bar'})
        self.assertEqual(len(array), 4)
        array += jsonobj.JSONarray([{'key': 'value'}])
        self.assertEqual(array.seq[4], {'key': 'value'})
        self.assertEqual(len(array), 5)

    def test_repr(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        self.assertEqual(eval(repr(array)), array)

    def test_str(self):
        array = jsonobj.JSONarray(['value1', {'foo': 'bar'}])
        self.assertEqual(str(array), '["value1", {"foo": "bar"}]')
