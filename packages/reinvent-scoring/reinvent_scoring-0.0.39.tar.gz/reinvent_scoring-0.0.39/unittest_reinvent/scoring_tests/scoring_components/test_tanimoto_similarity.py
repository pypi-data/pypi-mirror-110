import unittest

from typing import List
from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components import TanimotoSimilarity
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
    return TanimotoSimilarity(ComponentParameters(
        component_type=ScoringFunctionComponentNameEnum().TANIMOTO_SIMILARITY,
        name="tanimoto_similarity",
        weight=1.,
        smiles=smiles,
        model_path="",
        specific_parameters=specific_parameters))


class TestTanimotoSimilarity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.component = instantiate_component()

    def test_similarity_1(self):
        npt.assert_almost_equal(score_single(self.component, "CCC"), 1.0)

    def test_similarity_2(self):
        npt.assert_almost_equal(score_single(self.component, celecoxib), 1.0)

    def test_similarity_3(self):
        npt.assert_almost_equal(score_single(self.component, celecoxib_C), 0.89, decimal=3)

    def test_similarity_4(self):
        smiles = ["CCC", celecoxib]
        scores = score(self.component, smiles)
        npt.assert_almost_equal(scores, 1.0)


class TestTanimotoCustomFingerprintParameters(unittest.TestCase):

    def test_default(self):
        component = instantiate_component(specific_parameters={})
        npt.assert_almost_equal(score_single(component, caffeine), 0.101, decimal=3)

    def test_custom_radius(self):
        component = instantiate_component(specific_parameters={"radius": 2})
        npt.assert_almost_equal(score_single(component, caffeine), 0.125, decimal=3)

    def test_custom_use_counts(self):
        component = instantiate_component(specific_parameters={"use_counts": False})
        npt.assert_almost_equal(score_single(component, caffeine), 0.054, decimal=3)

    def test_custom_use_features_1(self):
        component = instantiate_component(specific_parameters={"use_features": False})
        npt.assert_almost_equal(score_single(component, caffeine), 0.083, decimal=3)

    def test_custom_use_features_2(self):
        smiles = ["c1ccccn1"]
        component = instantiate_component(
            smiles=smiles, specific_parameters={"use_features": False})
        npt.assert_almost_equal(score_single(component, "c1ccco1"), 0.206, decimal=3)

    def test_custom_use_features_3(self):
        component = instantiate_component(specific_parameters={"use_features": False})
        npt.assert_almost_equal(score_single(component, celecoxib_C), 0.810, decimal=3)
