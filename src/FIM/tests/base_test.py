import numpy as np
import pandas as pd
from FIM.utils import TransactionEncoder


class AlgorithmErrors(object):
    """
    Class for testing algorithm errors.
    """

    def construct(self, algorithm) -> None:
        self.bool_array = np.array(
            [[True, True, False, True, False, True, False],
             [False, True, False, True, True, False, True],
             [False, False, False, True, True, True, False],
             [True, True, False, False, True, False, False],
             [False, True, True, True, False, True, False],
             [True, False, False, False, True, True, False],
             [True, True, True, True, True, True, False],
             [False, True, False, True, True, True, False],
             [False, True, True, False, True, False, True],
             [True, False, False, True, True, True, False],
             [False, True, True, True, True, False, False]])

        self.single_items = [
            'beef',
            'beer',
            'carrot',
            'crisps',
            'eggs',
            'onion',
            'tomato'
        ]

        self.df = pd.DataFrame(self.bool_array, columns=self.single_items)
        self.algorithm = algorithm

    def test_itemset_type(self):
        """
        Test if itemsets are of type frozenset.
        """
        res_indices_df = self.algorithm(self.df, show_colnames=False)
        for itemset in res_indices_df['itemsets']:
            self.assertIsInstance(itemset, frozenset) is True
        res_names_df = self.algorithm(self.df, show_colnames=True)
        for itemset in res_names_df['itemsets']:
            self.assertIsInstance(itemset, frozenset) is True

    def test_input_binary(self):
        """
        Test if input data is binary.

        Raises:
            ValueError: If input data is not binary.
        """
        for itemset in self.df.values:
            for item in itemset:
                if type(item) != np.bool_ or item not in [0, 1]:
                    raise ValueError("Input data must be a bool or binary pandas DataFrame.")


class TestExample1(object):
    """
    Class for testing basic example.
    """
    def construct(self, algorithm, dataset_array=None) -> None:
        if dataset_array is not None:
            self.dataset_array = dataset_array
        else:
            self.dataset_array = np.array(
                [[True, True, False, True, False, True, False],
                 [False, True, False, True, True, False, True],
                 [False, False, False, True, True, True, False],
                 [True, True, False, False, True, False, False],
                 [False, True, True, True, False, True, False],
                 [True, False, False, False, True, True, False],
                 [True, True, True, True, True, True, False],
                 [False, True, False, True, True, True, False],
                 [False, True, True, False, True, False, True],
                 [True, False, False, True, True, True, False],
                 [False, True, True, True, True, False, False]])

        self.single_items = [
            'beef',
            'beer',
            'carrot',
            'crisps',
            'eggs',
            'onion',
            'tomato'
        ]

        self.df = pd.DataFrame(self.dataset_array, columns=self.single_items)
        self.algorithm = algorithm

    def test_itemset_selection(self):
        """
        Test if itemsets are selected correctly.
        """
        res_df = self.algorithm(self.df, min_support=0.4, show_colnames=True)
        assert res_df.shape[0] == 10
        assert res_df[res_df['itemsets'] == frozenset({'crisps', 'beer'})].values.shape == (1, 2)
        assert res_df[res_df['itemsets'] == frozenset({'beer', 'crisps'})].values.shape == (1, 2)
        assert res_df[res_df['itemsets'] == {'crisps', 'beer'}].values.shape == (1, 2)
        assert res_df[res_df['itemsets'] == {'beer', 'crisps'}].values.shape == (1, 2)

    def test_default(self):
        """
        Test if algorithm work correctly.
        """
        res_df = self.algorithm(self.df, min_support=0.4, show_colnames=True)
        solution = pd.DataFrame(
            [
                [0.45454545454545453, frozenset({'beef'})],
                [0.7272727272727273, frozenset({'beer'})],
                [0.7272727272727273, frozenset({'crisps'})],
                [0.8181818181818182, frozenset({'eggs'})],
                [0.6363636363636364, frozenset({'onion'})],
                [0.5454545454545454, frozenset({'crisps', 'beer'})],
                [0.5454545454545454, frozenset({'eggs', 'beer'})],
                [0.5454545454545454, frozenset({'eggs', 'crisps'})],
                [0.5454545454545454, frozenset({'crisps', 'onion'})],
                [0.45454545454545453, frozenset({'eggs', 'onion'})]
            ],
            columns=['support', 'itemsets']
        )

        compare_dataframes(res_df, solution)

    def test_max_len(self):
        """
        Test if max_len parameter works correctly.
        """
        res_df = self.algorithm(self.df)
        max_len = np.max(res_df["itemsets"].apply(len))
        assert max_len == 2

        res_df_max_len_1 = self.algorithm(self.df, max_len=1)
        max_len = np.max(res_df_max_len_1["itemsets"].apply(len))
        assert max_len == 1


class TestExample2(object):
    """
    Class for testing basic example.
    """
    def construct(self, algorithm):
        dataset = [['a', 'b'], ['c'], ['e'], ['f'], ['c', 'd', 'f']]
        te = TransactionEncoder()
        self.df = te.fit_transform(dataset)
        self.algorithm = algorithm

    def test_default(self):
        """
        Test if algorithm work correctly.
        """
        res_df = self.algorithm(self.df, min_support=0.01, show_colnames=True)
        solution = pd.DataFrame(
            [
                [0.2, frozenset({'a'})],
                [0.2, frozenset({'b'})],
                [0.4, frozenset({'c'})],
                [0.2, frozenset({'d'})],
                [0.2, frozenset({'e'})],
                [0.4, frozenset({'f'})],
                [0.2, frozenset({'a', 'b'})],
                [0.2, frozenset({'c', 'd'})],
                [0.2, frozenset({'f', 'c'})],
                [0.2, frozenset({'f', 'd'})],
                [0.2, frozenset({'f', 'c', 'd'})]
            ],
            columns=['support', 'itemsets']
        )

        compare_dataframes(res_df, solution)


def compare_dataframes(df1, df2):
    """
    Compare two dataframes.

    Args:
        df1 (DataFrame)
        df2 (DataFrame)

    Raises:
        AssertionError: Different frequent itemsets
        AssertionError: Different support
    """
    itemsets1 = [sorted(list(i)) for i in df1["itemsets"]]
    itemsets2 = [sorted(list(i)) for i in df2["itemsets"]]

    rows1 = sorted(zip(itemsets1, df1["support"]))
    rows2 = sorted(zip(itemsets2, df2["support"]))

    for row1, row2 in zip(rows1, rows2):
        if row1[0] != row2[0]:
            msg = f"Expected different frequent itemsets\nx:{row1[0]}\ny:{row2[0]}"
            raise AssertionError(msg)
        elif row1[1] != row2[1]:
            msg = f"Expected different support\nx:{row1[1]}\ny:{row2[1]}"
            raise AssertionError(msg)
