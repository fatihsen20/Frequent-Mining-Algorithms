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

<p>The database consisting of string items is represented as a binary database as can be seen in the figure. There are as many columns as the number of single items. If there is an item in the line, it is represented by "1", otherwise it is represented by "0". The reason we keep the database as a binary database is that it is more costly to calculate over strings. All algorithms in this library work on this type of database.</p>
<p>SingleItems is a list of single items in the database. The reason why we keep this list is to show the results found in string type.</p>           

<table>
  <tr>
    <th>Index</th>
    <th>Transaction</th>
  </tr>
  <tr>
  	<td>0</td>
    <td>['A' 'B' 'E' 'G']</td>
  </tr>
  <tr>
    <td>1</td>
    <td>['B' 'C' 'E' 'F']</td>
  </tr>
  <tr>
    <td>2</td>
    <td>['A' 'E' 'F']</td>
  </tr>
  <tr>
    <td>3</td>
    <td>['B' 'F' 'G']</td>
  </tr>
  <tr>
    <td>4</td>
    <td>['A' 'B' 'D' 'E']</td>
  </tr>
  <tr>
    <td>5</td>
    <td>['A' 'F' 'G']</td>
  </tr>
  <tr>
    <td>6</td>
    <td>['A' 'B' 'D' 'E' 'F' 'G']</td>
  </tr>
  <tr>
    <td>7</td>
    <td>['A' 'B' 'E' 'F']</td>
  </tr>
  <tr>
    <td>8</td>
    <td>['B' 'C' 'D' 'F']</td>
  </tr>
  <tr>
    <td>9</td>
    <td>['A' 'E' 'F' 'G']</td>
  </tr>
  <tr>
    <td>10</td>
    <td>['B' 'D' 'E' 'F']</td>
  </tr>
</table>
</div>
<div>
<table>
  <tr>
    <th>Index</th>
    <th>Transaction</th>
  </tr>
  <tr>
  	<td>0</td>
    <td>[1 1 0 0 1 0 1]</td>
  </tr>
  <tr>
    <td>1</td>
    <td>[0 1 1 0 1 1 0]</td>
  </tr>
  <tr>
    <td>2</td>
    <td>[1 0 0 0 1 1 0]</td>
  </tr>
  <tr>
    <td>3</td>
    <td>[0 1 0 0 0 1 1]</td>
  </tr>
  <tr>
    <td>4</td>
    <td>[1 1 0 1 1 0 0]</td>
  </tr>
  <tr>
    <td>5</td>
    <td>[1 0 0 0 0 1 1]</td>
  </tr>
  <tr>
    <td>6</td>
    <td>[1 1 0 1 1 1 1]</td>
  </tr>
  <tr>
    <td>7</td>
    <td>[1 1 0 0 1 1 0]</td>
  </tr>
  <tr>
    <td>8</td>
    <td>[0 1 1 1 0 1 0]</td>
  </tr>
  <tr>
    <td>9</td>
    <td>[1 0 0 0 1 1 1]</td>
  </tr>
  <tr>
    <td>10</td>
    <td>[0 1 0 1 1 1 0]</td>
  </tr>
</table>

<p>SingleItems:["A","B","C","D","E","F","G"]</p>
