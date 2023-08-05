import unittest

import numpy as np
import numpy.testing as npt

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import TransformationTypeEnum


class Test_num_rings_score_no_transformation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        csp_enum = ComponentSpecificParametersEnum()
        ts_parameters = ComponentParameters(component_type=sf_enum.NUM_RINGS,
                                            name="Number of Rings",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters={
                                                csp_enum.TRANSFORMATION: False
                                            })
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_num_rings_1(self):
        smiles = [
                  "C1=CC2=C(C=C1)C1=CC=CC=C21",
                  "C12C3C4C1C5C2C3C45",
                  "N12CC3C(=NC4C(C=3)=CC=CC=4)C1=CC1=C(COC(=O)C1(O)CC)C2=O",
                  "N12CC3C(=NC4C(C=3C(=O)O)=CC3=C(OCCO3)C=4)C1=CC1=C(COC(=O)C1(O)CC)C2=O",
                  "FC1C=CC(CC(=NS(=O)(=O)C2C=CC(C)=CC=2)N2CCN(CC3C4C(=CC=CC=4)N=C4C=3CN3C4=CC4=C(COC(=O)C4(O)CC)C3=O)CC2)=CC=1"
                  ]
        values = np.array([3., 6., 5., 6., 8.])
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, values, 2)

class Test_num_rings_score_with_double_sigmoid(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        csp_enum = ComponentSpecificParametersEnum()
        tt_enum = TransformationTypeEnum()
        specific_parameters = {
                                csp_enum.TRANSFORMATION: True,
                                csp_enum.LOW: 3,
                                csp_enum.HIGH: 5,
                                csp_enum.TRANSFORMATION_TYPE: tt_enum.STEP
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.NUM_RINGS,
                                            name="Number of Rings",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters
                                            )
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_num_rings_1(self):
        smiles = [
                  "C1=CC2=C(C=C1)C1=CC=CC=C21",
                  "C12C3C4C1C5C2C3C45",
                  "N12CC3C(=NC4C(C=3)=CC=CC=4)C1=CC1=C(COC(=O)C1(O)CC)C2=O",
                  "N12CC3C(=NC4C(C=3C(=O)O)=CC3=C(OCCO3)C=4)C1=CC1=C(COC(=O)C1(O)CC)C2=O",
                  "FC1C=CC(CC(=NS(=O)(=O)C2C=CC(C)=CC=2)N2CCN(CC3C4C(=CC=CC=4)N=C4C=3CN3C4=CC4=C(COC(=O)C4(O)CC)C3=O)CC2)=CC=1"
                  ]
        values = np.array([1.0, 0.0, 1.0, 0.0, 0.0])
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, values, 2)



