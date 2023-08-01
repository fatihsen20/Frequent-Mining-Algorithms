import unittest

import numpy as np
import pandas as pd

from base_test import (
    AlgorithmErrors,
    TestExample1,
    TestExample2,
    compare_dataframes,
)

from FIM import apriori, eclat, fpgrowth, hmine
from FIM.utils import TransactionEncoder


class TestAlgorithmErrors(unittest.TestCase, AlgorithmErrors):
    def setUp(self):
        AlgorithmErrors.construct(self, algorithm=hmine)


class TestHmine1(unittest.TestCase, TestExample1):
    def setUp(self):
        TestExample1.construct(self, algorithm=hmine)


class TestHmine2(unittest.TestCase, TestExample2):
    def setUp(self):
        TestExample2.construct(self, algorithm=hmine)


class TestHmineBinaryOutput(unittest.TestCase, TestExample1):
    def setUp(self):
        db_array = np.array([
                            [1, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 1, 0, 1],
                            [0, 0, 0, 1, 1, 1, 0],
                            [1, 1, 0, 0, 1, 0, 0],
                            [0, 1, 1, 1, 0, 1, 0],
                            [1, 0, 0, 0, 1, 1, 0],
                            [1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 0, 1, 1, 1, 0],
                            [0, 1, 1, 0, 1, 0, 1],
                            [1, 0, 0, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 0, 0]
                            ])
        TestExample1.construct(self, algorithm=hmine, dataset_array=db_array)


class TestCorrect(unittest.TestCase):
    def setUp(self):
        dataset = [['a', 'b'], ['d'], ['c'], ['e'], ['b'], ['f'], ['c', 'd', 'f']]
        te = TransactionEncoder()
        self.df = te.fit_transform(dataset)

    def test_compare_correct(self):
        self.setUp()
        solution = pd.DataFrame(
            [[0.14285714285714285, frozenset({'a'})],
             [0.2857142857142857, frozenset({'b'})],
             [0.2857142857142857, frozenset({'c'})],
             [0.2857142857142857, frozenset({'d'})],
             [0.14285714285714285, frozenset({'e'})],
             [0.2857142857142857, frozenset({'f'})],
             [0.14285714285714285, frozenset({'a', 'b'})],
             [0.14285714285714285, frozenset({'c', 'd'})],
             [0.14285714285714285, frozenset({'f', 'c'})],
             [0.14285714285714285, frozenset({'f', 'd'})],
             [0.14285714285714285, frozenset({'f', 'c', 'd'})]],
            columns=['support', 'itemsets'])

        algorithms = {
            apriori: None,
            eclat: None,
            fpgrowth: None,
            hmine: None
        }
        for algorithm in algorithms.keys():
            res_df = algorithm(self.df, min_support=0.01, show_colnames=True)
            compare_dataframes(res_df, solution)
            algorithms[algorithm] = res_df

        compare_dataframes(algorithms[hmine], algorithms[apriori])
        compare_dataframes(algorithms[hmine], algorithms[fpgrowth])
        compare_dataframes(algorithms[hmine], algorithms[eclat])
