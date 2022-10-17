 # How to Install
```shell
pip install FIMdeneme
```
# How to Use It
```python
from FIM import FIMAlgorithms

algo_obj = FIMAlgorithms.Apriori(DB,SingleItems,MinAbsSupp)
algo_obj.findFrequentItems()
algo_obj.showFrequentItems()
arm = FIMAlgorithms.ARM((DATABASE,SingleItems), algo_obj.FREQUENTITEMSETS, minconf = 0.9, minkulc = 0.4)
arm.findRules()
```