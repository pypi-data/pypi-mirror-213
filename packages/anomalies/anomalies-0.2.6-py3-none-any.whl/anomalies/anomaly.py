import numpy as np
# !/usr/bin/env python3
r'''
Implementation of arXiv:1905.13729:

A set of $N$  $n_\alpha$ integers that satisfy Diophantine
equations
$$
\sum_{\alpha=1}^{N}n_{\alpha}=0\,,\qquad  \sum_{\alpha=1}^{N}n_{\alpha}^3=0\,,
$$
can be parametrized as a function of two sets of integers $l$ and $k$,
with dimensions $(N-3)/2$ and $(N-1)/2$ for $N$ odd,
or $N/2-1$ and $N/2-1$ for $N$ even
'''


def _z(ll, k, sort=True, reverse=False):
    r'''
    Implementation of arXiv:1905.13729
    For l,k two set of same dimensions (or k with an extra dimension)
    return a builded array z, such that
     sum( z )=0
     sum( z**3)=0
    '''
    ll = list(ll)
    k = list(k)
    # Build vector-like solutions x,y
    if len(ll) == len(k):
        x = np.array([ll[0]] + k + [-ll[0]] + [-i for i in k])
        y = np.array([0, 0] + ll + [-i for i in ll])
    else:
        x = np.array([0] + k + [-i for i in k])
        y = np.array(ll + [k[0]] + [0] + [-i for i in ll] + [-k[0]])
    # Build not trivial solution
    zz = (x * y**2).sum() * x - (x**2 * y).sum() * y
    if sort:
        zz = sorted(zz, key=abs, reverse=reverse)
    return np.array(zz)


class cfree(object):
    '''
    Add attributes to the _z function:
    * `gcd`: general common denominator
    * `simplified`: solution with gcd=1
    '''
    def __call__(self, ll, k, sort=True, reverse=False):
        zz = _z(ll, k, sort=sort, reverse=reverse)
        self.gcd = np.gcd.reduce(zz)
        self.simplified = (zz / self.gcd).astype(int)
        return zz


free = cfree()
if __name__ == '__main__':
    ll = input('List of integers → l=')
    k = input('List of integers → k=')
    sltn = free(eval(ll), eval(k))
    print(free.simplified)
