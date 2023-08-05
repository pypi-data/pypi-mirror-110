import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components import CustomAlerts
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_custom_alerts_configuration
from unittest_reinvent.scoring_tests.scoring_components.fixtures import score_single, score
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
import numpy.testing as npt

class Test_custom_alerts_with_default_alerts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        parameters = create_custom_alerts_configuration()
        cls.component = CustomAlerts(parameters)

    def test_alert_1(self):
        npt.assert_almost_equal(score(self.component, ["C1CCCCCCCCC1", "C1CCCCCCCCCC1"]), [0.0, 0.0])

    def test_alert_2(self):
        npt.assert_almost_equal(score_single(self.component, "CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"), 1.0)


class Test_custom_alerts_with_user_alerts(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        list_of_alerts = ["c1ccc2c(c1)c(cnc2O)C(=O)"]
        parameters = ComponentParameters(component_type=sf_enum.CUSTOM_ALERTS,
                                         name="custom_alerts",
                                         weight=1.,
                                         smiles=list_of_alerts,
                                         model_path="",
                                         specific_parameters={})
        self.component = CustomAlerts(parameters)

    def test_user_alert_1(self):
        npt.assert_almost_equal(score(self.component, ["C1CCCCCCCCC1", "C1CCCCCCCCCC1"]), [1.0, 1.0])

    def test_user_alert_2(self):
        npt.assert_almost_equal(score_single(self.component, "CC(O)(CO)c1ccc2nc(NC3CCN(S(C)(=O)=O)CC3)cc(C)c2c1"), 1.0)

    def test_user_alert_3(self):
        npt.assert_almost_equal(score_single(self.component, "c1ccc2c(c1)c(cnc2O)C(=O)"), 0.0)
