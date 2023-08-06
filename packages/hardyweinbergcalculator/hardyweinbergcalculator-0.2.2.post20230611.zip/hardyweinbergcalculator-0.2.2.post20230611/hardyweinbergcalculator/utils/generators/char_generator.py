import random


# --------------------------------------------------------------------------- #
def random_chars(n: int = 1):
    """Generate a random character from the alphabet."""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    yield random.choice(characters)

# --------------------------------------------------------------------------- #
