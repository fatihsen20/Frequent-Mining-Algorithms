import math

import numpy as np
import pandas as pd

from FIM.utils import *


def apriori(df: pd.DataFrame,
            min_support: float = 0.5,
            show_colnames: bool = True,
            max_len: int = None
            ) -> dict:
    """
    This method implements the Apriori algorithm.

    Args:
        df (pd.DataFrame): Pandas DataFrame with the transaction database format.
        min_support (float, optional): A float between 0 and 1 for minumum support of the itemsets returned. Defaults to 0.5.
        show_colnames (bool, optional): If True, the itemsets in the "itemsets" column
            will be shown as strings with the column names from the original DataFrame. Defaults to True.
        max_len (int, optional): Maximum length of the itemsets generated. Defaults to None.

    Raises:
        ValueError: If `min_support` is not a positive number within the interval `(0, 1)`.

    Returns:
        pd.DataFrame: Pandas DataFrame with the itemsets (as strings if `show_colnames=True`) and their corresponding support values.
    """

    if min_support <= 0.0:
        raise ValueError(
            "`min_support` must be a positive "
            "number within the interval `(0, 1)`. "
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
        abs_supp = calc_absolute_supp(itemsets, item)
        if minsup <= abs_supp:
            Fk.append(item)
            FREQUENTITEMSETS[frozenset(single_items[item])] = abs_supp / len(df)

    if max_len != 1:
        while True:
            Fkm1 = Fk
            Fk = []
            Ck = candidate_generation(Fkm1)
            for i in range(0, len(Ck)):
                candidate_item = Ck[i]
                if max_len is not None and len(candidate_item) > max_len:
                    break
                abs_supp = calc_absolute_supp(itemsets, candidate_item)
                if minsup <= abs_supp:
                    Fk.append(candidate_item)
                    FREQUENTITEMSETS[frozenset(single_items[candidate_item])] = abs_supp / len(df)
            if len(Ck) * len(Fk) == 0:
                break

    res_df = pd.DataFrame([FREQUENTITEMSETS.values(), FREQUENTITEMSETS.keys()]).T
    res_df.columns = ["support", "itemsets"]

    if not show_colnames:
        mapping = {item: idx for idx, item in enumerate(df.columns)}
        res_df["itemsets"] = res_df["itemsets"].apply(
            lambda x: frozenset([mapping[i] for i in x])
        )

    return res_df


def does_exist(itm: np.array,
               transaction: np.array
               ) -> bool:
    """
    This method checks if the itemset exists in the transaction.

    Args:
        itm (np.array): Candidate itemset.
        transaction (np.array): Transaction.

    Returns:
        bool: True if the itemset exists in the transaction, False not exists.
    """
    return True if sum(transaction[itm]) == len(itm) else False


def calc_absolute_supp(itemsets: np.array,
                       itm: np.array
                       ) -> int:
    """
    This method calculates the absolute support of the itemset.

    Args:
        itemsets (np.array): Transaction Database.
        itm (np.array): Candidate itemset.

    Returns:
        int: Absolute support of the itemset.
    """
    abs_supp = 0
    for i in range(0, itemsets.shape[0]):
        transaction = itemsets[i, :]
        if does_exist(itm, transaction):
            abs_supp += 1
    return abs_supp


def candidate_generation(Fkm1: list) -> list:
    """
    This method generates the candidate itemsets. egg.
    Fkm1 = [[1,2],[1,3],[2,3]] -> Ck = [[1,2,3]]

    Args:
        Fkm1 (list): Frequent itemsets of size k-1.(k = Size of the candidate itemsets.)

    Returns:
        list: Candidate itemsets of size k.
    """
    Ck = []
    for i in range(0, len(Fkm1) - 1):
        for j in range(i + 1, len(Fkm1)):
            itemset1 = Fkm1[i]
            itemset2 = Fkm1[j]
            if len(itemset1) == 1:
                NewItem = np.hstack((np.array(itemset1), np.array(itemset2[-1])))
                Ck.append(NewItem)
            else:
                if sum(abs(itemset1[1:] - itemset2[:-1])) == 0:
                    NewItem = np.hstack((np.array(itemset1), np.array(itemset2[-1])))
                    Ck.append(NewItem)
    return Ck
