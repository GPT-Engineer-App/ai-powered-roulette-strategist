import numpy as np
import decimal

bet_types = {
    'straight': 12,  # Any single number
    '1-6': 1.95,     # First two columns: 1, 2, 3, 4, 5, 6
    '4-9': 1.95,     # Middle two columns: 4, 5, 6, 7, 8, 9
    '7-12': 1.95,    # Last two columns: 7, 8, 9, 10, 11, 12
    'even': 1.95,    # All even numbers
    'odd': 1.95,     # All odd numbers
    '2to1_1': 2.95,  # Line bet: 3, 6, 9, 12
    '2to1_2': 2.95,  # Line bet: 2, 5, 8, 11
    '2to1_3': 2.95,  # Line bet: 1, 4, 7, 10
    'red': 1.95,     # All red numbers
    'black': 1.95    # All black numbers
}

bet_values = [1, 5, 10, 25, 50, 100]

def spin_roulette():
    spin_result = np.random.randint(1, 13)
    if spin_result in [1, 3, 5, 7, 9, 11]:
        spin_color = 'red'
    else:
        spin_color = 'black'
    return spin_result, spin_color

def get_winning_bet(spin_result):
    if spin_result in range(1, 13):
        return 'straight'
    elif spin_result in range(1, 7):
        return '1-6'
    elif spin_result in range(4, 10):
        return '4-9'
    elif spin_result in range(7, 13):
        return '7-12'
    elif spin_result % 2 == 0:
        return 'even'
    else:
        return 'odd'

def play_round(bet_type, bet_amount, balance):
    spin_result, spin_color = spin_roulette()
    payout = 0
    if bet_type == 'straight' and bet_type == get_winning_bet(spin_result):
        payout = bet_types[bet_type] * bet_amount
    elif bet_type in ['1-6', '4-9', '7-12'] and spin_result in bet_type_range[bet_type]:
        payout = bet_types[bet_type] * bet_amount
    elif bet_type in ['even', 'odd'] and bet_type == get_winning_bet(spin_result):
        payout = bet_types[bet_type] * bet_amount
    elif bet_type in ['2to1_1', '2to1_2', '2to1_3'] and spin_result in bet_type_range[bet_type]:
        payout = bet_types[bet_type] * bet_amount
    elif bet_type in ['red', 'black'] and spin_color == bet_type:
        payout = bet_types[bet_type] * bet_amount
    balance -= bet_amount
    balance += payout
    return spin_result, spin_color, payout, balance