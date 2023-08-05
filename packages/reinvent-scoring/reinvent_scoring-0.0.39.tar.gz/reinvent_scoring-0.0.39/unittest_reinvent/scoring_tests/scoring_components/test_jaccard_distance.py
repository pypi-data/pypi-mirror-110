import unittest

from typing import List
from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components import JaccardDistance
from unittest_reinvent.scoring_tests.scoring_components.fixtures import score_single, score
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
import numpy.testing as npt


caffeine = "O=C1C2=C(N=CN2C)N(C(=O)N1C)C"
celecoxib = "O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"
celecoxib_C = "O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)NC"


def instantiate_component(smiles: List[str] = None, specific_parameters: dict = None):
    if specific_parameters is None:
        specific_parameters = {}
    if smiles is None:
        smiles = ["CCC", celecoxib]
    return JaccardDistance(
        ComponentParameters(
            component_type=ScoringFunctionComponentNameEnum().JACCARD_DISTANCE,
            name="jaccard_distance",
            weight=1.0,
            smiles=smiles,
            model_path="",
            specific_parameters=specific_parameters,
        )
    )


class TestJaccardDistance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.component = instantiate_component()

    def test_distance_1(self):
        npt.assert_almost_equal(score_single(self.component, "CCC"), 0.0)

    def test_distance_2(self):
        npt.assert_almost_equal(score_single(self.component, celecoxib), 0.0)

    def test_distance_3(self):
        npt.assert_almost_equal(score_single(self.component, celecoxib_C), 0.109, 3)

    def test_distance_4(self):
        smiles = [celecoxib, "CCC"]
        npt.assert_almost_equal(score(self.component, smiles), [0, 0])


class TestJaccardCustomFingerprintParameters(unittest.TestCase):
    def test_default(self):
        component = instantiate_component(specific_parameters={})
        npt.assert_almost_equal(score_single(component, caffeine), 0.898, decimal=3)

    def test_custom_radius(self):
        component = instantiate_component(specific_parameters={"radius": 2})
        npt.assert_almost_equal(score_single(component, caffeine), 0.875, decimal=3)

    def test_custom_use_counts(self):
        component = instantiate_component(specific_parameters={"use_counts": False})
        npt.assert_almost_equal(score_single(component, caffeine), 0.945, decimal=3)

    def test_custom_use_features_1(self):
        component = instantiate_component(specific_parameters={"use_features": False})
        npt.assert_almost_equal(score_single(component, caffeine), 0.916, decimal=3)

    def test_custom_use_features_2(self):
        smiles = ["c1ccccn1"]
        component = instantiate_component(
            smiles=smiles, specific_parameters={"use_features": False}
        )
        npt.assert_almost_equal(score_single(component, "c1ccco1"), 0.793, decimal=3)

    def test_custom_use_features_3(self):
        component = instantiate_component(specific_parameters={"use_features": False})
        npt.assert_almost_equal(score_single(component, celecoxib_C), 0.189, decimal=3)
