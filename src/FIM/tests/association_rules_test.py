import unittest

import numpy as np
import pandas as pd

from FIM import apriori, association_rules


class AssociationRulesBase(object):
    def construct(self, metric='confidince'):
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
        self.metric = metric
        self.freq_items_df = apriori(self.df, min_support=0.3, show_colnames=True)
        self.columns = [
            'antecedents',
            'consequents',
            'antecedent support',
            'consequent support',
            'support',
            'confidence',
            'lift',
            'kulc'
        ]


class AssociationRulesErrors(unittest.TestCase, AssociationRulesBase):
    """
    Class for testing association rules errors.
    """
    def setUp(self, metric='confidence'):
        AssociationRulesBase.construct(self, metric)
    
    def test_data_type(self):
        """
        Test if itemsets are of type frozenset.
        """
        res_df = association_rules(self.freq_items_df)
        for antecent in res_df['antecedents']:
            self.assertIsInstance(antecent, frozenset)
        for consequent in res_df['consequents']:
            self.assertIsInstance(consequent, frozenset)
    
    def test_empty_result(self):
        solution = pd.DataFrame(columns=['antecedents', 'consequents'])
        res_df = association_rules(self.freq_items_df, min_threshold=5)
        assert res_df.equals(solution)
    
    def test_confidence(self):
        self.metric = 'confidence'
        res_df = association_rules(self.freq_items_df, metric=self.metric, min_threshold=0.7)
        assert res_df.shape[0] == 12
    
    def test_lift(self):
        self.metric = 'lift'
        res_df = association_rules(self.freq_items_df, self.metric, min_threshold=1.2)
        assert res_df.shape[0] == 6
    
    def test_kulc(self):
        self.metric = 'kulc'
        res_df = association_rules(self.freq_items_df, self.metric, min_threshold=0.8)
        assert res_df.shape[0] == 2
    
    def test_default(self):
        """
        Test association rules with default values.
        """
        solution = pd.DataFrame(
            [[frozenset({'beef'}), frozenset({'eggs'}), 0.45454545454545453, 
              0.8181818181818182, 0.36363636363636365, 0.8, 0.9777777777777777,0.6222222222222222],
             [frozenset({'beef'}), frozenset({'onion'}), 0.45454545454545453,
              0.6363636363636364, 0.36363636363636365, 0.8, 1.2571428571428573, 0.6857142857142857],
             [frozenset({'carrot'}), frozenset({'beer'}), 0.36363636363636365, 
              0.7272727272727273, 0.36363636363636365, 1.0, 1.375, 0.75],
             [frozenset({'crisps'}), frozenset({'beer'}), 0.7272727272727273, 0.7272727272727273,
              0.5454545454545454, 0.7499999999999999, 1.0312499999999998, 0.7499999999999999],
             [frozenset({'beer'}), frozenset({'crisps'}), 0.7272727272727273, 0.7272727272727273,
              0.5454545454545454, 0.7499999999999999, 1.0312499999999998, 0.7499999999999999],
             [frozenset({'beer'}), frozenset({'eggs'}), 0.7272727272727273, 0.8181818181818182, 
              0.5454545454545454, 0.7499999999999999, 0.9166666666666665, 0.7083333333333333],
             [frozenset({'crisps'}), frozenset({'eggs'}), 0.7272727272727273, 0.8181818181818182,
              0.5454545454545454, 0.7499999999999999, 0.9166666666666665, 0.7083333333333333],
             [frozenset({'crisps'}), frozenset({'onion'}), 0.7272727272727273, 0.6363636363636364,
              0.5454545454545454, 0.7499999999999999, 1.1785714285714284, 0.8035714285714285],
             [frozenset({'onion'}), frozenset({'crisps'}), 0.6363636363636364, 0.7272727272727273,
              0.5454545454545454, 0.8571428571428571, 1.1785714285714284, 0.8035714285714285],
             [frozenset({'onion'}), frozenset({'eggs'}), 0.6363636363636364, 0.8181818181818182,
              0.45454545454545453, 0.7142857142857143, 0.873015873015873, 0.6349206349206349],
             [frozenset({'onion', 'beer'}), frozenset({'crisps'}), 0.36363636363636365,
              0.7272727272727273, 0.36363636363636365, 1.0, 1.375, 0.75],
             [frozenset({'onion', 'eggs'}), frozenset({'crisps'}), 0.45454545454545453,
              0.7272727272727273, 0.36363636363636365, 0.8, 1.1, 0.65]],
            columns=self.columns)
 
        res_df = association_rules(self.freq_items_df)
        assert res_df.equals(solution), res_df

