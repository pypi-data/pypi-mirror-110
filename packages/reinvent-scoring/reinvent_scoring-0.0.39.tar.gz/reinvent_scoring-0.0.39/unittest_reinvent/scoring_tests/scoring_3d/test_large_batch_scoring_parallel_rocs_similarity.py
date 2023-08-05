import unittest

import numpy.testing as npt

from reinvent_scoring.scoring.component_parameters import ComponentParameters
from reinvent_scoring.scoring import CustomProduct
from unittest_reinvent.fixtures.paths import ROCS_SHAPE_QUERY_BATCH
from reinvent_scoring.scoring.enums import ROCSInputFileTypesEnum, ROCSSimilarityMeasuresEnum, ROCSSpecificParametersEnum
from reinvent_scoring.scoring.enums import ScoringFunctionComponentNameEnum
from reinvent_scoring.scoring.enums import ComponentSpecificParametersEnum


class Test_parallel_rocs_similarity_with_shape_query_large_batch(unittest.TestCase):
    # This is to assert that there is always a 1:1 between smiles and scores for each batch
    # even when one or more smiles fail to produce a score
    @classmethod
    def setUpClass(self):
        enum = ScoringFunctionComponentNameEnum()
        sim_measure_enum = ROCSSimilarityMeasuresEnum()
        input_type_enum = ROCSInputFileTypesEnum()
        csp_enum = ComponentSpecificParametersEnum()
        rsp_enum = ROCSSpecificParametersEnum()
        custom_alerts = ComponentParameters(component_type=enum.CUSTOM_ALERTS,
                                            name="custom_alerts_name",
                                            weight=1.,
                                            smiles=[],
                                            model_path="",
                                            specific_parameters={})
        matching_substructure = ComponentParameters(component_type=enum.MATCHING_SUBSTRUCTURE,
                                                    name="matching_substructure_name",
                                                    weight=1.,
                                                    smiles=[],
                                                    model_path="",
                                                    specific_parameters={})
        specific_parameters = {rsp_enum.SHAPE_WEIGHT: 0.5,
                               rsp_enum.COLOR_WEIGHT: 0.5,
                               rsp_enum.SIM_MEASURE: sim_measure_enum.REF_TVERSKY,
                               rsp_enum.ROCS_INPUT: ROCS_SHAPE_QUERY_BATCH,
                               rsp_enum.INPUT_TYPE: input_type_enum.SHAPE_QUERY,
                               csp_enum.TRANSFORMATION: False,
                               rsp_enum.MAX_CPUS: 4
                               }
        rocs_sim = ComponentParameters(component_type=enum.PARALLEL_ROCS_SIMILARITY,
                                       name="parallel_rocs_similarity",
                                       weight=3.,
                                       smiles=[],
                                       model_path="",
                                       specific_parameters=specific_parameters)
        self.sf_state = CustomProduct(parameters=[custom_alerts, matching_substructure, rocs_sim])

    def test_quick(self):
        score = self.sf_state.get_final_score(smiles=[
            'c1[nH]nc(-c2cc(Cl)ccc2Oc2c(F)c(Cl)cc(F)c2)n1',
            'c1(=O)n(-c2cc(F)c(-c3cccc(OCC)c3)cc2OC)c2c(ccc(=NS(=O)(=O)C3CC3)c2)o1',
            'N(=c1cco[nH]1)S(=O)(=O)c1ccc2c(-c3c(OC)cc(-c4cc(Cl)ccc4OC)c4n(C)c(=O)oc43)cccc2c1'
        ])
        vals = [0.43, 0., 0.67]
        npt.assert_array_almost_equal(score.total_score, vals, 2)

    def test_extended(self):
        score = self.sf_state.get_final_score(smiles=
        [
            'C1CC1c1c(OCC2(F)CCN(S(=O)(=O)N=c3[nH]nccc3)CC2)cc(F)c(C(F)(F)F)c1',
            'C(c1cc(Cl)c(F)cc1)(CO)N1CCC(COc2c(C3CC3)cc(C(=O)NS(C)(=O)=O)c(F)c2)CC1',
            'C1CCCCC1C(O)C=Cc1cc(-c2c(F)cc(-n3c4c(ccc3=O)CN(S(=O)(=O)N=c3cc(C)[nH]cn3)CC4)c(OC)c2)ccc1',
            'S(=O)(=O)(c1ccc2c(ccc(=O)n2-c2ccc(-c3cc(Cl)ccc3OC)cc2OC)c1)N=c1nccc[nH]1',
            'COc1cc(-c2cccc(F)c2)ccc1-n1c2c(ccc1=O)cc(S(=O)(=O)N=c1cco[nH]1)cc2',
            'c1(-c2c3ccc(S(N=c4cco[nH]4)(=O)=O)cc3ccn2)c(OCc2cccc(F)c2)cccc1',
            'c1c(Cl)cc(-c2cc(OC)c(-c3[nH]c(=O)cc4cc(S(=O)(N=c5cco[nH]5)=O)ccc43)cc2F)cc1C',
            'c1cc2c(c(C(n3c4cc(F)c(S(N=c5[nH]c(F)ccc5)(=O)=O)cc4oc3=O)C)c1)OCCO2',
            'c1(N2c3ccc(S(=O)(=O)N=c4[nH]cns4)cc3OCC2)ccc(C(F)(F)F)cc1-n1ccnc1C',
            'C1C(COc2cc(F)c(C(=O)NS(C3CC3)(=O)=O)cc2C2CC2)CCN(C(C)c2cc(C(F)(F)F)c(F)cc2)C1',
            'C1(COc2cc(F)c(C(=O)NS(=O)(=O)C)cc2C2CC2)(C)CCc2sc(Cl)cc2C1C',
            'Fc1cc(NC2CCCCC2N(C)CC)c(Cl)cc1S(N(c1c(OC)cc(C(NS(=O)(C)=O)=O)c(F)c1)C)(=O)=O',
            'C1C(F)(F)CCC(COc2cc(F)c(C(NS(C)(=O)=O)=O)cc2C2CC2)C1',
            'FC(F)(F)c1cccc(C2(F)CCOc3cc(S(=O)(N=c4snc[nH]4)=O)ccc32)c1',
            'CN(C)C1C(Nc2c(Cl)cc(S(N=c3scc[nH]3)(=O)=O)c(F)c2)CCCC1',
            'c12ccc(S(=O)(N=c3cc[nH]cn3)=O)cc1cccc2-c1c(C)cc(Cl)cc1',
            'c1(C)c2ccc(=O)n(-c3cc(F)c(-c4cc(Cl)cc(F)c4)cc3OC)c2cc(Cl)c1',
            'O=S(NC(c1cc(C)c(-c2cnc(OCC3CCCCC3)c(Cl)c2)cc1F)=O)(C)=O',
            'S(=O)(C1CC1)(=O)NC(c1c(F)cc(OCC2(C)CCC=CC2)c(C2CC2)c1)=O',
            'c1(-c2c3c(ccc2)cccc3)c(F)cc(-n2c(=O)ccc3c2ccc(S(=O)(=O)N=c2cco[nH]2)c3)c(OC)c1',
            'c1c(Oc2ccc(Cl)cc2-c2c(=N)[nH][nH]c2)c(Cl)cc(S(=O)(N=c2[nH]ncs2)=O)c1F',
            'O1CCN(c2cc(C(F)(F)F)cc(Cl)c2C#N)c2ccc(S(=O)(=O)N=c3scc[nH]3)cc21',
            'c1c(-c2c(Cl)cc(-n3c4c(ccc3=O)cc(S(=O)(N=c3[nH]cns3)=O)cc4)c(OC)c2)ccc(F)c1F',
            'c1c(C(C)N2CC(n3ncc4c3CC3(CC3)CCC4)CC2)cc(Cl)c(OCC23CC4CC(CC(C2)C4)C3)c1Cl',
            'c1(C)cc(-c2c(F)cc(-n3c(=O)ccc4cc(S(=O)(=O)N=c5cc(C)[nH]cn5)ccc43)c(OC)c2)cc(F)c1',
            'c1c(=NS(N2CCc3c(ccc(=O)n3-c3cc(F)c(-c4cc(C)c(C)cc4)cc3OC)C2)(=O)=O)[nH]ncc1',
            'c12c(ccc(S(=O)(=O)N=c3[nH]ccs3)c1)N(c1c(C#N)cc(C(F)(F)F)cc1)CCO2',
            'c1c(F)cc(C(C)n2c3cc(F)c(S(=O)(N=c4snc[nH]4)=O)cc3cn2)cc1F',
            'n1c(-c2ccc(C(F)(F)F)cc2OC)c2cc(S(N=c3cc[nH]cn3)(=O)=O)ccc2n(-c2ccc(Cl)cc2)c1=O',
            'c1c(Oc2ccc(-c3cc(C(F)(F)F)nn3C)cc2C#N)c(C#N)cc(S(=O)(=O)N=c2[nH]ccs2)c1',
            'N(=c1snc[nH]1)S(=O)(=O)c1cc(Cl)c(NCCCCNC2CNCC2O)cc1F',
            'S(c1ccc(Oc2ccc(Cl)cc2-c2cc[nH]c(=N)c2)c(Cl)c1)(=O)(=O)N=c1scc[nH]1',
            'C1(c2cc(NCCCCNc3c(Cl)cc(S(=O)(=O)N=c4scc[nH]4)c(F)c3)c(Cl)cc2O)CC1',
            'c1[nH]c(=NS(=O)(c2cc(Cl)c(NCC34CCCN3CCC4)cc2COC)=O)sc1', 'c1[nH]nc(-c2cc(Cl)ccc2Oc2c(F)c(Cl)cc(F)c2)n1',
            'c1(=O)n(-c2cc(F)c(-c3cccc(OCC)c3)cc2OC)c2c(ccc(=NS(=O)(=O)C3CC3)c2)o1',
            'N(=c1cco[nH]1)S(=O)(=O)c1ccc2c(-c3c(OC)cc(-c4cc(Cl)ccc4OC)c4n(C)c(=O)oc43)cccc2c1',
            'c1(F)c(F)cc(-c2ccc(-c3ncnc4cc(S(=O)(=O)N=c5[nH]occ5)ccc43)c(OC)c2)cc1',
            'c1c(=NS(=O)(=O)c2ccc3c(-c4c(-c5ccnn5C)cc(C(F)(F)F)cc4)cccc3c2)[nH]ncc1',
            'CN(C)C1CCc2c(c(CN3CCC(Oc4ccc(F)cc4)(C)CC3)cc(F)c2)C1',
            'n1c(-c2cc(F)c(-c3cc(F)cc(OC)c3)cc2OC)c2c(cc(S(N=c3[nH]ncs3)(=O)=O)cc2)cc1',
            'N1(S(=O)(=O)NC(=O)c2cc(C3CC3)c(OC3CCC4(CC3)CCCC4)cc2F)CCC1',
            'FC(F)(F)c1cc(-c2ccnn2C)c(C2CCOc3cc(S(N=c4[nH]c(F)ccc4)(=O)=O)ccc32)cc1',
            'c1c(C(NC2CC2c2ccccc2)=O)ccc(Oc2cc(-c3ccc(Cl)cc3)ccc2)c1C#N',
            'Fc1cc(-n2c3ccc(S(=O)(=O)N=c4nccc[nH]4)cc3ccc2=O)c(OC)cc1C#CC1CCCC1',
            'N(c1cc(F)c(S(=O)(N=c2scc[nH]2)=O)cc1Cl)C1CCCCC1N(C)C1C(N)CCC1',
            'c1c(-c2cc(Cl)ccc2Oc2c(F)cc(S(N=c3[nH]ccs3)(=O)=O)c(F)c2)cnnc1',
            'C1CCC(Oc2cc(F)c(C(=O)NS(=O)(=O)C)cc2C2CC2)CN1Cc1cc(F)c(Cl)cc1C(F)(F)F',
            'C1C2CCC(CN1CCCNc1c(Cl)cc(S(=O)(N=c3sc(F)c[nH]3)=O)c(F)c1)N2',
            'n1ccnc(N2CCOc3cc(S(N=c4[nH]ccs4)(=O)=O)ccc32)c1',
            'O=S(=O)(NC(c1c(F)cc(OCC2CC3C(F)(F)C3CC2)c(C2CC2)c1)=O)N1CCC1',
            'O1CCC(COc2cc(F)c(C(=O)NS(=O)(=O)C)cc2C2CC2)CC1',
            'C1(c2cc(C(=O)NS(=O)(C)=O)c(F)cc2OC2CC(C)(C)CCC2c2cnn(C)c2)CC1',
            'C12(CC(N(C)C)CC1)CCN(Cc1cccc(C(F)(F)F)c1)CC2',
            'c1cc2c(ccc(S(=O)(=O)N=c3cco[nH]3)c2)n(-c2cc(F)c(-c3cc(F)cc(Cl)c3)cc2OC)c1=O',
            'O=S(N=c1[nH]ccs1)(c1cc(Br)c(NCC23N(CC(C)(C)C2)CCC3)cc1F)=O',
            'C1CCCC1n1c2cc(C#N)c(S(=O)(N=c3nc[nH]c(C)c3)=O)cc2cn1',
            'C1NC(c2c(OC)cc(-c3c(Oc4c(F)cc(S(=O)(=O)N=c5[nH]ccs5)c(F)c4)ccc(Cl)c3)cc2)=NC1',
            'C(C(CCN)O)Oc1c(C2CC2)cc(C(NS(=O)(C)=O)=O)c(F)c1',
            'c1c(-n2c3ccc(S(=O)(N=c4cco[nH]4)=O)cc3ccc2=O)c(OC)cc(-c2ccc(C)c(OC)c2)c1',
            'C1(COc2cc(F)c(C(=O)NS(C)(=O)=O)cc2Cl)(C)CCC(F)(F)CC1',
            'c1cc(-c2c(C)cc(-n3c4ccc(S(N=c5cco[nH]5)(=O)=O)cc4ccc3=O)c(OC)c2)cc(OC)c1C',
            'c1c(-c2cc(OC)c(-n3c(=O)ccc4cc(S(=O)(N=c5ncc(F)c[nH]5)=O)ccc43)cc2F)c(OC)c(Cl)cc1',
            'C1(COc2cc(F)c(C(=O)NS(=O)(C3CC3)=O)cc2C2CC2)CCN(C(COC)c2cc(F)c(F)cc2)CC1',
            'C1C2CC3C(C2(C)Oc2cc4n(c(=NS(=O)(=O)C)[nH]n4)cc2-c2c(C4=CCNCC4)cc(C(F)(F)F)cc2)C1C3',
            'c1(-c2cc(-n3c(=O)ccc4cc(S(=O)(N=c5ncc(F)c[nH]5)=O)ccc43)c(OC)cc2)cccc(C(F)(F)F)c1',
            'O=C(N(C)C)N1CC(COc2c(C3CC3)cc(C(NS(=O)(C)=O)=O)c(F)c2)C1',
            'c1c(C(C)n2c3cc(F)c(S(=O)(N=c4nc[nH]cc4)=O)cc3oc2=O)cc2c(c1)C(N(C)C)CCC2',
            'C1C(S(=O)(=O)NC(=O)c2c(F)cc(OCC3CCN(C(c4cc(Cl)cc(Cl)c4)COC)CC3)c(C3CC3)c2)C1',
            'N1(c2ccc(C(F)(F)F)cc2-c2ncco2)c2ccc(S(=O)(N=c3snc[nH]3)=O)cc2OCC1',
            'c1c2n(-c3c(OC)cc(-c4cc(Cl)c(OC)cc4)c(F)c3)c(=O)ccc2cc(S(=O)(N=c2[nH]ccnc2)=O)c1',
            'O=S(NC(c1cc(Cl)c(OC2CCC(C)(C)CCC2c2ccnn2C)cc1F)=O)(C)=O',
            'c1nc(OC2CC(C)(C)Oc3cc(S(N=c4[nH]cns4)(=O)=O)ccc32)c(Cl)cc1C(F)(F)F',
            'FC(F)(F)c1cc(-c2n(CC)ncc2)c(Oc2cc(F)c(S(=O)(=O)Nc3cscn3)cc2Cl)cc1',
            'N(c1cc(F)c(S(=O)(N=c2[nH]ccs2)=O)cc1Cl)CCCCNC(CN(C)C)=O',
            'c1c(S(=O)(=O)N=c2nc[nH]cc2)cc2c(c1)C(c1c(-c3ncc(F)cc3)cc(C(F)(F)F)cc1)CN2C',
            'c1ccc(C2C(COc3ccc(S(N=c4cc[nH]cn4)(=O)=O)c(F)c3)CN(CC)C2)cc1',
            'N(C1CNCC1)(CCCCN)CCCCNc1cc(F)c(S(=O)(=O)N=c2[nH]ccs2)cc1Cl',
            'c1c(Cl)cc(-c2cc(OC)c(-n3c(=O)ccc4cc(S(=O)(N=c5cco[nH]5)=O)ccc34)cc2F)cc1OC(F)(F)F',
            'c1c(=NSc2c(Cl)cc(-c3cc(F)c(Cl)cc3OC)c(C#N)c2)nc(-c2ccccc2)[nH]c1',
            'c1c(Cl)c(NC2C(N(C)C)CC3C(Cl)=CCC32)cc(F)c1S(=O)(N=c1scc[nH]1)=O',
            'c1c2c(c(-c3ccc(C(F)(F)F)cc3OC)ncc2)ccc1S(=O)(=O)N=c1nc[nH]cc1',
            'c1cc2c(ccc(S(N=c3sc(F)c[nH]3)(=O)=O)c2)c(-c2ccc(C(F)(F)F)cc2C2=CCNCC2)c1',
            'c1(C2CC2)c(OCC2CCC(C)CC2)cc(F)c(C(NS(C2C2)(=O)=O)=O)c1',
            'Fc1ccc(C2c3c(cc(S(=O)(N=c4cc[nH]cn4)=O)cc3)OCC2)c(C2=CCNCC2)c1',
            'c1c(-c2cc(F)cc(Cl)c2)ccc(-c2ncnc3cc(S(=O)(=O)N=c4o[nH]cc4)ccc23)c1OC',
            '[nH]1ccsc1=NS(=O)(=O)c1cc(Cl)c(NC2C(N3CCCCC3)CC(C(F)(F)F)CC2)cc1F',
            'Clc1ccc(Oc2cc(F)c(S(=O)(=O)N=c3snc[nH]3)cc2F)c(-c2ccnn2C)c1',
            'Fc1cc(OCCc2ccccc2)c(C2CC2)cc1C(NS(=O)(=O)N1CCC1)=O',
            'c1c(-c2ccc(F)c(F)c2)cc(OC)c(N(c2ncc(S(=O)(=O)N=c3[nH]occ3)cc2)C(NC)=O)c1',
            'c1c(=NS(=O)(=O)c2ccc3c(ccnc3-c3c(OC)cc(-c4cccc(F)c4)cc3)c2)[nH]oc1',
            'N1CC(COc2c(Cl)cc(C(=O)NS(=O)(C)=O)c(F)c2)C1',
            'c1(NC2C(N3CC4C(C4CO)C3)CCCC2)c(Cl)cc(S(=O)(N=c2[nH]ccs2)=O)c(F)c1',
            'c12c(cc3c(c1)N(c1ccc(C(F)(F)F)cc1)CCO3)CCC(NC)C2',
            'c1c(F)c(S(N=c2scc[nH]2)(=O)=O)cc2ccnc(-c3ccc(C#N)cc3OC)c12',
            'c1c(Oc2c(Cl)cc(-c3cc(F)c(C(=O)NS(C)(=O)=O)cc3OC)cn2)c(Cl)cc(Cl)c1',
            'Fc1cc(Oc2ccc(Cl)cc2CCCN)c(N2CCOCC2)cc1S(=O)(=O)N=c1sc(F)c[nH]1',
            'c1(Cl)cc(Cl)cc(CC)c1Oc1c(C#N)cc(-c2c(OC)cc(C(NS(=O)(C)=O)=O)cc2)cn1',
            'C1C2(CCC(C(F)(F)F)CC2)CNCC12CCC2',
            'c1c(NCCCCNCC2NCC(c3ccccc3)C2)c(Cl)cc(S(N=c2[nH]cns2)(=O)=O)c1F',
            'n1c2cc(F)c(S(N=c3[nH]cns3)(=O)=O)cc2c(-c2ccccc2OC)cc1',
            'C1C2CC3CC1(COc1cc(F)c(C(NS(=O)(=O)N4CCC4)=O)cc1C1C(N)CCCC1)CC(C2)C3',
            'c1[nH]ccc(=NS(=O)(c2cc3c(cc2)N(c2cc(Cl)ccc2C#N)CCO3)=O)n1',
            'N(C(C)c1c2c(ccc1)OCCO2)c1c(Cl)cc(S(=O)(N=c2[nH]ccs2)=O)c(F)c1',
            'c1c(Oc2ccc(Cl)cc2-c2cc3c(=NS(=O)(=O)C)[nH]oc3cc2)ccc(S(N=c2[nH]ccs2)(=O)=O)c1',
            'c1(F)ncc(-c2c(F)cc(-n3c4c(cc(S(=O)(N=c5[nH]ccnc5)=O)cc4)ccc3=O)c(OC)c2)cc1',
            'Fc1cccc(=O)n1-c1cc(C)c(-c2cccc(Cl)c2OC)c1',
            'c1(F)cc(-c2cc(C(F)(F)F)ccc2Oc2c(C#N)cc(S(N=c3[nH]cns3)(=O)=O)cc2)c(OC)cc1',
            'c1cc(C(F)(F)F)ccc1C1CCC(Oc2cc(F)c(S(=O)(N=c3cc[nH]cn3)=O)cc2C)C(N(C)C)C1',
            'C1(Oc2cc(F)c(S(=O)(N=c3cc[nH]cn3)=O)c(F)c2)CC2N(Cc3cc(Cl)cc(Cl)c3)C(CC2)C1',
            'c1c2c(ccc1S(=O)(=O)N=c1[nH]nccc1)C(Nc1cc(F)c(S(=O)(=O)N=c3[nH]ccs3)cc1Cl)CC(C)(C)O2',
            '[nH]1ccsc1=NS(=NS(c1ccc2c(ccnc2-c2c(OC)cc(-c3ccc(C)c(Cl)c3)c(C#N)c2)c1)(=O)=O)=O',
            'c1(F)c(-c2cccc3c2CCN(S(=O)(N=c2snc[nH]2)=O)C3)ccc(F)c1',
            'c1c(-c2ccc(C(F)(F)F)cc2-c2ccnn2C)ccc(C(=O)NS(=O)(=O)C2CC2)c1F',
            'o1[nH]c(=NS(=O)(=O)c2c(F)cc(OC3C(c4ccnn4C)CC(O)CC3)c(Cl)c2)cc1',
            'c1cc2c(cc1S(N=c1[nH]ccs1)(=O)=O)OCCN2c1c2c(c(C)cc1)cccc2',
            'c12cc(S(=O)(N=c3[nH]cccn3)=O)ccc1c(-c1cc(C)c(-c3cc(OC)cc(OC)c3)cc1OC)ncn2',
            'c1cc(S(=O)(=O)N=c2nc[nH]cc2)cc2ccccc12',
            'c1co[nH]c1=NS(=O)(=O)c1ccc2c(ccc(=O)n2-c2ccc(-c3cc(OCC)ccc3)cc2OC)c1',
            'O=S(N=c1cco[nH]1)(c1ccc2n(-c3cc(-c4cc(OC)cc(Cl)c4)ccc3OC)c(=O)ccc2c1)=O',
            'Clc1ccc(-c2cc(OC)c(-n3c4c(ccc3=O)cc(S(N=c3[nH]cco3)(=O)=O)cc4)cc2)cc1',
            'C1OCCN(C(c2c(F)cc(F)c(Cl)c2)c2c(Cl)cccc2)C1',
            'n1(-c2ccc(-c3c(C)ccc(Cl)c3)cc2OC)c2c(ccc1=O)cc(S(N=c1cccn[nH]1)(=O)=O)cc2',
            'C1CC(C(F)(F)F)CCC1Oc1cc(F)c(C(=O)NS(N2CCC2)(=O)=O)cc1C1CC1',
            'n1(-c2cc(F)c(C(NS(C)(=O)=O)=O)cc2Cl)ncc2cc(S(=O)(=O)N=c3[nH]occ3)ccc12',
            'c1c(-c2ncnc3cc(S(=O)(N=c4cc[nH]cn4)=O)ccc32)c(OCC)cc(Cl)c1',
            'c1(-c2ccccc2F)cc(OC)c(-n2c3ccc(S(N=c4cc[nH]cn4)(=O)=O)cc3ccc2=O)cc1F',
            'CC(Oc1ncc(-c2cc(F)c(C(NS(=O)(=O)C)=O)cc2OC)cc1Cl)c1ccccc1'
        ])
        vals = [0.54785436, 0.51199263, 0.53988296, 0.6491024, 0.6448111, 0.66577786, 0.65293634, 0.6864748, 0.6770459,
                0.50656855, 0.52933055, 0.6061616, 0.53057694, 0.6699753, 0.6470201, 0.65551513, 0.4487341, 0.47132412,
                0.53764516, 0.65164775, 0.67645836, 0.676525, 0.64655364, 0.5090254, 0.64699244, 0.5020371, 0.66106236,
                0.67106295, 0.58833563, 0.6690819, 0.6187181, 0.6937064, 0.62679434, 0.63447994, 0.43496045, 0.,
                0.6682732, 0.64601994, 0.6591158, 0.4217804, 0.63641626, 0.5222816, 0.716769, 0.5139435, 0.6610465,
                0.69826317, 0.6650195, 0.5369433, 0.6169785, 0.62601924, 0.52034765, 0.51728463, 0.5238461, 0.36029583,
                0.6588155, 0.6363349, 0.60484016, 0.6891712, 0.5011976, 0.6484245, 0.5233563, 0.6513113, 0.6549425,
                0.51908314, 0.72563994, 0.6790403, 0.51625097, 0.6774275, 0.5216174, 0.67539704, 0.6359917, 0.612426,
                0.6462272, 0.7293385, 0.65199435, 0.71802187, 0.6549865, 0.6445632, 0.6451999, 0.5220306, 0.65798074,
                0.6529695, 0.6563924, 0., 0.69008875, 0.6414959, 0.68148595, 0.69654393, 0.5195591, 0.6549228,
                0.65212345, 0.4873761, 0.64038026, 0.35971507, 0.661089, 0.5080971, 0.6806261, 0.5010431, 0.3115581,
                0.6134103, 0.6000912, 0.5327473, 0.65729165, 0.64695835, 0.70536953, 0.6401583, 0., 0.72925955,
                0.68552244, 0.6364403, 0.62962675, 0., 0.5101254, 0.5388503, 0.6751181, 0.6670973, 0.63709164,
                0.44639778, 0.64214265, 0.6607938, 0.6471432, 0.35518622, 0.6379324, 0.5145776, 0.6349987, 0.6573758,
                0.64685506, 0.51633555]
        npt.assert_array_almost_equal(score.total_score, vals, 2)
