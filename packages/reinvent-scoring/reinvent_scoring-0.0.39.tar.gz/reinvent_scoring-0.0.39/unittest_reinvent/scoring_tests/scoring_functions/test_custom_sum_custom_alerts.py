import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_custom_alerts_configuration
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum


class Test_custom_alerts_with_default_alerts(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        parameters = create_custom_alerts_configuration()
        self.sf_state = CustomSum(parameters=[parameters])

    def test_alert_1(self):
        score = self.sf_state.get_final_score(smiles=["C1CCCCCCCCC1", "C1CCCCCCCCCC1"])
        for i, s in enumerate(score.total_score):
            with self.subTest(i=i):
                self.assertEqual(score.total_score[i], 0.)

    def test_alert_2(self):
        score = self.sf_state.get_final_score(smiles=["CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"])
        for i, s in enumerate(score.total_score):
            with self.subTest(i=i):
                self.assertEqual(score.total_score[i], 1.)


class Test_custom_alerts_with_user_alerts(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        list_of_alerts = ["c1ccc2c(c1)c(cnc2O)C(=O)"]
        ts_parameters = ComponentParameters(component_type=sf_enum.CUSTOM_ALERTS,
                                            name="custom_alerts",
                                            weight=1.,
                                            smiles=list_of_alerts,
                                            model_path="",
                                            specific_parameters={})
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_user_alert_1(self):
        score = self.sf_state.get_final_score(smiles=["C1CCCCCCCCC1", "C1CCCCCCCCCC1"])
        for i, s in enumerate(score.total_score):
            with self.subTest(i=i):
                self.assertEqual(score.total_score[i], 1.)

    def test_user_alert_2(self):
        score = self.sf_state.get_final_score(smiles=["CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"])
        for i, s in enumerate(score.total_score):
            with self.subTest(i=i):
                self.assertEqual(score.total_score[i], 1.)

    def test_user_alert_3(self):
        score = self.sf_state.get_final_score(smiles=["c1ccc2c(c1)c(cnc2O)C(=O)"])
        for i, s in enumerate(score.total_score):
            with self.subTest(i=i):
                self.assertEqual(score.total_score[i], 0.)
