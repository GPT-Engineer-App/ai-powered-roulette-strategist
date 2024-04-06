import numpy as np
import decimal

bet_types = {
    'straight': 35,
    'split': 17,
    'street': 11,
    'corner': 8,
    'five': 6,
    'sixline': 5,
    'basket': 6,
    'dozen': 2,
    'column': 2,
    'red': 1,
    'black': 1,
    'even': 1,
    'odd': 1,
    'low': 1,
    'high': 1
}

bet_values = [1, 5, 10, 25, 50, 100]

def spin_roulette():
    spin_result = np.random.randint(37)
    if spin_result == 0:
        spin_color = 'green'
    elif spin_result % 2 == 0:
        spin_color = 'red'
    else:
        spin_color = 'black'
    return spin_result, spin_color

def get_winning_bet(spin_result):
    if spin_result == 0:
        return 'basket'
    elif spin_result in range(1, 37):
        return 'straight'
    else:
        raise ValueError(f"Invalid spin result: {spin_result}")

def play_round(bet_types, bet_amounts, balance):
    spin_result, spin_color = spin_roulette()
    total_payout = 0
    for bet_type, bet_amount in zip(bet_types, bet_amounts):
        payout = bet_types[bet_type] * bet_amount if bet_type == get_winning_bet(spin_result) else 0
        total_payout += payout
        balance -= bet_amount
    balance += total_payout
    return spin_result, spin_color, total_payout, balance