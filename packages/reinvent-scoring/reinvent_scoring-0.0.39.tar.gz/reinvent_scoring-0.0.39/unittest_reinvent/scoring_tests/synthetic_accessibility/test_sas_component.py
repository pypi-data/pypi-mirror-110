import unittest

import numpy.testing as npt
from reinvent_chemistry.conversions import Conversions

from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.score_components.synthetic_accessibility.sas_component import SASComponent
from unittest_reinvent.fixtures.paths import SAS_MODEL_PATH
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import create_activity_component_regression
from unittest_reinvent.scoring_tests.scoring_components.fixtures import celecoxib, random_compound


class Test_sas_component(unittest.TestCase):

    def setUp(self):
        csp_enum = ComponentSpecificParametersEnum()
        ts_parameters = create_activity_component_regression()
        ts_parameters.specific_parameters[csp_enum.TRANSFORMATION] = False
        ts_parameters.model_path = SAS_MODEL_PATH
        chemistry = Conversions()

        self.query_smiles = [celecoxib,
                             random_compound,
                             "c1ccccc1CN"]
        self.query_mols = [chemistry.smile_to_mol(smile) for smile in self.query_smiles]
        self.component = SASComponent(ts_parameters)

    def test_sas(self):
        summary = self.component.calculate_score(self.query_mols)
        npt.assert_almost_equal(summary.total_score, [0.97, 0.5, 1.], decimal=2)
