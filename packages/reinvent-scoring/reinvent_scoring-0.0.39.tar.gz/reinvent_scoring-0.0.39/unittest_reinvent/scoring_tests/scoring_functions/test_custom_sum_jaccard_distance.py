import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum


class Test_jaccard_distance(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        td_parameters = ComponentParameters(component_type=sf_enum.JACCARD_DISTANCE,
                                            name="jaccard_distance",
                                            weight=1.,
                                            smiles=["COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21", "CCCCC"],
                                            model_path="",
                                            specific_parameters={})
        self.scoring_function = CustomSum(parameters=[td_parameters])

    def test_distance_1(self):
        score = self.scoring_function.get_final_score(smiles=["CCCCC"])
        self.assertEqual(score.total_score[0], .0)

    def test_distance_2(self):
        score = self.scoring_function.get_final_score(smiles=["COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"])
        self.assertEqual(score.total_score[0], .0)

    def test_distance_3(self):
        score = self.scoring_function.get_final_score(smiles=["CCCN(CCCCN1CCN(c2ccccc2OC)CC1)Cc1ccc2ccccc2c1"])
        self.assertAlmostEqual(score.total_score[0], 0.632, 3)

    def test_distance_4(self):
        score = self.scoring_function.get_final_score(smiles=["COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21", "CCCCC"])
        for i, s in enumerate(score.total_score):
            self.assertEqual(score.total_score[i], .0)