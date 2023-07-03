from itertools import combinations

import numpy as np
import pandas as pd

def association_rules(df:pd.DataFrame,
                      metric:str="confidence",
                      min_threshold:float=0.7
                      ) -> pd.DataFrame:
    
    if not df.shape[0]:
        raise ValueError("Input DataFrame is empty. Frequent Itemsets are not generated.")
    
    if not all(col in df.columns for col in ["support", "itemsets"]):
        raise ValueError(
            "Input DataFrame must contain columns `support` and `itemsets`."
        )
    
    columns_ordered = [
        "antecedent support",
        "consequent support",
        "support",
        "confidence"
    ]

    def confidince_helper(antecedent_supp, consequent_supp, itemset_supp):
        return itemset_supp / antecedent_supp
    
    def lift_helper(antecedent_supp, consequent_supp, itemset_supp):
        return confidince_helper(antecedent_supp, consequent_supp, itemset_supp) / consequent_supp
    
    def kulc_helper(antecedent_supp, consequent_supp, itemset_supp):
        return 0.5 * ((itemset_supp / consequent_supp) + (itemset_supp / antecedent_supp))

    metrics = {
        "confidence": confidince_helper,
        "lift": lift_helper,
        "kulc": kulc_helper
    }

    if metric not in metrics.keys():
        raise ValueError(
            "Invalid metric '{}'. Metric must be in '{}'."
            .format(metric, " or ".join(list(metrics.keys())))       
        )
    
    freq_items_dict = df.set_index("itemsets").T.to_dict("records")[0]

    rule_antecedents = []
    rule_consequents = []
    rule_supports = []

    for key, value in freq_items_dict.items():
        itemset_size = len(key)
        if itemset_size > 1:

            for i in range(1, itemset_size):
                for item in combinations(key, i):
                    antecedent = frozenset(item)
                    consequent = key.difference(antecedent)
                    antecedent_support = freq_items_dict[antecedent]
                    consequent_support = freq_items_dict[consequent]
                    score = metrics[metric](antecedent_support, consequent_support, value)
                    if score >= min_threshold:
                        rule_antecedents.append(antecedent)
                        rule_consequents.append(consequent)
                        rule_supports.append([antecedent_support, consequent_support, value])
    
    if not rule_supports:
        return pd.DataFrame(columns=["antecedents", "consequents"] + columns_ordered)
    
    else:
        rule_supports = np.array(rule_supports).T.astype(float)
        df_res = pd.DataFrame(
            data=list(zip(rule_antecedents, rule_consequents)),
            columns=["antecedents", "consequents"],
        )
        df_res["antecedent support"] = rule_supports[0]
        df_res["consequent support"] = rule_supports[1]
        df_res["support"] = rule_supports[2]
        for key, value in metrics.items():
            df_res[key] = value(rule_supports[0], rule_supports[1], rule_supports[2])
            
        return df_res


def calc_confidence(itemset:frozenset, antecedent:frozenset, freq_items_dict:dict) -> float:
    itemset_support = freq_items_dict[itemset]
    antecedent_support = freq_items_dict[antecedent]
    return itemset_support / antecedent_support


    