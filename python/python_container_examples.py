from collections.abc import MutableMapping
from sortedcontainers import SortedList


class OrderedMapItem:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
    
    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key
    
    def __le__(self, other):
        return self.key <= other.key
    
    def __gt__(self, other):
        return self.key > other.key
    
    def __ge__(self, other):
        return self.key >= other.key

    def __ne__(self, other):
        return self.key != other.key
    
    def __str__(self):
        return str(self.key)
        
    


class OrderedMap(MutableMapping):

    def __init__(self, *args, **kwargs):
        """
            dict() -> new empty dictionary
            dict(mapping) -> new dictionary initialized from a mapping object's
                (key, value) pairs
            dict(iterable) -> new dictionary initialized as if via:
                d = {}
                for k, v in iterable:
                      d[k] = v
            dict(**kwargs) -> new dictionary initialized with the name=value pairs
                  in the keyword argument list.  For example:  dict(one=1, two=2)
        """
        self._data = SortedList()
        self.update(*args, **kwargs)
    
    
    def __getitem__(self, key):
        """
            x.__getitem__(y) <==> x[y]
        """
        i = self._data.bisect_left(OrderedMapItem(key,0))
        if i < len(self._data) and  self._data[i].key == key:
            return  self._data[i].value
        else:
            raise KeyError
    

    def __setitem__(self, key, value):
        """
            Set self[key] to value.
        """
        i = self._data.bisect_left(OrderedMapItem(key,0))
        if i < len(self._data) and  self._data[i].key == key:
            self._data[i].value = value
        else:
            self._data.add(OrderedMapItem(key=key, value=value))


    def __delitem__(self, key):
        """
            Delete self[key].
        """
        i = self._data.bisect_left(OrderedMapItem(key,0))
        if i < len(self._data) and  self._data[i].key == key:
            self._data.__delitem__(i)
        else:
            raise KeyError


    def __iter__(self):
        """
            Implement iter(self).
        """
        for k, v in self.items():
            yield k


    def __len__(self) -> int:
        """
            Return len(self).
        """
        return len(self._data)


    def __repr__(self):
        dictRepr = ""
        for k, v in self.items():
            dictRepr += f"{repr(k)}: {repr(v)}, "
        dictRepr = dictRepr[:-2] if dictRepr[-2:] == ', ' else dictRepr
        return "OrderedMap({%s})" % dictRepr


    def items(self):
        """
            D.items() -> a set-like object providing a view on D's items
        """
        size = len(self)
        for i in range(size):
            if len(self) != size:
                raise RuntimeError("dictionary changed size during iteration")
            item = self._data[i]
            yield item.key, item.value

    # def keys(self):
    #     """
    #         D.keys() -> a set-like object providing a view on D's keys
    #     """
    #     return self.__iter__()
            
    
    # def values(self):
    #     """
    #         D.values() -> an object providing a view on D's values
    #     """
    #     for k, v in self.items():
    #         yield v


    # def get(self, key, default=None):
    #     """
    #         Return the value for key if key is in the dictionary, else default.
    #     """
    #     try:
    #         return self.__getitem__(key)
    #     except KeyError:
    #         return default


    # def clear(self):
    #     """
    #         D.clear() -> None.  Remove all items from D.
    #     """
    #     self._data.clear()


    # def pop(self, key, default=None):
    #     """
    #         D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
    
    #         If key is not found, default is returned if given, otherwise KeyError is raised
    #     """

        
    # def popitem(self):
    #     """
    #         Remove and return a (key, value) pair as a 2-tuple.
    
    #         Pairs are returned in LIFO (last-in, first-out) order.
    #         Raises KeyError if the dict is empty.
    #     """
    #     return super().popitem()
    

    def copy(self):
        """
            D.copy() -> a shallow copy of D
        """
        ret = OrderedMap()
        ret._data = self._data.copy()
        return ret


    def update(self, *args, **kwargs):
        """
            D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
            If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
            If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
            In either case, this is followed by: for k in F:  D[k] = F[k]
        """
        if args and args[0]:
            if hasattr(args[0], "keys"):
                for k in args[0]:
                    self.__setitem__(k, args[0][k])
            else:
                for k, v in args[0]:
                    self.__setitem__(k,v)
        for k, v in kwargs.items():
            self.__setitem__(k,v)
            


if __name__ == '__main__':
    m1 = OrderedMap()
    m2 = OrderedMap({'c': 1, 'b': 2})
    m3 = OrderedMap([('a', 1), ('b', 2)])
    m4 = OrderedMap(a=1, b=2)
    m2['a'] = 3
    print(m1)
    print(m3)
    print(m4)
    print(m2['a'])
    for k in m2:
        print(k)
    for k in m3.keys():
        print(k)
    for v in m4.values():
        print(v)
    for k,v in m4.items():
        print(k,v)
    print(m2.get('a'))
    print(m2.pop('a'))
    print(m2.get('a'))
    m2.clear()
    print(m2)
    m3['1'] = 3
    m5 = m3.copy()
    print(m3.popitem())
    print(m3.popitem())
    print(m3.popitem())
    print(m3)
    print(m5)
    