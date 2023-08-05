import sys

from termcolor import colored

from imppkg.harmonic_mean import harmonic_mean


def _parse_nums(input: list[str]) -> list[float]:
    try:
        return [float(arg) for arg in input]
    except ValueError:
        return []


def _calculate_result(nums: list[float]) -> float:
    result = 0.0
    try:
        result = harmonic_mean(nums)
    except ZeroDivisionError:
        pass
    return result


def _format_output(result: float) -> str:
    return colored(str(result), "red", "on_yellow", attrs=["bold"])


def main():
    print(_format_output(_calculate_result(_parse_nums(sys.argv[1:]))))
