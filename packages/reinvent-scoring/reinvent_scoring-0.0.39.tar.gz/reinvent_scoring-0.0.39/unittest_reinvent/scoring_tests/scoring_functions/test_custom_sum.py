import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import \
    create_predictive_property_component_regression, create_activity_component_regression
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from unittest_reinvent.scoring_tests.scoring_components.fixtures import celecoxib, random_compound


class Test_custom_sum(unittest.TestCase):

    def setUp(self):
        enum = ScoringFunctionComponentNameEnum()
        predictive_property = create_predictive_property_component_regression()
        activity = create_activity_component_regression()
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score_name",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts_name",
                                            weight=1.,
                                            smiles=["CCCOOO"],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1ccccc1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_instance = CustomSum(
            parameters=[activity, qed_score, custom_alerts, matching_substructure, predictive_property])

    def test_special_selectivity_multiplicative_no_sigm_trans_1(self):
        score = self.sf_instance.get_final_score(smiles=[celecoxib])
        self.assertAlmostEqual(score.total_score[0], 0.456, 3)

    def test_special_selectivity_multiplicative_no_sigm_trans_2(self):
        score = self.sf_instance.get_final_score(smiles=[random_compound])
        self.assertAlmostEqual(score.total_score[0], 0.166, 3)

    def test_special_selectivity_multiplicative_no_sigm_trans_3(self):
        score = self.sf_instance.get_final_score(smiles=["CCCOOOCCCOOO"])
        self.assertEqual(score.total_score, 0)

    def test_special_selectivity_multiplicative_no_sigm_trans_4(self):
        score = self.sf_instance.get_final_score(smiles=["C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)O"])
        self.assertAlmostEqual(score.total_score[0], 0.151, 3)

