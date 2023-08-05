import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum


class Test_tanimoto_similarity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        ts_parameters = ComponentParameters(component_type=enum.TANIMOTO_SIMILARITY,
                                            name="tanimoto_similarity",
                                            weight=1.,
                                            smiles=["CCC", "COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"],
                                            model_path="",
                                            specific_parameters={})
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_similarity_1(self):
        score = self.sf_state.get_final_score(smiles=["CCC"])
        self.assertEqual(score.total_score, [1.])

    def test_similarity_2(self):
        score = self.sf_state.get_final_score(smiles=["COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"])
        self.assertEqual(score.total_score, [1.])

    def test_similarity_3(self):
        score = self.sf_state.get_final_score(smiles=["CCCN(CCCCN1CCN(c2ccccc2OC)CC1)Cc1ccc2ccccc2c1"])
        self.assertGreater([.5], score.total_score)

    def test_similarity_4(self):
        score = self.sf_state.get_final_score(smiles=["CCC", "COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"])
        for i, s in enumerate(score.total_score):
            self.assertEqual(score.total_score[i], 1.)