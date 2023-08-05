import unittest
from typing import Union, List
from unittest import mock

import numpy.testing as npt
import rdkit
from rdkit.Chem.rdmolfiles import MolFromSmiles

from reinvent_scoring import ScoringFunctionComponentNameEnum, TransformationTypeEnum
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.predictive_model.model_container import ModelContainer
from reinvent_scoring.scoring.score_components import PredictivePropertyComponent, ComponentParameters
from unittest_reinvent.scoring_tests.fixtures.predictive_model_fixtures import \
    create_predictive_property_component_regression
from unittest_reinvent.scoring_tests.scoring_components.fixtures import score_single, score, celecoxib


class Test_predictive_property_component(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.csp_enum = ComponentSpecificParametersEnum()
        activity = create_predictive_property_component_regression()
        cls.component = PredictivePropertyComponent(activity)

    def test_predictive_property_1(self):
        npt.assert_almost_equal(score_single(self.component, celecoxib), 0.306, 3)

    def test_predictive_property_2(self):
        self.assertTrue(self.component.parameters.specific_parameters[self.csp_enum.TRANSFORMATION])


class ModelWithPredictFromSmiles:
    def predict_from_smiles(self, smiles: Union[str, List[str]]) -> List[float]:
        input = [smiles] if isinstance(smiles, str) else smiles  # Wrap single SMILES in a list.
        output = [len(smi) for smi in input]
        return output


class ModelWithPredictFromMols:
    def predict_from_rdkit_mols(self, mols: List[rdkit.Chem.Mol]) -> List[float]:
        output = [mol.GetNumAtoms() for mol in mols]
        return output

    def predict_from_smiles(self, smiles: Union[str, List[str]]) -> List[float]:
        mols = [MolFromSmiles(s) for s in smiles]
        output = [mol.GetNumAtoms() for mol in mols]
        return output


class Test_predictive_property_component_with_predict_from_smiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        csp_enum = ComponentSpecificParametersEnum()
        params = {
            csp_enum.TRANSFORMATION: True,
            csp_enum.TRANSFORMATION_TYPE: TransformationTypeEnum().NO_TRANSFORMATION,
            csp_enum.SCIKIT: "regression",
            csp_enum.DESCRIPTOR_TYPE: None,
            "container_type": "optuna_container"
        }
        with mock.patch(
            'reinvent_scoring.scoring.score_components.PredictivePropertyComponent._load_container',
            return_value=ModelContainer(ModelWithPredictFromSmiles(), params)
        ):
            cls.component = PredictivePropertyComponent(
                ComponentParameters(
                    component_type=ScoringFunctionComponentNameEnum.PREDICTIVE_PROPERTY,
                    name="predictive_property",
                    weight=1.,
                    smiles=[],
                    model_path="",
                    specific_parameters=params
                )
            )

    def test_predictive_property_1(self):
        npt.assert_almost_equal(score_single(self.component, celecoxib), 50, 3)

    def test_predictive_property_2(self):
        npt.assert_almost_equal(score(self.component, ["CCC", "CCCCC"]), [3, 5], 3)


class Test_predictive_property_component_with_predict_from_mols(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        csp_enum = ComponentSpecificParametersEnum()
        params = {
            csp_enum.TRANSFORMATION: True,
            csp_enum.TRANSFORMATION_TYPE: TransformationTypeEnum().NO_TRANSFORMATION,
            csp_enum.SCIKIT: "regression",
            csp_enum.DESCRIPTOR_TYPE: None,
            "container_type": "optuna_container"
        }
        with mock.patch(
            'reinvent_scoring.scoring.score_components.PredictivePropertyComponent._load_container',
            return_value=ModelContainer(ModelWithPredictFromMols(), params)
        ):
            cls.component = PredictivePropertyComponent(
                ComponentParameters(
                    component_type=ScoringFunctionComponentNameEnum.PREDICTIVE_PROPERTY,
                    name="predictive_property",
                    weight=1.,
                    smiles=[],
                    model_path="",
                    specific_parameters=params
                )
            )

    def test_predictive_property_1(self):
        npt.assert_almost_equal(score_single(self.component, celecoxib), 26, 3)

    def test_predictive_property_2(self):
        npt.assert_almost_equal(score(self.component, ["CCC", "CCCCC"]), [3, 5], 3)
