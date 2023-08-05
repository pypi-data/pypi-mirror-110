import unittest

from rdkit import Chem

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from reinvent_scoring.scoring.score_components.score_component_factory import ScoreComponentFactory
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum


class Test_custom_sum_qed_score(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        self.parameters = ComponentParameters(component_type=sf_enum.QED_SCORE,
                                              name="qed_score",
                                              weight=1.,
                                              smiles=[],
                                              model_path="",
                                              specific_parameters={})
        self.scoring_function = CustomSum(parameters=[self.parameters])

    def test_qed_sum(self):
        score = self.scoring_function.get_final_score(smiles=["C1CCCCCCCCC1"])
        self.assertAlmostEqual(score.total_score[0], 0.4784, 4)

    def test_qed_component_factory(self):
        factory = ScoreComponentFactory([self.parameters])
        scoring_components = factory.create_score_components()
        sc = scoring_components[0]
        smile = "C1CCCCCCCCC1"
        mol = Chem.MolFromSmiles(smile)
        score = sc.calculate_score([mol])
        self.assertAlmostEqual(score.total_score[0], 0.4784, 4)
