 # How to Install
```shell
pip install FIM
```
# How to Use It
```python
from FIM import Apriori, Eclat, HMine, ARM

algo_obj = Apriori(DB,SingleItems,MinAbsSupp)
algo_obj.findFrequentItems()
algo_obj.showFrequentItems()
arm = ARM((DATABASE,SingleItems), algo_obj.FREQUENTITEMSETS, minconf = 0.9, minkulc = 0.4)
arm.findRules()
```