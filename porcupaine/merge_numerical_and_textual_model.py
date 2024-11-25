from statistics import median


def combine_chances(*chances: float):

    # The following function calculates and returns the desired combinations of the provided chances

    average_value = sum(chances) / len(chances)
    median_value = median(chances)
    max_value = max(chances)
    min_value = min(chances)

    return {"Average": average_value, "Median": median_value, "Maximum": max_value, "Minimum": min_value}


def print_chances(comb: dict[str, float]):

    # The function accesses the values from combine_chances and prints them

    print(f"Šance na úspěch (avg): {comb ['Average']:.2f}%")
    print(f"Šance na úspěch (med): {comb ['Median']:.2f}%")
    print(f"Šance na úspěch (max): {comb ['Maximum']:.2f}%")
    print(f"Šance na úspěch (min): {comb ['Minimum']:.2f}%")


if __name__ == "__main__":
    # Get results from combine_chances function and store them in 'combinations'
    # Example values in brackets
    combinations = combine_chances(0.5,0.9,0.4,0.99,0.25)

    # Print the results using print_chances function
    print_chances(combinations)
