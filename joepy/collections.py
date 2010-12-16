from __future__ import absolute_import

class Bag(object):
  '''A bag or multiset:
  http://en.wikipedia.org/wiki/Set_(computer_science)#Multiset
  Mimics python's set with multiple membership. Similar to collections.Counter 
  class, but deletes elements if their count reaches zero and doesn't support
  negative counts.'''
  def __init__(self, data = None):
    '''Creates a new Bag, optionally copying the underlying dict from the
    provided data.

    For example:
    >>> Bag()
    Bag({})
    >>> b = Bag({'a':1, 'b':2})
    >>> b
    Bag({'a': 1, 'b': 2})
    >>> c = Bag(b)
    >>> c
    Bag({'a': 1, 'b': 2})
    '''
    self._b = dict()
    if data:
      for k in data:
        self[k] = data[k]

  def __getitem__(self, item):
    '''Gets the number of times item occurs in the Bag, or zero if the item
    is not in the Bag.

    For example:
    >>> b = Bag({'a':1, 'b':2})
    >>> b['a']
    1
    >>> b['b']
    2
    >>> b['c']
    0
    '''
    return self._b.get(item, 0)

  def __setitem__(self, item, value):
    '''Sets the item's value.  The item is added if it doesn't exist.  If the
    value <= 0, the item isn't added, and is removed if it exists in the bag.

    For example:
    >>> b = Bag({'a':1, 'b':2})
    >>> b['a'] = 2
    >>> b['b'] = 0
    >>> b
    Bag({'a': 2})
    '''
    value = int(value)
    if value > 0:
      self._b[item] = value
    else:
      try: del self._b[item]
      except KeyError: pass

  def __iter__(self):
    '''Returns an iterator over the unique items in the Bag.

    For example:
    >>> b = Bag({'a':1, 'b':2})
    >>> for x in b: print x
    ...
    a
    b
    '''
    return iter(self._b)

  def __contains__(self, item):
    '''Tests if the item is in the Bag at least once.

    For example:
    >>> b = Bag({'a':1, 'b':2})
    >>> 'a' in b
    True
    >>> 'c' in b
    False
    '''
    return item in self._b

  def __iadd__(self, other):
    '''Modifies the Bag in place, adding every element from the provided Bag.

    For example:
    >>> b, c = Bag({'a':1, 'b':2}), Bag({'a':3, 'c':1})
    >>> b += c
    >>> b
    Bag({'a': 4, 'c': 1, 'b': 2})
    '''
    for x in other: self[x] += other[x]
    return self

  def __isub__(self, other):
    '''Modifies the Bag in place, subtracting every element from the provided
    Bag.

    For example:
    >>> b, c = Bag({'a':1, 'b':2}), Bag({'a':3, 'c':1})
    >>> b -= c
    >>> b
    Bag({'b': 2})
    '''
    for x in set(other.keys()) & set(self.keys()):
      self[x] = self[x] - other[x]
    return self

  def __add__(self, other):
    '''Returns the sum of all items in either Bag.

    For example:
    >>> Bag({'a':1, 'b':2}) + Bag({'a':3, 'c':1})
    Bag({'a': 4, 'c': 1, 'b': 2})
    '''
    b = Bag(self)
    b += other
    return b

  def __sub__(self, other):
    '''Returns the bag containing this bag minus the other one.

    For example:
    >>> Bag({'a':1, 'b':2}) - Bag({'a':3, 'c':1})
    Bag({'b': 2})
    '''
    b = Bag(self)
    b -= other
    return b

  def __and__(self, other):
    '''Returns the intersection of the two bags.

    For example:
    >>> Bag({'a':1, 'b':2}) & Bag({'a':3, 'c':1})
    Bag({'a': 1})
    '''
    b = Bag()
    for k in set(self.keys()) & set(other.keys()):
      b[k] = min(self[k], other[k])
    return b

  def __or__(self, other):
    '''Returns the max of values in either of the two Bags.

    For example:
    >>> Bag({'a':1, 'b':2}) | Bag({'a':3, 'c':1})
    Bag({'a': 3, 'c': 1, 'b': 2})
    '''
    b = Bag()
    for k in set(self.keys()) | set(other.keys()):
      b[k] = max(self[k], other[k])
    return b

  def __len__(self):
    '''Returns the number of unique elements in the set.  The len() is always
    less than or equal to the cardinality of the set, and only equal when all
    elements occur only once.'''
    return len(self._b)

  def __repr__(self):
    return 'Bag(%s)' % str(self._b)

  def add(self, item, count = 1):
    '''Add an element to the bag, optionally the provided count.

    For example:
    >>> b = Bag({'a':1, 'b':2})
    >>> b.add('c')
    >>> b.add('d', 10)
    >>> b.add('a')
    >>> b
    Bag({'a': 2, 'c': 1, 'b': 2, 'd': 10})
    '''
    self[item] += count

  def sum(self):
    '''Returns the total number of elements in the bag, or the cardinality of
    this set.

    For example:
    >>> b = Bag({'a':1, 'b':2, 'c':4})
    >>> b.sum()
    7
    '''
    return sum(x for x in self._b.values())

  def keys(self):
    '''Returns a collection (list) of unique items in the Bag.

    For example:
    >>> b = Bag({'a':1, 'b':2, 'c':4})
    >>> b.keys()
    ['a', 'c', 'b']
    '''
    return self._b.keys()

  def clear(self):
    self._b.clear()

  def iteritems(self):
    return self._b.iteritems()

  def itervalues(self):
    return self._b.itervalues()

class BagOfWords(Bag):
  import re
  tokenizer = re.compile('(\\w+)')

  def add_text(self, text, tokenizer = None):
    '''Adds the text string to the bag, tokenizing with the tokenizer.  The
    provided tokenizer must be a compiled regular expression object or an
    iterable over words in the provided text.

    For example:
    >>> b = BagOfWords()
    >>> b.add_text('a man a plan a canal panama')
    >>> b
    Bag({'a': 3, 'canal': 1, 'panama': 1, 'plan': 1, 'man': 1})
    '''
    if not tokenizer:
      tokenizer = BagOfWords.tokenizer

    for w in tokenizer.finditer(text):
      self.add(w.group(1))

if __name__ == "__main__":
  import doctest
  doctest.testmod()
