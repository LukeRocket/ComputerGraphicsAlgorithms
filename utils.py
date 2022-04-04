def cumulative_average(mean: float, sample: float, n: int) -> float:
    n += 1
    mean += (sample - mean) / n
    return mean
