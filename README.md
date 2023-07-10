 # How to Install
```shell
pip install FIMProject
```
# How to Use It
```python
from FIM import apriori, association_rules

freq_items = apriori(df, min_support=0.6, show_colnames=True)
rules = association_rules(freq_items, metric="confidince", min_threshold=0.7)

```

# What is df?  

<p>
df is a pandas dataframe. It is a table of transactions. Each row is a transaction and each column is an item. The value of each cell is the number of items in the transaction.
</p>
