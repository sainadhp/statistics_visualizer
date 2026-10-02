import numpy as np

def calculate_mean(data):
    return np.mean(data)


# def calculate_median(data):
#     sorted_data = sorted(data)

#     n = len(sorted_data)
#     middle = n // 2
#     if n % 2 == 1:
#         return sorted_data[middle]

#     return (sorted_data[middle - 1] + sorted_data[middle]) / 2



def calculate_median(data):
    """Middle value after sorting (average of the two middle values if n is even)."""
    return float(np.median(data))


def calculate_mode(data):
    """
    Most frequent value(s). Returns a list because data can have:
      - one mode       [3, 7, 7]       -> [7]
      - several modes  [1, 1, 2, 2, 3] -> [1, 2]
      - no mode        [1, 2, 3]       -> []   (every value appears once)
    """
    values, counts = np.unique(data, return_counts=True)
    if counts.max() == 1:
        return []
    return [float(v) for v in values[counts == counts.max()]]


def frequencies(data):
    """{value: count} sorted by value. Used by the mode page and mode animation."""
    values, counts = np.unique(data, return_counts=True)
    return {float(v): int(c) for v, c in zip(values, counts)}