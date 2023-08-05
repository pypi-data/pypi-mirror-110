import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomProduct
from reinvent_scoring.scoring.score_summary import FinalSummary
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_activity_component_regression, \
    create_offtarget_activity_component_regression, create_custom_alerts_configuration
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import TransformationTypeEnum
from unittest_reinvent.scoring_tests.scoring_components.fixtures import celecoxib


class Test_primary_multiplicative_with_desirability_component(unittest.TestCase):
    def setUp(self):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        enum = ScoringFunctionComponentNameEnum()
        activity = create_activity_component_regression()
        activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        activity.specific_parameters[csp_enum.COEF_SI] = 150.
        activity.specific_parameters[csp_enum.COEF_SE] = 150.
        off_activity = create_offtarget_activity_component_regression()

        delta_params = {
            "high": 3.0,
            "k": 0.25,
            "low": 0.0,
            "transformation": True,
            "transformation_type": "sigmoid"
        }

        selectivity = ComponentParameters(component_type=enum.SELECTIVITY,
                                           name="desirability",
                                           weight=1.,
                                           smiles=[],
                                           model_path="",
                                           specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": off_activity.model_path,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity.specific_parameters,
                                               "delta_transformation_parameters": delta_params
                                           })
        qed_score = ComponentParameters(component_type=enum.QED_SCORE,
                                        name="qed_score",
                                        weight=1.,
                                        smiles=[],
                                        model_path="",
                                        specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure",
                                                    weight=1.,
                                                    smiles=["c1ccccc1"],
                                                    model_path="",
                                                    specific_parameters={})
        custom_alerts = create_custom_alerts_configuration()

        self.sf_state = CustomProduct(
            parameters=[activity, selectivity, qed_score, matching_substructure, custom_alerts])

    def test_desirability_component_1(self):
        score: FinalSummary = self.sf_state.get_final_score(smiles=["c1ccccc1CN"])
        self.assertAlmostEqual(score.total_score[0], 0.312, 3)

    def test_desirability_component_2(self):
        score: FinalSummary = self.sf_state.get_final_score(smiles=[celecoxib])
        self.assertAlmostEqual(score.total_score[0], 0.342, 3)
