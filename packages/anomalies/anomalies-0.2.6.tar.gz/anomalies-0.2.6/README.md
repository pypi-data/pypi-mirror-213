# Anomalies

![Python package](https://github.com/restrepo/anomalies/workflows/Python%20package/badge.svg)
![Upload Python Package](https://github.com/restrepo/anomalies/workflows/Upload%20Python%20Package/badge.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5526558.svg)](https://doi.org/10.5281/zenodo.5526558)

Implement the anomaly free solution of  [arXiv:1905.13729](https://arxiv.org/abs/1905.13729) [PRL]:

Obtain a numpy array `z` of `N` integers which satisfy the Diophantine equations
```python
>>> z.sum()
0
>>> (z**3).sum()
0
```
The input is two lists `l` and `k` with any `(N-3)/2` and `(N-1)/2` integers for `N` odd, or `N/2-1` and `N/2-1` for `N` even (`N>4`).
The function is implemented below under the name: `free(l,k)`

## Install
```bash
$ pip install anomalies
```
## USAGE
```python
>>> from anomalies import anomaly
>>> anomaly.free([-1,1],[4,-2])
array([  3,   3,   3, -12, -12,  15])
>>> anomaly.free.gcd
3
>>> anomaly.free.simplified
array([ 1,  1,  1, -4, -4,  5])
```

## Example
A sample for `4<N<13` with integers until `|30|` with `~400 000` chiral solutions can be download from: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7380817.svg)](https://doi.org/10.5281/zenodo.7380817) [JSON]
