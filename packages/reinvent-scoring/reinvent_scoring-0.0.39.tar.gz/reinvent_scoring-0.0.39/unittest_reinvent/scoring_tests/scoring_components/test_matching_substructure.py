import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring.score_components import MatchingSubstructure
from unittest_reinvent.scoring_tests.scoring_components.fixtures import score_single
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
import numpy.testing as npt

class Test_matching_substructures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sf_enum = ScoringFunctionComponentNameEnum()
        parameters = ComponentParameters(component_type=sf_enum.MATCHING_SUBSTRUCTURE,
                                         name="matching_substructure",
                                         weight=1.,
                                         smiles=["c1[c;H]cc2[nH]c(nc2c1c3[c;H][c;H][c;H][n][c;H]3)c4cc[nH]n4"],
                                         model_path="",
                                         specific_parameters={})
        cls.component = MatchingSubstructure(parameters)

    def test_match_1(self):
        npt.assert_almost_equal(score_single(self.component, "Cn1cc(c([NH])cc1=O)"), 0.5)

    def test_match_2(self):
        npt.assert_almost_equal(score_single(self.component, "c1ccc2c(c1)c(cnc2O)C(=O)"), 0.5)

    def test_match_3(self):
        npt.assert_almost_equal(score_single(self.component, "CCN(C(C=C(C1)C(=O)Nc(c([n][nH]2)c([nH]c(c3c(cc4)c(c[n]cc5)c5)c4)[n]3)c2)=O)C=1"), 1.0)


class Test_matching_substructures_not_provided(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sf_enum = ScoringFunctionComponentNameEnum()
        parameters = ComponentParameters(component_type=sf_enum.MATCHING_SUBSTRUCTURE,
                                         name="matching_substructure",
                                         weight=1.,
                                         smiles=[],
                                         model_path="",
                                         specific_parameters={})
        cls.component = MatchingSubstructure(parameters)

    def test_match_no_structure_1(self):
        npt.assert_almost_equal(score_single(self.component, "Cn1cc(c([NH])cc1=O)"), 1.0)


class Test_invalid_matching_substructure(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sf_enum = ScoringFunctionComponentNameEnum()
        cls.matching_pattern = "HNc1nc(nc2c1nc(H)n2C(H)(H)C(H)(H)H)N(H)C(H)(C(H)(H)OH)C(H)(C(H)(H)H)C(H)(H)H"
        cls.parameters = ComponentParameters(component_type=sf_enum.MATCHING_SUBSTRUCTURE,
                                             name="matching_substructure",
                                             weight=1.,
                                             smiles=[cls.matching_pattern],
                                             model_path="",
                                             specific_parameters={})

    def test_match_invalid_structure_1(self):
        with self.assertRaises(IOError) as context:
            _ = MatchingSubstructure(self.parameters)
        msg = f"Invalid smarts pattern provided as a matching substructure: {self.matching_pattern}"
        self.assertEqual(msg, str(context.exception))
