# MONarchy module for MON estimators #

![](https://img.shields.io/github/workflow/status/prise-3d/MONarchy/build?style=flat-square) ![](https://img.shields.io/pypi/v/MONarchy?style=flat-square) ![](https://img.shields.io/pypi/dm/MONarchy?style=flat-square)

## MONArchy provides : ##
- estimation functions using MON and derivative methods
- The MONArchy class to call each function on a set of data

## Analyse.py ##
- Analyse : to load data and return a JSON file with estimations and descriptive statistics

exemple : 
```
a = Analyse(path)
print(a.head())

print(a.infos())
a.save_graph("0_0_R","fig.png")
```
with 
- ``path`` : the path of a CSV file (string)
- ``column_name`` : the column name (string)

produce a JSON file with statistical estimators

## Changelog 

### 1.0.8
- add a method to list column name

### 1.0.7
- correct requirements.txt

### 1.0.6
- add save_graph in Analyse

### 1.0.5 
- add bayesian MoN 

## References 

```
@article{orenstein_robust_2019,
	title = {Robust Mean Estimation with the Bayesian Median of Means},
	url = {http://arxiv.org/abs/1906.01204},
	journaltitle = {{arXiv}:1906.01204 [math, stat]},
	author = {Orenstein, Paulo},
	urldate = {2021-04-08},
	date = {2019-06-04},
	eprinttype = {arxiv},
	eprint = {1906.01204},
	keywords = {Bayesian, Estimators, {MON}, Math, Mathematics - Statistics Theory, Statistics - Methodology},
}
```

```
@unpublished{buisine:hal-03201630,
  TITLE = {{Fireflies removing in Monte Carlo rendering with adaptive Median of meaNs}},
  AUTHOR = {Buisine, J{\'e}r{\^o}me and Delepoulle, Samuel and Renaud, Christophe},
  URL = {https://hal.archives-ouvertes.fr/hal-03201630},
  NOTE = {working paper or preprint},
  YEAR = {2021},
  MONTH = Apr,
  PDF = {https://hal.archives-ouvertes.fr/hal-03201630/file/Gini_MON_2021_arXiv.pdf},
  HAL_ID = {hal-03201630},
  HAL_VERSION = {v1},
}
```

# License

[MIT](LICENSE)
