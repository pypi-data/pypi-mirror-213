from typing import List

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from tqdm import tqdm


class CalculatorAUC:
    """CalculatorAUC class for calculating AUC."""

    def __init__(
        self,
        df: pd.DataFrame,
        selected_columns: List[str],
        weights_for_groups: pd.Series,
    ) -> None:
        """Initialize CalculatorAUC.

        :param df: dataframe
        :param selected_columns: selected columns
        :param weights_for_groups: weights for group
        """
        self.df = df
        self.selected_values = self.df[selected_columns].values
        self.weights_for_groups = weights_for_groups

    def get_overall_score(self, weights_for_equation: np.ndarray) -> None:
        """Calculate overall score.

        :param weights_for_equation: weights for equation
        """
        self.df["overall_score"] = np.product(
            self.selected_values**weights_for_equation, axis=1
        )

    def calculate_wuauc(
        self,
        groupby: str,
        weights_for_equation: np.ndarray,
        weights_for_groups: pd.Series,
        label_column: str = "label",
    ) -> float:
        """Calculate weighted user AUC.

        :param groupby: groupby column
        :param weights_for_equation: weights for equation
        :param weights_for_groups: weights for group
        :param label_column: label column
        :return: weighted user AUC
        """
        self.get_overall_score(weights_for_equation)
        grouped = self.df.groupby(groupby).apply(
            lambda x: float(roc_auc_score(x[label_column], x["overall_score"]))
        )
        counts_sorted = weights_for_groups.loc[grouped.index]
        wuauc = float(np.average(grouped, weights=counts_sorted.values))
        return wuauc

    def calculate_auc_triple_parameters(self, grid_interval: int) -> tuple:
        """Calculate AUC triple parameters.

        :param grid_interval: grid interval
        :return: tuple of W1, W2, WUAUC
        """
        w1_values = np.linspace(0, 1, grid_interval)
        w2_values = np.linspace(0, 1, grid_interval)
        W1, W2 = np.meshgrid(w1_values, w2_values)
        WUAUC = np.zeros_like(W1)

        for i in tqdm(range(W1.shape[0]), desc="Progress"):
            for j in range(W1.shape[1]):
                w1 = W1[i, j]
                w2 = W2[i, j]
                w3 = 1 - w1 - w2
                if w3 < 0:
                    WUAUC[i, j] = np.nan
                else:
                    WUAUC[i, j] = self.calculate_wuauc(
                        groupby="user_id",
                        weights_for_equation=np.array([w1, w2, w3]),
                        weights_for_groups=self.weights_for_groups,
                    )
        return W1, W2, WUAUC
