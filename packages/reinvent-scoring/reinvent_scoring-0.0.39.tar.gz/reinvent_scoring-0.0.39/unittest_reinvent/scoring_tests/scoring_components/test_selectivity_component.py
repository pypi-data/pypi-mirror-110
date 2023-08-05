import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components import SelectivityComponent
from unittest_reinvent.fixtures.paths import ACTIVITY_REGRESSION
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_activity_component_regression, \
    create_offtarget_activity_component_regression, create_offtarget_activity_component_classification, \
    create_activity_component_classification
from unittest_reinvent.scoring_tests.scoring_components.fixtures import score_single, score, celecoxib, random_compound
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import TransformationTypeEnum
import numpy.testing as npt

#TODO implement unittest_reinvent with activity regression and oftarget classification.
# Classification score should be higher than regression

class Test_mixed_selectivity_component(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        enum = ScoringFunctionComponentNameEnum()

        delta_params = {
            "high": 3.0,
            "k": 0.25,
            "low": 0.0,
            "transformation": True,
            "transformation_type": "sigmoid"
        }

        activity = create_activity_component_regression()
        activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        activity.specific_parameters[csp_enum.COEF_SI] = 150.
        activity.specific_parameters[csp_enum.COEF_SE] = 150.

        off_activity = create_offtarget_activity_component_classification()

        selectivity = ComponentParameters(component_type=enum.SELECTIVITY,
                                          name="desirability",
                                          weight=1.,
                                          smiles=[],
                                          model_path="",
                                          specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": off_activity.model_path,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity.specific_parameters.copy(),
                                               "delta_transformation_parameters": delta_params
                                          })
        self.component = SelectivityComponent(parameters=selectivity)

    def test_selectivity_component(self):
        smiles = [celecoxib, random_compound]
        expected_values = [0.634, 0.609]
        scores = score(self.component, smiles)
        npt.assert_almost_equal(scores, expected_values, decimal=3)


class Test_classification_selectivity_component(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        enum = ScoringFunctionComponentNameEnum()

        delta_params = {
            "high": 3.0,
            "k": 0.25,
            "low": 0.0,
            "transformation": True,
            "transformation_type": "sigmoid"
        }
        activity = create_activity_component_classification()
        activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        activity.specific_parameters[csp_enum.COEF_SI] = 150.
        activity.specific_parameters[csp_enum.COEF_SE] = 150.

        off_activity = create_offtarget_activity_component_classification()

        selectivity = ComponentParameters(component_type=enum.SELECTIVITY,
                                          name="desirability",
                                          weight=1.,
                                          smiles=[],
                                          model_path="",
                                          specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": off_activity.model_path,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity.specific_parameters.copy(),
                                               "delta_transformation_parameters": delta_params
                                           })

        cls.component = SelectivityComponent(parameters=selectivity)

    def test_selectivity_component_1(self):
        npt.assert_almost_equal(score_single(self.component, celecoxib), 0.01)


class Test_regression_selectivity_component(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        enum = ScoringFunctionComponentNameEnum()

        delta_params = {
            "high": 3.0,
            "k": 0.25,
            "low": 0.0,
            "transformation": True,
            "transformation_type": "sigmoid"
        }

        activity = create_activity_component_regression()
        activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        activity.specific_parameters[csp_enum.COEF_SI] = 150.
        activity.specific_parameters[csp_enum.COEF_SE] = 150.

        off_activity = create_offtarget_activity_component_regression()

        selectivity = ComponentParameters(component_type=enum.SELECTIVITY,
                                          name="desirability",
                                          weight=1.,
                                          smiles=[],
                                          model_path="",
                                          specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": ACTIVITY_REGRESSION,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity.specific_parameters.copy(),
                                               "delta_transformation_parameters": delta_params
                                           })
        cls.component = SelectivityComponent(parameters=selectivity)

    def test_selectivity_component(self):
        smiles = [celecoxib, "c1ccccc1CN"]
        expected_values = [0.053, 0.053]
        scores = score(self.component, smiles)
        npt.assert_almost_equal(scores, expected_values, decimal=3)


class Test_broken_regression_selectivity_component(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        csp_enum = ComponentSpecificParametersEnum()
        transf_type = TransformationTypeEnum()
        enum = ScoringFunctionComponentNameEnum()

        delta_params = {
            "high": 3.0,
            "k": 0.25,
            "low": 0.0,
            "transformation": True,
            "transformation_type": "sigmoid"
        }

        activity = create_activity_component_regression()
        activity.specific_parameters[csp_enum.TRANSFORMATION_TYPE] = transf_type.DOUBLE_SIGMOID
        activity.specific_parameters[csp_enum.COEF_DIV] = 100.
        activity.specific_parameters[csp_enum.COEF_SI] = 150.
        activity.specific_parameters[csp_enum.COEF_SE] = 150.

        off_activity = create_offtarget_activity_component_regression()

        activity.specific_parameters.pop(csp_enum.TRANSFORMATION_TYPE, None)
        off_activity.specific_parameters.pop(csp_enum.TRANSFORMATION_TYPE, None)

        selectivity = ComponentParameters(component_type=enum.SELECTIVITY,
                                          name="desirability",
                                          weight=1.,
                                          smiles=[],
                                          model_path="",
                                          specific_parameters={
                                               "activity_model_path": activity.model_path,
                                               "offtarget_model_path": ACTIVITY_REGRESSION,
                                               "activity_specific_parameters": activity.specific_parameters.copy(),
                                               "offtarget_specific_parameters": off_activity.specific_parameters.copy(),
                                               "delta_transformation_parameters": delta_params
                                           })
        cls.component = SelectivityComponent(parameters=selectivity)

    def test_selectivity_component(self):
        smiles = [celecoxib, random_compound]
        expected_values = [0.053, 0.053]
        scores = score(self.component, smiles)
        npt.assert_almost_equal(scores, expected_values, decimal=3)
