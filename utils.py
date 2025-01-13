import random

def random_account_number():
    return str(random.randint(10**9, 10**10 - 1))
