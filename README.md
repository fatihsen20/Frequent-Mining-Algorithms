 # How to Install
```shell
pip install FIMProject
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
# What is DATABASE and SingleItems?
<p>0 :  ['A' 'B' 'E' 'G']                                      0  :  [1 1 0 0 1 0 1]</p>
<p>1 :  ['B' 'C' 'E' 'F']                                      1  :  [0 1 1 0 1 1 0]</p>
<p>2 :  ['A' 'E' 'F']                                          2  :  [1 0 0 0 1 1 0]</p>
<p>3 :  ['B' 'F' 'G']                                          3  :  [0 1 0 0 0 1 1]</p>
<p>4 :  ['A' 'B' 'D' 'E']              ======>                 4  :  [1 1 0 1 1 0 0]</p>
<p>5 :  ['A' 'F' 'G']                                          5  :  [1 0 0 0 0 1 1]</p>
<p>6 :  ['A' 'B' 'D' 'E' 'F' 'G']                              6  :  [1 1 0 1 1 1 1]</p>
<p>7 :  ['A' 'B' 'E' 'F']                                      7  :  [1 1 0 0 1 1 0]</p>
<p>8 :  ['B' 'C' 'D' 'F']                                      8  :  [0 1 1 1 0 1 0]</p>
<p>9 :  ['A' 'E' 'F' 'G']                                      9  :  [1 0 0 0 1 1 1]</p>
<p>10 : ['B' 'D' 'E' 'F']                                      10 :  [0 1 0 1 1 1 0]</p>    

<p>The database consisting of string items is represented as a binary database as can be seen in the figure. There are as many columns as the number of single items. If there is an item in the line, it is represented by "1", otherwise it is represented by "0". The reason we keep the database as a binary database is that it is more costly to calculate over strings. All algorithms in this library work on this type of database.</p>
<p>SingleItems is a list of single items in the database. The reason why we keep this list is to show the results found in string type.</p>                                  