import unittest

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum


class Test_matching_substructures(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        ts_parameters = ComponentParameters(component_type=sf_enum.MATCHING_SUBSTRUCTURE,
                                            name="matching_substructure",
                                            weight=1.,
                                            # smiles=["[*]n1cc(c([NH])cc1=O)"],
                                            smiles=["c1[c;H]cc2[nH]c(nc2c1c3[c;H][c;H][c;H][n][c;H]3)c4cc[nH]n4"],
                                            model_path="",
                                            specific_parameters={})
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_match_1(self):
        score = self.sf_state.get_final_score(smiles=["Cn1cc(c([NH])cc1=O)"])
        for i, s in enumerate(score.total_score):
            self.assertEqual(score.total_score[i], .5)

    def test_match_2(self):
        score = self.sf_state.get_final_score(smiles=["c1ccc2c(c1)c(cnc2O)C(=O)"])
        for i, s in enumerate(score.total_score):
            self.assertEqual(score.total_score[i], 0.5)

    def test_match_3(self):
        score = self.sf_state.get_final_score(smiles=["CCN(C(C=C(C1)C(=O)Nc(c([n][nH]2)c([nH]c(c3c(cc4)c(c[n]cc5)c5)c4)[n]3)c2)=O)C=1"])
        for i, s in enumerate(score.total_score):
            self.assertEqual(score.total_score[i], 1.)


class Test_matching_substructures_not_provided(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        ts_parameters = ComponentParameters(component_type=sf_enum.MATCHING_SUBSTRUCTURE,
                                            name="matching_substructure",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters={})
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_match_no_structure_1(self):
        score = self.sf_state.get_final_score(smiles=["Cn1cc(c([NH])cc1=O)"])
        for i, s in enumerate(score.total_score):
            self.assertEqual(score.total_score[i], 1.)


class Test_invalid_matching_substructure(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        self.matching_pattern = "HNc1nc(nc2c1nc(H)n2C(H)(H)C(H)(H)H)N(H)C(H)(C(H)(H)OH)C(H)(C(H)(H)H)C(H)(H)H"
        self.ts_parameters = ComponentParameters(component_type=sf_enum.MATCHING_SUBSTRUCTURE,
                                                 name="matching_substructure",
                                                 weight=1.,
                                                 smiles=[self.matching_pattern],
                                                 model_path="",
                                                 specific_parameters={})

    def test_match_invalid_structure_1(self):
        with self.assertRaises(IOError) as context:
            self.sf_state = CustomSum(parameters=[self.ts_parameters])
            score = self.sf_state.get_final_score(smiles=["Cn1cc(c([NH])cc1=O)"])
            print(score.total_score)
        msg = f"Invalid smarts pattern provided as a matching substructure: {self.matching_pattern}"
        self.assertEqual(msg, str(context.exception))
