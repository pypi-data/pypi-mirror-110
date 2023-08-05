import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from unittest_reinvent.fixtures.paths import ROCS_MULTI_SIMILARITY_TEST_DATA
from reinvent_scoring.scoring.enums import ROCSInputFileTypesEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum


class Test_rocs_multi_similarity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        csp_enum = ComponentSpecificParametersEnum()
        # NOTE: license is required
        # "export OE_LICENSE='/opt/scp/software/oelicense/1.0/oe_license.seq1'"
        specific_parameters = {"shape_weight": 0.5, "color_weight": 0.5,
                               "rocs_input": ROCS_MULTI_SIMILARITY_TEST_DATA,
                               "input_type": input_type_enum.SDF_QUERY,
                               csp_enum.TRANSFORMATION: False
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.ROCS_SIMILARITY,
                                            name="rocs_multi_similarity",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_rocs_similarity_1(self):
        score = self.sf_state.get_final_score(smiles=["O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"])
        self.assertGreater(score.total_score, [0.94])

    def test_rocs_similarity_2(self):
        score = self.sf_state.get_final_score(smiles=["CC1CC1COc2ccc(cc2)C(=O)N[C@H](C(=O)NO)C(C)(C)N"])
        self.assertAlmostEqual(score.total_score, [0.33], delta=0.01)

    def test_rocs_similarity_3(self):
        score = self.sf_state.get_final_score(smiles=["777"])
        self.assertEqual(score.total_score, [0.0])


class Test_parallel_rocs_multi_similarity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        csp_enum = ComponentSpecificParametersEnum()
        # NOTE: license is required
        # "export OE_LICENSE='/opt/scp/software/oelicense/1.0/oe_license.seq1'"
        specific_parameters = {"shape_weight": 0.5, "color_weight": 0.5,
                               "rocs_input": ROCS_MULTI_SIMILARITY_TEST_DATA,
                               "input_type": input_type_enum.SDF_QUERY,
                               csp_enum.TRANSFORMATION: False,
                               "max_num_cpus": 8
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                            name="rocs_multi_similarity",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_rocs_similarity_1(self):
        score = self.sf_state.get_final_score(smiles=["O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"])
        self.assertGreater(score.total_score, [0.94])

    def test_rocs_similarity_2(self):
        score = self.sf_state.get_final_score(smiles=["CC1CC1COc2ccc(cc2)C(=O)N[C@H](C(=O)NO)C(C)(C)N"])
        self.assertAlmostEqual(score.total_score, [0.35], delta=0.01)

    def test_rocs_similarity_3(self):
        score = self.sf_state.get_final_score(smiles=["777"])
        self.assertEqual(score.total_score, [0.0])
