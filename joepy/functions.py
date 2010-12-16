'''Some combinatoric functions given list input.'''

def all_tuples(n, x):
  '''yields all tuples of length n from iterable x'''
  if n <= 0:
    raise ValueError('Cannot create negative length tuples')
  x = list(x)
  if n > len(x):
    raise ValueError('Cannot create tuple longer than x')
  elif n == len(x):
    yield tuple(x)
  elif n == 1:
    for i in x: yield (i,)
  else:
    # 2 <= n < len(x)
    for i in xrange(len(x)-(n-1)):
      for t in all_tuples(n-1, x[i+1:]):
        yield (x[i],) + t

def all_pairs(x):
  '''yields all pairs of elements from iterable x'''
  for y in all_tuples(2, x): yield y

def all_triples(x):
  '''yields all triples of elements from iterable x'''
  for y in all_tuples(3, x): yield y
