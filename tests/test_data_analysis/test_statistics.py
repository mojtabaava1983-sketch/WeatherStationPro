from data_analysis.statistics import StatisticsCalculator

def test_basic_statistics():
    values = [1, 2, 3, 4]
    assert StatisticsCalculator.mean(values) == 2.5
    assert StatisticsCalculator.median(values) == 2.5
    assert StatisticsCalculator.minimum(values) == 1
    assert StatisticsCalculator.maximum(values) == 4

def test_missing_values_are_ignored():
    assert StatisticsCalculator.mean([1, None, 3]) == 2.0

def test_stddev():
    assert StatisticsCalculator.population_stddev([1, 2, 3]) > 0
