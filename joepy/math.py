'''some math functions'''
from __future__ import division
from __future__ import absolute_import
import math as m
import numpy as n

def median(x):
  '''computes the median of a list of items'''
  l = len(x)
  if l == 0:
    raise ValueError('Cannot compute median of 0-length sequence')
  if l == 1:
    return x[0]
  x = sorted(x)
  if l % 2 == 0:
    return (x[l//2] + x[(l//2)-1]) / 2
  else:
    return x[ (l//2) ]

def mean(x):
  '''computes the mean of a sequence'''
  if len(x) == 0:
    raise ValueError('Cannot compute mean of 0-length sequence')
  return sum(x) / len(x)

def variance(x):
  '''computes the variance of a sequence'''
  m = mean(x)
  return sum((xi-m)**2 for xi in x)

def std_dev(x):
  '''computes the standard deviation of a sequence'''
  return m.sqrt(variance(x))

def hist(x):
  '''prints a histogram of the data'''
  import numpy as n
  (vals, bins) = n.histogram(x, new=True)
  s = '\n'.join('[%0.3f,%0.3f): %s' % (bins[i], bins[i+1], '#'*vals[i]) for i \
                in xrange(len(vals)-1))
  s = s + '\n[%0.3f,%0.3f]: %s' % (bins[len(vals)-1], bins[len(vals)],
                                '#'*vals[-1])
  return s
