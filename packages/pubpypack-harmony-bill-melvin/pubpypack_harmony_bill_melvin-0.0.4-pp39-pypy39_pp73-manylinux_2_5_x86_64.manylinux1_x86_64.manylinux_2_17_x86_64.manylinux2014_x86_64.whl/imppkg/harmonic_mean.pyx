from typing import List


def harmonic_mean(measurements: List[float]):
    n = sum([1 / m for m in measurements])
    return len(measurements) / n


if __name__ == "__main__":
    nums = [float(i) for i in range(1, 10)]
    print(harmonic_mean(nums))
