from typing import List

import numpy as np
from rdkit import Chem

from reinvent_scoring.scoring.score_components import BaseScoreComponent


def score(component: BaseScoreComponent, smiles: List[str]) -> np.array:
    """Calculates score for a list of SMILES strings."""
    mols = [Chem.MolFromSmiles(s) for s in smiles]
    score = component.calculate_score(mols)
    return score.total_score


def score_single(component: BaseScoreComponent, smi: str) -> float:
    """Calculates score for a single SMILES string."""
    mol = Chem.MolFromSmiles(smi)
    score = component.calculate_score([mol])
    return score.total_score[0]


celecoxib = 'O=S(=O)(c3ccc(n1nc(cc1c2ccc(cc2)C)C(F)(F)F)cc3)N'
random_compound = "C1C2C([N+](=O)[O-])C(C(=O)O)C1C=C2"
