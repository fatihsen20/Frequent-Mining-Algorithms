# FIMProject - Frequent Itemset Algorithms and Frequent Sequence Mining Algorithms in Python

[![PyPI](https://img.shields.io/pypi/v/FIMProject.svg?style=flat-square&color=orange)](https://pypi.org/project/FIMProject/)
[![Downloads](https://static.pepy.tech/personalized-badge/fimproject?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/fimproject)
[![Downloads](https://static.pepy.tech/personalized-badge/fimproject?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads/Month)](https://pepy.tech/project/fimproject)
[![Downloads](https://static.pepy.tech/personalized-badge/fimproject?period=week&units=international_system&left_color=black&right_color=orange&left_text=Downloads/Week)](https://pepy.tech/project/fimproject)


## Installation
FIMProject requires Python 3.7 or newer, and the easiest way to install it is via
`pip`:
```shell
pip install FIMProject
```
## Simple Example
```py
from FIM import apriori
from FIM import association_rules
from FIM.utils import TransactionEncoder


# The apriori function expects data in a one-hot encoded pandas DataFrame.
# Suppose we have the following transaction data:
data = [['onion', 'beer', 'crisps', 'beef'],
        ['beer', 'tomato', 'crisps', 'eggs'],
        ['onion', 'crisps', 'eggs'],
        ['beer', 'eggs', 'beef'],
        ['onion', 'beer', 'carrot', 'crisps'],
        ['onion', 'eggs', 'beef'],
        ['onion', 'beer', 'carrot', 'crisps', 'eggs', 'beef'],
        ['onion', 'beer', 'crisps', 'eggs'],
        ['beer', 'tomato', 'carrot', 'eggs'],
        ['onion', 'crisps', 'eggs', 'beef'],
        ['beer', 'carrot', 'crisps', 'eggs']]

# We can transform it into the right format via the TransactionEncoder as follows:
te = TransactionEncoder()
df = te.fit_transform(data, set_pandas=True)

# Now, let us return the items and itemsets with at least 30% support:
freq_items = apriori(df, min_support=0.3)
# Now, let us return the association rules with freq_items df:
rules = association_rules(freq_items, metric="confidince", min_threshold=0.7)

```

## What is df?  

<p>
df is a pandas dataframe. It is a table of transactions. Each row is a transaction and each column is an item. The value of each cell is the number of items in the transaction.
</p>
