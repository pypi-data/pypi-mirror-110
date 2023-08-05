import unittest

"""" As long as we use additive methods with both tanimoto distance and similarity we'll get a result of .5 (given equal weights. 
However, as T_d = 1-T_s, we could just use one of them and maintain the same information with less information and just scale the weight accordingly."""
from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum


class Test_combined_distance_and_similarity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        ts_parameters = ComponentParameters(component_type=sf_enum.TANIMOTO_SIMILARITY,
                                            name="tanimoto_similarity",
                                            weight=1.,
                                            smiles=["CCC", "COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"],
                                            model_path="",
                                            specific_parameters={})
        td_parameters = ComponentParameters(component_type=sf_enum.JACCARD_DISTANCE,
                                            name="tanimoto_distance",
                                            weight=1.,
                                            smiles=["CCC", "COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"],
                                            model_path="",
                                            specific_parameters={})
        self.sf_state = CustomSum(parameters=[ts_parameters, td_parameters])

    def test_combined_1(self):
        score = self.sf_state.get_final_score(smiles=["CCC"])
        self.assertEqual(score.total_score, [.5])
