import numpy as np
import pandas as pd


def itemsets_transformation(df: pd.DataFrame) -> tuple:

    assert len(df) != 0, "Dataframe is empty"
    itemsets = df.values
    single_items = np.array(df.columns)

    return itemsets, single_items


def itemset_optimisation(
    itemsets: np.array,
    single_items: np.array,
    minsup: int,
) -> tuple:
    """
    Downward-closure property of H-Mine algorithm.
        Optimizes the itemsets matrix by removing items that do not
        meet the minimum support.

    Args:
        itemsets (np.array): matrix of bools or binary
        single_items (np.array): array of single items
        minsup (int): minimum absolute support

    Returns:
        itemsets (np.array): reduced itemsets matrix of bools or binary
        single_items (np.array): reduced array of single items
        single_items_support (np.array): reduced single items support
    """

    single_items_support = np.array(np.sum(itemsets, axis=0)).reshape(-1)
    items = np.nonzero(single_items_support >= minsup)[0]
    itemsets = itemsets[:, items]
    single_items = single_items[items]
    single_items_support = single_items_support[items]

    return itemsets, single_items, single_items_support


class TransactionEncoder():
    def __init__(self) -> None:
        pass

    def fit(self, itemsets: list) -> object:
        """
        This method creates a list of unique items in the dataset.

        Args:
            itemsets (list): dataset
        """
        unique_items = []
        for transaction in itemsets:
            for item in transaction:
                if item not in unique_items:
                    unique_items.append(item)
        self.columns = sorted(unique_items)
        self.columns_dict = {item: idx for idx, item in enumerate(self.columns)}
        return self

    def transform(self, itemsets: list, set_pandas=True) -> np.array:
        """
        This method converts the dataset into a binary matrix.

        Args:
            itemsets (list): dataset
        """
        output = np.zeros((len(itemsets), len(self.columns)), dtype=bool)
        for idx, transaction in enumerate(itemsets):
            for item in transaction:
                if item in self.columns_dict:
                    output[idx, self.columns_dict[item]] = True
        if set_pandas:
            return pd.DataFrame(output, columns=self.columns)
        return output

    def inverse_transform(self, itemsets: list) -> list:
        """
        This method converts the binary matrix into a dataset.

        Args:
            itemsets (list): binary matrix
        """
        output = []
        for transaction in itemsets:
            tmp = []
            for idx, item in enumerate(transaction):
                if item:
                    tmp.append(self.columns[idx])
            output.append(tmp)
        return output

    def fit_transform(self, itemsets: list, set_pandas=True) -> np.array:
        """
        This method combines fit and transform methods.

        Args:
            itemsets (list): dataset
        """
        return self.fit(itemsets).transform(itemsets, set_pandas=set_pandas)
