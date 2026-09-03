from data_analysis.models import Observation
from data_analysis.quality import quality_score, acceptable

def test_quality_is_bounded():
    o=Observation.__new__(Observation)
    object.__setattr__(o,"quality",120)
    assert quality_score(o)==100

def test_acceptance():
    o=Observation.__new__(Observation)
    object.__setattr__(o,"quality",80)
    assert acceptable(o,80)
