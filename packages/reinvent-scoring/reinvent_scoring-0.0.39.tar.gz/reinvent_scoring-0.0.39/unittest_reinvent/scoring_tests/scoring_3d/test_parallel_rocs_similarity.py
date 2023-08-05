import unittest
import os
import shutil

import numpy.testing as npt
from rdkit.Chem import SDMolSupplier

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from unittest_reinvent.fixtures.paths import MAIN_TEST_PATH
from reinvent_scoring.scoring import CustomSum
from reinvent_scoring.scoring.enums import ROCSInputFileTypesEnum
from unittest_reinvent.fixtures.paths import ROCS_SIMILARITY_TEST_DATA, ROCS_SHAPE_QUERY, ROCS_SHAPE_QUERY_2, \
    ROCS_SHAPE_QUERY_3, ROCS_SHAPE_QUERY_CFF, ROCS_CUSTOM_CFF, ROCS_HIGH_ENERGY_QRY, ROCS_NEG_VOL_SQ, ROCS_NEG_VOL_LIG, \
    ROCS_NEG_VOL_PROTEIN
from reinvent_scoring.scoring.enums import ROCSSimilarityMeasuresEnum, ROCSSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum
from reinvent_scoring.scoring.enums import TransformationTypeEnum


class Test_parallel_rocs_similarity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.ROCS_INPUT: ROCS_SIMILARITY_TEST_DATA,
                               rsp_enum.INPUT_TYPE: input_type_enum.SDF_QUERY,
                               rsp_enum.MAX_CPUS: 4
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                            name="parallel_rocs_similarity",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_parallel_rocs_similarity_1(self):
        smiles = ["O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"]*128
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, [0.94]*128, 2)

    def test_parallel_rocs_similarity_2(self):
        score = self.sf_state.get_final_score(smiles=["O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"])
        npt.assert_array_almost_equal(score.total_score, [0.94], 2)

class Test_parallel_rocs_similarity_omegaopts_default(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        csp_enum = ComponentSpecificParametersEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.ROCS_INPUT: ROCS_HIGH_ENERGY_QRY,
                               rsp_enum.INPUT_TYPE: input_type_enum.SDF_QUERY,
                               csp_enum.TRANSFORMATION: False,
                               rsp_enum.MAX_CPUS: 4
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                            name="parallel_rocs_similarity",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_parallel_rocs_similarity_1(self):
        smiles = ["CCC(C)c1ccc(c2c1c(c[nH]2)C#N)NS(=O)(=O)c3cccc(c3)C#N"]
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, [0.64], 2)

class Test_parallel_rocs_similarity_omegaopts(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.ROCS_INPUT: ROCS_HIGH_ENERGY_QRY,
                               rsp_enum.INPUT_TYPE: input_type_enum.SDF_QUERY,
                               rsp_enum.EWINDOW: 50,
                               rsp_enum.MAX_CONFS: 600,
                               rsp_enum.MAX_CPUS: 4
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                            name="parallel_rocs_similarity",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_parallel_rocs_similarity_1(self):
        smiles = ["CCC(C)c1ccc(c2c1c(c[nH]2)C#N)NS(=O)(=O)c3cccc(c3)C#N"]
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, [0.87], 2)

class Test_parallel_rocs_similarity_tautomers(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.ROCS_INPUT: ROCS_SIMILARITY_TEST_DATA,
                               rsp_enum.INPUT_TYPE: input_type_enum.SDF_QUERY,
                               rsp_enum.MAX_CPUS: 4
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                            name="parallel_rocs_similarity",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_parallel_rocs_similarity_1(self):
        smiles = [
            "CCNS(=O)(=O)c1ccc(-n2nc(C[NH+](C)C)cc2-c2ccc[nH]c2=O)cc1",
            "CCNS(=O)(=O)c1ccc(-n2nc(CN(C)C)cc2-c2cccnc2O)cc1",
            "CCNS(=O)(=O)c1ccc(-n2[nH+]c(CN(C)C)cc2-c2cccnc2[O-])cc1",
            "CCNS(=O)(=O)c1ccc(cc1)n2c(cc(n2)C[NH+](C)C)c3ccc[nH]c3=O"
        ]
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, [0.73]*len(smiles), 2)


class Test_parallel_rocs_similarity_with_shape_query_no_transf_kw(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        sim_measure_enum = ROCSSimilarityMeasuresEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                               rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY,
                               rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                               rsp_enum.MAX_CPUS: 8
                               }
        rocs_sim = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                       name="parallel_rocs_similarity",
                                       weight=1.,
                                       smiles=[],
                                       model_path="",
                                       specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[rocs_sim])

    def test_parallel_rocs_similarity_1(self):
        smiles = ["O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"]*128
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score[0], [0.38], 2)

    def test_parallel_rocs_similarity_2(self):
        score = self.sf_state.get_final_score(smiles=["O=C(CNc1c[nH]nc1-c1nc(c(-c2ccccc2)ccc2)c2[nH]1)NCc1ncccc1"])
        self.assertAlmostEqual(score.total_score, [0.65], delta=0.01)

    def test_parallel_rocs_similarity_3(self):
        score = self.sf_state.get_final_score(smiles=["777"])
        self.assertEqual(score.total_score, [0.0])


class Test_parallel_rocs_similarity_with_transformation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        sim_measure_enum = ROCSSimilarityMeasuresEnum()
        csp_enum = ComponentSpecificParametersEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        tt_enum = TransformationTypeEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                               rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY,
                               rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                               csp_enum.TRANSFORMATION: True,
                               csp_enum.LOW: 0.3,
                               csp_enum.HIGH: 0.7,
                               csp_enum.K: 1,
                               csp_enum.TRANSFORMATION_TYPE: tt_enum.REVERSE_SIGMOID
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                            name="parallel_rocs_similarity",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[ts_parameters])

    def test_rocs_similarity_1(self):
        score = self.sf_state.get_final_score(smiles=["O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"])
        self.assertAlmostEqual(score.total_score, [1.0], delta=0.01)

    def test_rocs_similarity_2(self):
        score = self.sf_state.get_final_score(smiles=["O=C(CNc1c[nH]nc1-c1nc(c(-c2ccccc2)ccc2)c2[nH]1)NCc1ncccc1"])
        self.assertAlmostEqual(score.total_score, [0.0], delta=0.01)


class Test_parallel_rocs_similarity_with_custom_cff(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        sim_measure_enum = ROCSSimilarityMeasuresEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                               rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY_CFF,
                               rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                               rsp_enum.CUSTOM_CFF: ROCS_CUSTOM_CFF,
                               rsp_enum.MAX_CPUS: 8
                               }
        rocs_sim = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                       name="parallel_rocs_similarity",
                                       weight=1.,
                                       smiles=[],
                                       model_path="",
                                       specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[rocs_sim])

    def test_parallel_rocs_similarity_1(self):
        score = self.sf_state.get_final_score(smiles=[
            "O=C([C@@H](CN(C1)C([C@@]2(C3)[C@@H](C4)C[C@H]3C[C@@H]4C2)=O)C([C@@H](C2CC2)N2C[C@H]3[C@H](CC4)C[C@H]4C3)=C1C2=O)NC[C@]1(C2)[C@H](C3)C[C@@H]2C[C@H]3C1"
        ])
        self.assertAlmostEqual(score.total_score, [0.24], delta=0.01)

    def test_parallel_rocs_similarity_2(self):
        score = self.sf_state.get_final_score(smiles=[
            "O=C([C@H]([C@@H](c1ccccc1)c(cc1)ccc1F)NC(C1=CN(Cc(ccc(F)c2)c2F)c(cc(C(F)(F)F)cc2)c2C1=O)=O)NCCc1cc(C(F)(F)F)ccc1"
        ])
        self.assertAlmostEqual(score.total_score, [0.65], delta=0.01)

    def test_parallel_rocs_similarity_3(self):
        score = self.sf_state.get_final_score(smiles=["777"])
        self.assertEqual(score.total_score, [0.0])


class Test_parallel_rocs_similarity_with_two_components(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        sim_measure_enum = ROCSSimilarityMeasuresEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        specific_parameters_1 = {rsp_enum.SHAPE_WEIGHT: 0.2,
                                 rsp_enum.COLOR_WEIGHT: 0.8,
                                 rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                                 rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY,
                                 rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                                 rsp_enum.MAX_CPUS: 8,
                                 }
        rocs_sim_1 = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                         name="parallel_rocs_similarity",
                                         weight=1.,
                                         smiles=[],
                                         model_path="",
                                         specific_parameters=specific_parameters_1)
        specific_parameters_2 = {rsp_enum.SHAPE_WEIGHT: 0.5,
                                 rsp_enum.COLOR_WEIGHT: 0.5,
                                 rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                                 rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY_2,
                                 rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                                 rsp_enum.MAX_CPUS: 8
                                 }
        rocs_sim_2 = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                         name="parallel_rocs_similarity",
                                         weight=1.,
                                         smiles=[],
                                         model_path="",
                                         specific_parameters=specific_parameters_2)
        self.sf_state = CustomSum(parameters=[rocs_sim_1, rocs_sim_2])

    def test_parallel_rocs_similarity_1(self):
        smiles = ["O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"]
        score = self.sf_state.get_final_score(smiles=smiles)
        self.assertAlmostEqual(score.total_score, [0.41], delta=0.01)

    def test_parallel_rocs_similarity_2(self):
        score = self.sf_state.get_final_score(smiles=["O=C(CNc1c[nH]nc1-c1nc(c(-c2ccccc2)ccc2)c2[nH]1)NCc1ncccc1"])
        self.assertAlmostEqual(score.total_score, [0.73], delta=0.01)


class Test_parallel_rocs_similarity_tversky_score_bug(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        sim_measure_enum = ROCSSimilarityMeasuresEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.0, rsp_enum.COLOR_WEIGHT: 1.0,
                               rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                               rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY_3,
                               rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                               rsp_enum.MAX_CPUS: 8
                               }
        rocs_sim = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                       name="parallel_rocs_similarity",
                                       weight=1.,
                                       smiles=[],
                                       model_path="",
                                       specific_parameters=specific_parameters)
        self.sf_state = CustomSum(parameters=[rocs_sim])

    def test_parallel_rocs_similarity(self):
        smiles = [
            "c1(-c2cc(Cc3ccccc3)ccc2OC2C3CC4(C(O)=O)CC2C4C3)cccc2cc(S(=O)(=O)Nc3ccccn3)ccc12",
            "c1c(-c2cc(C(F)(F)F)ccc2OC2C3CC4(C(O)=O)CC2C4(F)C3(F)F)c(Oc2ccc(Cl)cc2C2CC2)ccc1C(F)(F)F",
            "c1c(-c2cc(C(F)(F)F)ccc2OC2C3CC4(C(=O)O)CC2C4(F)C3)c(C2c3ccccc3CC2)ccc1F",
            "c1c(-c2cc(C(F)(F)F)ccc2OC2C3CC4(C(=O)O)CC2C4(F)C3)c(C2c3ccccc3C(CC3CC3)=C2)ccc1C(F)(F)F"
        ]
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_less(score.total_score, [1.0, 1.0, 1.0, 1.0])

class Test_parallel_rocs_similarity_with_shape_query_save_overlays(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        if not os.path.isdir(MAIN_TEST_PATH):
            os.makedirs(MAIN_TEST_PATH)
        sf_enum = ScoringFunctionComponentNameEnum()
        sim_measure_enum = ROCSSimilarityMeasuresEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        overlays_dir = os.path.join(MAIN_TEST_PATH, "test_save_rocs")
        prefix = "unit_test_"
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                               rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY,
                               rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                               rsp_enum.SAVE_ROCS_OVERLAYS: True,
                               rsp_enum.ROCS_OVERLAYS_DIR: overlays_dir,
                               rsp_enum.ROCS_OVERLAYS_PREFIX: prefix,
                               rsp_enum.MAX_CPUS: 8
                               }
        rocs_sim = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                       name="parallel_rocs_similarity",
                                       weight=1.,
                                       smiles=[],
                                       model_path="",
                                       specific_parameters=specific_parameters)
        self.file_name = os.path.join(overlays_dir, prefix + "-001.sdf")
        self.sf_state = CustomSum(parameters=[rocs_sim])

    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(MAIN_TEST_PATH):
            shutil.rmtree(MAIN_TEST_PATH)

    def test_parallel_rocs_similarity(self):
        smiles = ["O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N"]*128
        score = self.sf_state.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score[0], [0.38], 2)

        file_created = os.path.exists(self.file_name)
        self.assertTrue(file_created)
        num_mols = -1
        if file_created:
            suppl = SDMolSupplier(self.file_name)
            num_mols = len(suppl)
        self.assertEqual(num_mols, len(score.total_score))

class Test_parallel_rocs_similarity_enumerate_stereo(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        sim_measure_enum = ROCSSimilarityMeasuresEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                               rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY,
                               rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                               rsp_enum.ENUM_STEREO: False,
                               rsp_enum.MAX_STEREO: 3,
                               rsp_enum.MAX_CPUS: 8
                               }
        rocs_sim = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                       name="parallel_rocs_similarity",
                                       weight=1.,
                                       smiles=[],
                                       model_path="",
                                       specific_parameters=specific_parameters)
        self.sf_state_no_enum = CustomSum(parameters=[rocs_sim])
        specific_parameters[rsp_enum.ENUM_STEREO] = True
        rocs_sim.specific_parameters = specific_parameters
        self.sf_state_enum = CustomSum(parameters=[rocs_sim])

    def test_parallel_rocs_similarity(self):
        smiles = ["Cc1ccc(cc1)C2CC(CN2c3ccc(cc3)CN)C(F)(F)F"]
        score_no_enum = self.sf_state_no_enum.get_final_score(smiles=smiles)
        score_enum = self.sf_state_enum.get_final_score(smiles=smiles)
        self.assertAlmostEqual(score_no_enum.total_score[0], 0.33, delta=0.01)
        self.assertAlmostEqual(score_enum.total_score[0], 0.35, delta=0.01)

class Test_parallel_rocs_similarity_negative_volume(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sf_enum = ScoringFunctionComponentNameEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.ROCS_INPUT: ROCS_NEG_VOL_SQ,
                               rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                               rsp_enum.CUSTOM_CFF: ROCS_CUSTOM_CFF,
                               rsp_enum.NEGATIVE_VOLUME: True,
                               rsp_enum.PROTEIN_NEG_VOL_FILE: ROCS_NEG_VOL_PROTEIN,
                               rsp_enum.LIGAND_NEG_VOL_FILE: ROCS_NEG_VOL_LIG,
                               rsp_enum.ENUM_STEREO: True,
                               rsp_enum.MAX_STEREO: 3,
                               rsp_enum.MAX_CPUS: 8
                               }
        ts_parameters = ComponentParameters(component_type=sf_enum.PARALLEL_ROCS_SIMILARITY,
                                            name="parallel_rocs_similarity",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters=specific_parameters)
        self.sf_state_with_vol = CustomSum(parameters=[ts_parameters])
        specific_parameters[rsp_enum.NEGATIVE_VOLUME] = False
        ts_parameters.specific_parameters = specific_parameters
        self.sf_state_no_vol = CustomSum(parameters=[ts_parameters])

    def test_parallel_rocs_similarity_1(self):
        smiles = ["Cc1cc(c(cc1c2cccc3c2c([n]([n]3)C)C)C(=O)N(C)CC4(CCCCC4)OC)OC",
                  "CCCCCOc1cc(c(c(c1C(=O)N(C)CC2(CCCCC2)OC)C#C)c3cccc4c3c([n]([n]4)C)C)C",
                  "CCCCCOc1cc(c(c(c1C(=O)N(C)CC2(CCCCC2)OC)C#CC(C)(C)C)c3cccc4c3c([n]([n]4)C)C)C"
                  ]
        score = self.sf_state_with_vol.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, [0.51, 0.39, 0.35], 2)

    def test_parallel_rocs_similarity_2(self):
        smiles = ["Cc1cc(c(cc1c2cccc3c2c([n]([n]3)C)C)C(=O)N(C)CC4(CCCCC4)OC)OC",
                  "CCCCCOc1cc(c(c(c1C(=O)N(C)CC2(CCCCC2)OC)C#C)c3cccc4c3c([n]([n]4)C)C)C",
                  "CCCCCOc1cc(c(c(c1C(=O)N(C)CC2(CCCCC2)OC)C#CC(C)(C)C)c3cccc4c3c([n]([n]4)C)C)C"
                  ]
        score = self.sf_state_no_vol.get_final_score(smiles=smiles)
        npt.assert_array_almost_equal(score.total_score, [0.53, 0.44, 0.44], 2)