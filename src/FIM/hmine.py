import math

import numpy as np
import pandas as pd

from FIM.utils import *

ITEMSETS_SIZE = 0.01

def hmine(df:pd.DataFrame, min_support:float=0.5, show_colnames:bool=True, max_len:int=None) -> dict:

    global ITEMSETS_SIZE
    ITEMSETS_SIZE = df.shape[0]
    
    if min_support <= 0.0:
        raise ValueError(
            "`min_support` must be a positive "
            "number within the interval `(0, 1]`. "
            "Got %s." % min_support
        )
    
    minsupp = math.ceil(min_support * len(df))
    FREQUENTITEMSETS = {}
    itemsets, single_items = itemsets_transformation(df)
    itemsets, single_items, single_items_support = itemset_optimisation(itemsets,
                                                                        single_items,
                                                                        minsupp)
    numeric_single_items = np.arange(len(single_items))

    for itm in numeric_single_items:
        if single_items_support[itm] >= minsupp:
            itm_support = single_items_support[itm] / ITEMSETS_SIZE
            FREQUENTITEMSETS[frozenset([single_items[itm]])] = itm_support
        if max_len == 1:
            continue
        # recursive call to hmine_miner
        FREQUENTITEMSETS = hmine_miner([itm],
                                       itemsets,
                                       minsupp,
                                       single_items,
                                       FREQUENTITEMSETS,
                                       max_len)

    res_df = pd.DataFrame([FREQUENTITEMSETS.values(), FREQUENTITEMSETS.keys()]).T
    res_df.columns = ["support", "itemsets"]
    
    if not show_colnames:
        mapping = {item: idx for idx, item in enumerate(df.columns)}
        res_df["itemsets"] = res_df["itemsets"].apply(
            lambda x: frozenset([mapping[i] for i in x])
        )

    return res_df

def hmine_miner(item:list,
                itemsets:np.array,
                minsupp:int,
                single_items:np.array,
                FREQUENTITEMSETS:dict,
                max_len:int=None) -> dict:
    """
    Driver function for the hmine algorithm.
    Recursively generates frequent itemsets.
    Also works for sparse matrix.
    egg: item = [1] -> [1,2] -> [1,2,3] -> [1,2,4] -> [1,2,5]

    Args:
        item (list): list of items
        itemsets (np.array): matrix of bools or binary
        minsup (int): minimum absolute support
        single_items (np.array): array of single items
        FREQUENTITEMSETS (dict): dictionary of frequent itemsets
        max_len (int): maximum length of frequent itemsets

    Returns:
        FREQUENTITEMSETS(dict): dictionary of frequent itemsets
    """
    if max_len and len(item) >= max_len:
        return FREQUENTITEMSETS
    projected_itemsets = create_projected_itemsets(item, itemsets)
    initial_supports = np.array(np.sum(projected_itemsets, axis=0)).reshape(-1)
    suffixes = np.nonzero(initial_supports >= minsupp)[0]
    suffixes = suffixes[np.nonzero(suffixes > item[-1])[0]]

    for suffix in suffixes:
        new_item = item.copy()
        new_item.append(suffix)
        new_item_support = initial_supports[suffix] / ITEMSETS_SIZE
        FREQUENTITEMSETS[frozenset(single_items[new_item])] = new_item_support

        FREQUENTITEMSETS = hmine_miner(new_item,
                                       projected_itemsets,
                                       minsupp,
                                       single_items,
                                       FREQUENTITEMSETS,
                                       max_len)
    return FREQUENTITEMSETS

def create_projected_itemsets(item: list, itemsets: np.array) -> np.array:
    """
    Creates the projected itemsets for the given item.
   
    Args:
        item (list): list of items
        itemsets (np.array): matrix of bools or binary

    Returns:
        projected_itemsets(np.array): projected itemsets for the given item
    """

    indices = np.nonzero(np.sum(itemsets[:, item], axis=1) == len(item))[0]
    projected_itemsets = itemsets[indices, :]
    return projected_itemsets
