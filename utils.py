def cumulative_average(mean: float, sample: float, n: int) -> float:
    mean += (sample - mean) / n
    return mean
