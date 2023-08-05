import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomProduct
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_activity_component_regression, \
    create_predictive_property_component_classification
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from unittest_reinvent.scoring_tests.scoring_components.fixtures import celecoxib, random_compound


class Test_primary_multiplicative_function(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
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
                                            smiles=[],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1ccccc1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, qed_score, custom_alerts, matching_substructure])

    def test_primary_multiplicative_1(self):
        score = self.sf_state.get_final_score(smiles=[celecoxib])
        self.assertAlmostEqual(score.total_score[0], 0.481, 3)

    def test_primary_multiplicative_2(self):
        score = self.sf_state.get_final_score(smiles=[random_compound])
        self.assertAlmostEqual(score.total_score[0], 0.172, 3)


class Test_primary_multiplicative_with_alert(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
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
                                            smiles=['CCCOOO'],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1ccccc1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, qed_score, custom_alerts, matching_substructure])

    def test_primary_mult_with_alert_1(self):
        score = self.sf_state.get_final_score(smiles=['CCCOOO'])
        self.assertEqual(score.total_score, 0)

    def test_primary_mult_with_alert_2(self):
        score = self.sf_state.get_final_score(smiles=[celecoxib])
        self.assertAlmostEqual(score.total_score[0], 0.481, 3)


class Test_primary_mult_with_alert_no_sigm_trans(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
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
                                            smiles=['CCCOOO'],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1ccccc1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, qed_score, custom_alerts, matching_substructure])

    def test_primary_mult_with_alert_no_transform_1(self):
        score = self.sf_state.get_final_score(smiles=['CCCOOO'])
        self.assertEqual(score.total_score, 0)

    def test_primary_mult_with_alert_no_transform_2(self):
        score = self.sf_state.get_final_score(smiles=[celecoxib])
        self.assertAlmostEqual(score.total_score[0], 0.481, 3)

    def test_primary_mult_with_alert_no_transform_3(self):
        score = self.sf_state.get_final_score(smiles=['CCCOOOCCCOOO'])
        self.assertEqual(score.total_score, 0)


class Test_primary_mult_with_no_activity(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts_name",
                                            weight=1.,
                                            smiles=['CCCOOO'],
                                            model_path="",
                                            specific_parameters={})
        ts_parameters = ComponentParameters(component_type=enum.TANIMOTO_SIMILARITY,
                                            name="tanimoto_similarity",
                                            weight=1.,
                                            smiles=[random_compound],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1ccccc1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[ts_parameters, matching_substructure, custom_alerts])

    def test_primary_mult_with_no_activity_1(self):
        score = self.sf_state.get_final_score(smiles=['CCCOOO'])
        self.assertEqual(score.total_score, 0)

    def test_primary_mult_with_no_activity_2(self):
        score = self.sf_state.get_final_score(smiles=[celecoxib])
        self.assertAlmostEqual(score.total_score[0], 0.0504, 3)

    def test_primary_mult_with_no_activity_3(self):
        score = self.sf_state.get_final_score(smiles=['CCCOOOCCCOOO'])
        self.assertEqual(score.total_score, 0)


class Test_primary_mult_with_prediction_classification_and_regression_alert(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        activity = create_activity_component_regression()
        sci_activity = create_predictive_property_component_classification()
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score_name",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts_name",
                                            weight=1.,
                                            smiles=['CCCOOO'],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1ccccc1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[activity, qed_score, custom_alerts, matching_substructure, sci_activity])

    def test_primary_mult_with_reg_class_1(self):
        score = self.sf_state.get_final_score(smiles=[celecoxib])
        self.assertAlmostEqual(score.total_score[0], 0.438, 3)



class Test_primary_mult_with_no_activity_2(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts_name",
                                            weight=1.,
                                            smiles=['CCCOOO'],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=["c1ccccc1"],
                                                    model_path="",
                                                    specific_parameters={})
        self.sf_state = CustomProduct(
            parameters=[matching_substructure, custom_alerts])

    def test_primary_mult_with_alert_match_1(self):
        score = self.sf_state.get_final_score(smiles=['CCCOOO'])
        self.assertEqual(score.total_score, 0)

    def test_primary_mult_with_alert_match_2(self):
        score = self.sf_state.get_final_score(smiles=[celecoxib])
        self.assertAlmostEqual(score.total_score[0], 1, 3)

    def test_primary_mult_with_alert_match_3(self):
        score = self.sf_state.get_final_score(smiles=['CCCOOOCCCOOO'])
        self.assertEqual(score.total_score, 0)
