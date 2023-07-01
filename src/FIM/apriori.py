import math

import numpy as np
import pandas as pd

from FIM.utils import *

def apriori(df:pd.DataFrame, min_support:float=0.5, show_colnames:bool=True, max_len:int=None) -> dict:

    if min_support <= 0.0:
        raise ValueError(
            "`min_support` must be a positive "
            "number within the interval `(0, 1]`. "
            "Got %s." % min_support
        )

    minsup = math.ceil(min_support * len(df))
    FREQUENTITEMSETS = {}
    itemsets, single_items = itemsets_transformation(df)
    itemsets, single_items, single_items_support = itemset_optimisation(itemsets, single_items, minsup)
    numeric_single_items = np.arange(len(single_items))

    Fk = []

    for i in numeric_single_items:
        item = np.array([i])
        abs_supp = calcAbsSup(itemsets, item)

        if minsup <= abs_supp:
            Fk.append(item)
            FREQUENTITEMSETS[frozenset(single_items[item])] = abs_supp / len(df)
    
    if max_len != 1:
        while True:
            Fkm1 = Fk ; Fk = []
            Ck = candidateGeneration(Fkm1)
            for i in range(0,len(Ck)):
                candidate_item = Ck[i]
                if max_len is not None and len(candidate_item) > max_len:
                    break
                abs_supp = calcAbsSup(itemsets, candidate_item)
                if minsup <= abs_supp:
                    Fk.append(candidate_item)
                    FREQUENTITEMSETS[frozenset(single_items[candidate_item])] = abs_supp / len(df)
            if len(Ck)* len(Fk) == 0:
                break
    
    res_df = pd.DataFrame([FREQUENTITEMSETS.values(), FREQUENTITEMSETS.keys()]).T
    res_df.columns = ["support", "itemsets"]

    if not show_colnames:
        mapping = {item: idx for idx, item in enumerate(df.columns)}
        res_df["itemsets"] = res_df["itemsets"].apply(
            lambda x: frozenset([mapping[i] for i in x])
        )
    return res_df

def doesExist(itm,transaction) -> bool:
    """
        This method checks the presence of itm in transaction.
    """
    if sum(transaction[itm]) == len(itm):     
        E=True
    else:     
        E=False

    return E

def calcAbsSup(DATABASE, itm) -> int: 
    """
        This method calc the itm absolute support.
    """
    AbsSupp = 0
    for i in range(0, DATABASE.shape[0]):
        transaction = DATABASE[i,:]
        if doesExist(itm, transaction):
            AbsSupp += 1
        
    return AbsSupp
    
def candidateGeneration(Fkm1) -> list:
    Ck= [] 
    for i in range(0, len(Fkm1)-1):
        for j in range(i+1,len(Fkm1)):
            itemset1 = Fkm1[i]
            itemset2 = Fkm1[j]
                
            if len(itemset1) == 1:
                NewItem = np.hstack((np.array(itemset1),np.array(itemset2[-1])))
                Ck.append(NewItem)
            else:
                if sum(abs(itemset1[1:]-itemset2[:-1])) == 0:
                    NewItem = np.hstack((np.array(itemset1),np.array(itemset2[-1])))
                    Ck.append(NewItem)              
    return Ck