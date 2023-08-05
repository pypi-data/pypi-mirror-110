import unittest

import numpy as np
import numpy.testing as npt

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomSum
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import TransformationTypeEnum


class Test_number_of_stereo_centers(unittest.TestCase):

    def setUp(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        csp_enum = ComponentSpecificParametersEnum()
        tt_enum = TransformationTypeEnum()
        specific_parameters = {
                                csp_enum.TRANSFORMATION: False,
                                csp_enum.TRANSFORMATION_TYPE: tt_enum.NO_TRANSFORMATION
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.NUMBER_OF_STEREO_CENTERS,
                                            name="Number of stereo centers",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters
                                            )
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_tpsa_1(self):
        smiles = [
                  "CCC(C)C(C)C",
                  "c1ccccc1C"
                  ]
        values = np.array([1.0, 0.])
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, values, 2)



