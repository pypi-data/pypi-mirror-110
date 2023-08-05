import unittest

from reinvent_scoring.scoring.scoring_function_factory import ScoringFunctionFactory
from reinvent_scoring.scoring.scoring_function_parameters import ScoringFuncionParameters
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import ScoringFunctionNameEnum


class Test_parallel_scoring_function_factory(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        ts_parameters = dict(component_type=enum.TANIMOTO_SIMILARITY,
                             name="tanimoto_similarity",
                             weight=1.,
                             smiles=["CCC", "COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21"],
                             model_path="",
                             specific_parameters={})
        sf_enum = ScoringFunctionNameEnum()
        sf_parameters = ScoringFuncionParameters(name=sf_enum.CUSTOM_PRODUCT, parameters=[ts_parameters], parallel=True)
        self.sf_instance = ScoringFunctionFactory(sf_parameters=sf_parameters)

    def test_sf_factory_1(self):
        result = self.sf_instance.get_final_score(["CCC"])
        self.assertEqual(1., result.total_score)

    def test_sf_factory_2(self):
        result = self.sf_instance.get_final_score(["CCCCCC"])
        self.assertAlmostEqual(result.total_score[0], 0.353, 3)

