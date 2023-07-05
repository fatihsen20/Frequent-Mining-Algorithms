import collections
import math
import itertools

import numpy as np
import pandas as pd

from FIM.utils import (itemsets_transformation, 
                        itemset_optimisation)


def fpgrowth(df: pd.DataFrame,
            min_support: float = 0.5,
            show_colnames: bool = True,
            max_len: int = None
            ) -> pd.DataFrame:

    if min_support <= 0.0:
        raise ValueError(
            "`min_support` must be a positive "
            "number within the interval `(0, 1)`. "
            "Got %s." % min_support
        )
    
    minsupp = math.ceil(min_support * len(df))

    fptree, _ = construct_fptree(df, minsupp)
    generator = fpgrowth_driver(fptree, minsupp, max_len)
    res_df = generate_fis(generator, df.shape[0])

    if show_colnames:
        mapping = {idx: item for idx, item in enumerate(df.columns)}
        res_df["itemsets"] = res_df["itemsets"].apply(
            lambda x: frozenset([mapping[i] for i in x])
        )

    return res_df


def fpgrowth_driver(tree, minsupp, max_len):
    count = 0
    items = tree.nodes.keys()
    if tree.is_path():
        size_remain = len(items) + 1
        if max_len:
            size_remain = max_len - len(tree.conditional_items) + 1
        for i in range(1, size_remain):
            for transaction in itertools.combinations(items, i):
                count += 1
                support = min([tree.nodes[i][0].count for i in transaction])
                yield support, tree.conditional_items + list(transaction)
    
    elif not max_len or len(tree.conditional_items) < max_len:
        for item in items:
            count += 1
            support = sum([node.count for node in tree.nodes[item]])
            yield support, tree.conditional_items + [item]
    
    if not tree.is_path() and (not max_len or len(tree.conditional_items) < max_len):
        for item in items:
            conditional_tree = tree.conditional_tree(item, minsupp)
            for sup, iset in fpgrowth_driver(conditional_tree, minsupp, max_len):
                yield sup, iset

def construct_fptree(df, minsupp):
    num_of_transactions = df.shape[0]
    
    itemsets, _ = itemsets_transformation(df)

    item_support = np.array(np.sum(itemsets, axis=0))
    item_support = item_support.reshape(-1)
    items = np.nonzero(item_support >= minsupp)[0]

    indices = np.argsort(item_support[items])
    rank = {item: i for i, item in enumerate(items[indices])}

    fptree = FPTree(rank)
    for i in range(num_of_transactions):
        non_null = np.where(itemsets[i, :])[0]
        transaction = [item for item in non_null if item in rank]
        transaction.sort(key=rank.get, reverse=True)
        fptree.add_transaction(transaction)
    
    return fptree, rank


def generate_fis(generator, num_of_transaction):
    FREQUENTITEMSETS = {}
    for sup, items in generator:
        FREQUENTITEMSETS[frozenset(items)] = sup / num_of_transaction
    
    res_df = pd.DataFrame([FREQUENTITEMSETS.values(), FREQUENTITEMSETS.keys()]).T
    res_df.columns = ["support", "itemsets"] 
    return res_df


class FPTree(object):
    def __init__(self, rank=None):
        self.root = FPNode(None)
        self.nodes = collections.defaultdict(list)
        self.conditional_items = []
        self.rank = rank
    

    def conditional_tree(self, conditional_item: str or int, minsupp: int):
        branches = []
        count = collections.defaultdict(int)
        for node in self.nodes[conditional_item]:
            branch = node.itempath_from_root()
            branches.append(branch)
            for item in branch:
                count[item] += node.count
        items = [item for item in count if count[item] >= minsupp]
        items.sort(key=count.get)
        rank = {item: i for i, item in enumerate(items)}
        conditional_tree = FPTree(rank)

        if len(items) > 0:
            for idx, branch in enumerate(branches):
                branch = sorted([i for i in branch if i in rank], key=rank.get, reverse=True)
                conditional_tree.add_transaction(branch, self.nodes[conditional_item][idx].count)
            conditional_tree.conditional_items = self.conditional_items + [conditional_item]
        return conditional_tree

    def add_transaction(self, transaction, count=1):
        self.root.count += count

        if len(transaction) == 0:
            return
        
        index = 0
        node = self.root
        for item in transaction:
            if item in node.children:
                child = node.children[item]
                child.count += count
                node = child
                index += 1
            else:
                break
        for item in transaction[index: ]:
            child_node = FPNode(item, count, node)
            self.nodes[item].append(child_node)
            node = child_node
    

    def is_path(self):
        if len(self.root.children)>1:
            return False
        for i in self.nodes:
            if len(self.nodes[i])>1 or len(self.nodes[i][0].children) > 1:
                return False
        return True
    

class FPNode(object):
    def __init__(self, item, count=1, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = collections.defaultdict(FPNode)


    def itempath_from_root(self):
        path = []
        if self.item is None:
            return path
        node = self.parent
        while node.item is not None:
            path.append(node.item)
            node = node.parent
        path.reverse()
        return path

