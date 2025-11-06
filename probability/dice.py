from random import random


class Dice:
    """A class representing a six-sided dice."""

    def __init__(self):
        pass

    def roll(self) -> int:
        """Roll the dice and return a new random value between 1 and 6."""
        return int(random() * 6) + 1

    def roll_multiple(self, times: int) -> dict:
        """Roll the dice multiple times and return a dictionary of results."""

        results = []
        for _ in range(times):
            results.append(self.roll())

        relative_frequencies = {}
        for side in range(1, 7):
            relative_frequencies[side] = results.count(side) / times

        data = {
            "rolled_times": times,
            "results": results,
            "total": sum(results),
            "average": (sum(results) / times if times > 0 else 0),
            "relative_frequencies": relative_frequencies,
        }

        return data


if __name__ == "__main__":
    dice = Dice()
    rolls = dice.roll_multiple(10000000)
    print(f"relative frequencies for {rolls['rolled_times']} rolls: {rolls['relative_frequencies']}")
