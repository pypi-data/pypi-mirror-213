from __future__ import annotations
from typing import List, Union, Tuple, TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from clayrs.content_analyzer.ratings_manager.ratings import Prediction, Rank, Ratings
    from clayrs.evaluation.metrics.metrics import Metric

from clayrs.evaluation.eval_pipeline_modules.metric_evaluator import MetricEvaluator
from clayrs.utils.const import logger


class EvalModel:
    """
    Class for evaluating a recommender system.

    The Evaluation module needs the following parameters:

    *   A list of computed rank/predictions (in case multiple splits must be evaluated)
    *   A list of truths (in case multiple splits must be evaluated)
    *   List of metrics to compute

    Obviously the list of computed rank/predictions and list of truths must have the same length,
    and the rank/prediction in position $i$ will be compared with the truth at position $i$

    Examples:

        >>> import clayrs.evaluation as eva
        >>>
        >>> em = eva.EvalModel(
        >>>         pred_list=rank_list,
        >>>         truth_list=truth_list,
        >>>         metric_list=[
        >>>             eva.NDCG(),
        >>>             eva.Precision()
        >>>             eva.RecallAtK(k=5, sys_average='micro')
        >>>         ]
        >>> )

    Then call the fit() method of the instantiated EvalModel to perform the actual evaluation

    Args:
        pred_list: Recommendations list to evaluate. It's a list in case multiple splits must be evaluated. Both Rank
            objects (where items are ordered and the score is not relevant) or Prediction objects (where the score
             predicted is the predicted rating for the user regarding a certain item) can be evaluated
        truth_list: Ground truths list used to compare recommendations. It's a list in case multiple splits must
            be evaluated.
        metric_list: List of metrics that will be used to evaluate recommendation list specified

    Raises:
        ValueError: ValueError is raised in case the pred_list and truth_list are empty or have different length
    """
    def __init__(self,
                 pred_list: Union[List[Prediction], List[Rank]],
                 truth_list: List[Ratings],
                 metric_list: List[Metric]):

        if len(pred_list) == 0 and len(truth_list) == 0:
            raise ValueError("List containing predictions and list containing ground truths are empty!")
        elif len(pred_list) != len(truth_list):
            raise ValueError("List containing predictions and list containing ground truths must have the same length!")

        self._pred_list = pred_list
        self._truth_list = truth_list
        self._metric_list = metric_list

        self._yaml_report_result = None

    @property
    def pred_list(self) -> Union[List[Prediction], List[Rank]]:
        """
        List containing recommendations frame

        Returns:
            The list containing recommendations frame
        """
        return self._pred_list

    @property
    def truth_list(self) -> List[Ratings]:
        """
        List containing ground truths

        Returns:
            The list containing ground truths
        """
        return self._truth_list

    @property
    def metric_list(self) -> List[Metric]:
        """
        List of metrics used to evaluate recommendation lists

        Returns:
            The list containing all metrics
        """
        return self._metric_list

    def append_metric(self, metric: Metric):
        """
        Append a metric to the metric list that will be used to evaluate recommendation lists

        Args:
            metric: Metric to append to the metric list
        """
        self._metric_list.append(metric)

    def fit(self, user_id_list: list = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        This method performs the actual evaluation of the recommendation frames passed as input in the constructor of
        the class

        In case you want to perform evaluation for selected users, specify their ids parameter of this method.
        Otherwise, all users in the recommendation frames will be considered in the evaluation process

        Examples:

            >>> import clayrs.evaluation as eva
            >>> selected_users = ['u1', 'u22', 'u3'] # (1)
            >>> em = eva.EvalModel(
            >>>         pred_list,
            >>>         truth_list,
            >>>         metric_list=[eva.Precision(), eva.Recall()]
            >>> )
            >>> em.fit(selected_users)

        The method returns two pandas DataFrame: one containing ***system results*** for every metric in the metric
        list, one containing ***users results*** for every metric eligible

        Returns:
            The first DataFrame contains the **system result** for every metric inside the metric_list

            The second DataFrame contains every **user results** for every metric eligible inside the metric_list
        """
        logger.info('Performing evaluation on metrics chosen')

        pred_list = self._pred_list
        truth_list = self._truth_list

        if user_id_list is not None:
            user_id_list_set = set([str(user_id) for user_id in user_id_list])

            pred_list = [pred.filter_ratings(user_id_list_set) for pred in self._pred_list]
            truth_list = [truth.filter_ratings(user_id_list_set) for truth in self._truth_list]

        sys_result, users_result = MetricEvaluator(pred_list, truth_list).eval_metrics(self.metric_list)

        # we save the sys result for report yaml
        self._yaml_report_result = sys_result.to_dict(orient='index')

        return sys_result, users_result

    def __repr__(self):
        return f'EvalModel(pred_list={self._pred_list}, truth_list={self._truth_list},' \
               f' metric_list={self._metric_list}'
