import math

import numpy as np
import pandas as pd

from FIM.utils import *

ITEMSETS_SIZE = 0

def eclat(df:pd.DataFrame,
          min_support:float=0.5,
          show_colnames:bool=True,
          max_len:int=None
          ) -> dict:
    
    global ITEMSETS_SIZE
    ITEMSETS_SIZE = df.shape[0]

    if min_support <= 0.0:
        raise ValueError(
            "`min_support` must be a positive "
            "number within the interval `(0, 1]`. "
            "Got %s." % min_support
        )
    
    minsup = math.ceil(min_support * len(df))
    FREQUENTITEMSETS = {}
    itemsets, single_items = itemsets_transformation(df)
    itemsets, single_items, single_items_support = itemset_optimisation(itemsets,
                                                                        single_items,
                                                                        minsup)
    numeric_single_items = np.arange(len(single_items))

    vertical_db = list(HDtoVDB(itemsets))

    for i in numeric_single_items:
        item = np.array([i])
        FREQUENTITEMSETS[frozenset(single_items[item])] = len(vertical_db[i]) / ITEMSETS_SIZE
        if max_len == 1:
            continue
        FREQUENTITEMSETS = eclatMiner(vertical_db,
                                      item,
                                      minsup,
                                      single_items,
                                      FREQUENTITEMSETS,
                                      vertical_db[i],
                                      max_len)

    res_df = pd.DataFrame([FREQUENTITEMSETS.values(), FREQUENTITEMSETS.keys()]).T
    res_df.columns = ["support", "itemsets"]
    
    if not show_colnames:
        mapping = {item: idx for idx, item in enumerate(df.columns)}
        res_df["itemsets"] = res_df["itemsets"].apply(
            lambda x: frozenset([mapping[i] for i in x])
        )

    return res_df

def HDtoVDB(itemsets:np.array) -> list:
    """
        This method convert horizontal DB to Vertical DB.
    """
    NumOfItems = itemsets.shape[1]
    for i in range(0,NumOfItems):
        tmp = []
        for j in range(0, itemsets.shape[0]):
            transaction = itemsets[j]
            if transaction[i] != 0:
                tmp.append(j)
        yield tmp

def eclatMiner(vertical_db:list,
               item:np.array,
               minsupp:int,
               single_items:np.array,
               FREQUENTITEMSETS:dict,
               tid:list,
               max_len:int=None) -> dict:
    """
        This method includes the recursive part of the eclat algorithm.
    """

    tmp = item[-1]
    tid_ = []
    for itx in range(tmp+1,len(vertical_db)):
        tid_ = set(tid).intersection(vertical_db[itx])
        if len(tid_)>= minsupp:
            new_item = np.hstack((item,itx))
            if max_len is not None and len(new_item) > max_len:
                break
            FREQUENTITEMSETS[frozenset(single_items[new_item])] = len(tid_)/ITEMSETS_SIZE
            FREQUENTITEMSETS = eclatMiner(vertical_db, new_item, minsupp, single_items, FREQUENTITEMSETS, tid_)
            tid_ = []

    return FREQUENTITEMSETS
