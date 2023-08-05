import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.scoring_function_factory import ScoringFunctionFactory
from reinvent_scoring.scoring.scoring_function_parameters import ScoringFuncionParameters
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import \
    create_predictive_property_component_regression
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import ScoringFunctionNameEnum
from unittest_reinvent.scoring_tests.scoring_components.fixtures import celecoxib, random_compound


class Test_parallel_primary_multiplicative_function(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        sf_name_enum = ScoringFunctionNameEnum()
        activity = create_predictive_property_component_regression()
        activity.weight = 1
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

        sf_parameters = ScoringFuncionParameters(name=sf_name_enum.CUSTOM_PRODUCT,
                                                 parameters=[vars(activity), vars(qed_score), vars(custom_alerts),
                                                             vars(matching_substructure)], parallel=True)
        self.sf_instance = ScoringFunctionFactory(sf_parameters=sf_parameters)

    def test_primary_multiplicative_1(self):
        smiles = [celecoxib]*3
        score = self.sf_instance.get_final_score(smiles=smiles)
        self.assertAlmostEqual(score.total_score[0], 0.481, 3)

    def test_primary_multiplicative_2(self):
        smiles = [random_compound]*3
        score = self.sf_instance.get_final_score(smiles=smiles)
        self.assertAlmostEqual(score.total_score[0], 0.172, 3)
