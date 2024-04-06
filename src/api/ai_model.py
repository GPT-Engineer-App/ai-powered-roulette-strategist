import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Precision, Recall
import roulette
import os
import time
import logging
import roulette_config
from tensorflow.keras.layers import Dense, InputLayer

# Define bet terminology
bet_types = roulette_config.bet_types
bet_values = roulette_config.bet_values

# Clear the terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('absl').setLevel(logging.ERROR)

start_time = time.time()

# Create a MirroredStrategy object
mirrored_strategy = tf.distribute.MirroredStrategy()

epochs = 10  # Set the number of epochs you want to train for
num_rounds = 100  # Set the number of rounds per epoch
INITIAL_BALANCE = 100000  # Set the initial balance
balance = INITIAL_BALANCE

def format_input(sequence):
    return np.array([sequence]).reshape(1, 3)

with mirrored_strategy.scope():
    input_shape = (3,)
    num_layers = 2  # Set the desired number of layers
    nodes_per_layer = [64, 32]  # Set the desired number of nodes per layer
    activation_functions = ['relu', 'relu']  # Set the desired activation functions

    def model(input_shape, num_layers, nodes_per_layer, activation_functions, training=False):
        model = Sequential()
        model.add(InputLayer(input_shape=input_shape))
        for i in range(num_layers):
            model.add(Dense(nodes_per_layer[i], activation=activation_functions[i]))
        model.add(Dense(len(roulette.bet_types), activation='softmax'))
        model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=[Precision(), Recall()])
        return model

    for epoch in range(epochs):
        print(f"Epoch {epoch+1}/{epochs}")
        balance = INITIAL_BALANCE
        distributed_dataset = mirrored_strategy.experimental_distribute_dataset(
            tf.data.Dataset.from_tensor_slices((format_input(np.array([int(balance > 0), 0, 0])), np.zeros((1, len(roulette.bet_types))))).batch(1)
        )
        for round_num in range(num_rounds):
            @tf.function
            def train_step(sequence, target):
                with tf.GradientTape() as tape:
                    predictions = model(sequence, training=True)
                    loss = model.loss(target, predictions)
                gradients = tape.gradient(loss, model.trainable_variables)
                model.optimizer.apply_gradients(zip(gradients, model.trainable_variables))
                return loss, predictions

            sequence, target = next(iter(distributed_dataset))
            loss, predictions = mirrored_strategy.run(train_step, args=(sequence, target))
            bet_type = list(roulette.bet_types.keys())[tf.argmax(predictions[0])]
            bet_amount = roulette.bet_values[np.random.randint(len(roulette.bet_values))]
            print(f"Round {round_num+1}/{num_rounds}: Predicted bet: {bet_type} (${bet_amount})")

            spin_result, spin_color, payout, balance = roulette.play_round(bet_type, bet_amount, balance)
            print(f"Spin result: {spin_result} ({spin_color}), Payout: {payout}, Current balance: {balance}")

def print_roulette_table(spin_result, spin_color):
    roulette_table = """
    +-------+-------+-------+
    | 00    | 0     | 1-18  |
    +-------+-------+-------+
    | 2     | 3     | 4     |
    +-------+-------+-------+
    | 5     | 6     | 7     |
    +-------+-------+-------+
    | 8     | 9     | 10    |
    +-------+-------+-------+
    | 11    | 12    | 13    |
    +-------+-------+-------+
    | 14    | 15    | 16    |
    +-------+-------+-------+
    | 17    | 18    | 19-36 |
    +-------+-------+-------+
    """

    for i, char in enumerate(roulette_table):
        if char.isdigit():
            number = int(char)
            if number == spin_result:
                if spin_color == 'red':
                    print(f"\033[1;31m{char}\033[0m", end="")
                elif spin_color == 'black':
                    print(f"\033[1;30m{char}\033[0m", end="")
                else:
                    print(f"\033[1;32m{char}\033[0m", end="")
            else:
                print(char, end="")
        else:
            print(char, end="")
    print()

while True:
    try:
        distributed_dataset = mirrored_strategy.experimental_distribute_dataset(
        tf.data.Dataset.from_tensor_slices((format_input(np.array([int(balance > 0), 0, 0])), np.zeros((1, len(roulette.bet_types))))).batch(1)
        )
        
        mode = input('Enter "train" for training mode, "operate" for operation mode, "edit" for editing the model, or "exit" to quit:\n')

        if mode.lower() == 'exit':
            break
        elif mode.lower() == 'train':
            epochs = int(input('Enter the number of epochs for training:\n'))
            num_rounds = int(input('Enter the number of rounds per epoch:\n'))
            with mirrored_strategy.scope():
                for epoch in range(epochs):
                    print(f"Epoch {epoch+1}/{epochs}")
                    balance = INITIAL_BALANCE
                    distributed_dataset = mirrored_strategy.experimental_distribute_dataset(
                        tf.data.Dataset.from_tensor_slices((format_input(np.array([int(balance > 0), 0, 0])), np.zeros((1, len(roulette.bet_types))))).batch(1)
                    )
                    for round_num in range(num_rounds):
                        @tf.function
                        def train_step(sequence, target):
                            with tf.GradientTape() as tape:
                                predictions = model(sequence, num_layers, nodes_per_layer, activation_functions, training=True)
                                loss = model.loss(target, predictions)
                            gradients = tape.gradient(loss, model.trainable_variables)
                            model.optimizer.apply_gradients(zip(gradients, model.trainable_variables))
                            return loss, predictions

                        sequence, target = next(iter(distributed_dataset))
                        loss, predictions = mirrored_strategy.run(train_step, args=(sequence, target))
                        bet_type = list(roulette.bet_types.keys())[tf.argmax(predictions[0])]
                        bet_amount = roulette.bet_values[np.random.randint(len(roulette.bet_values))]
                        print(f"Round {round_num+1}/{num_rounds}: Predicted bet: {bet_type} (${bet_amount})")

                        spin_result, spin_color, payout, balance = roulette.play_round(bet_type, bet_amount, balance)
                        print(f"Spin result: {spin_result} ({spin_color}), Payout: {payout}, Current balance: {balance}")
            print(f"Epoch {epoch+1}/{epochs} completed. Final balance: {balance}")
        elif mode.lower() == 'operate':
            # Generate predictions from the model
            predictions = model(format_input(np.array([int(balance > 0), 0, 0])), training=False)
            bet_types = [list(roulette.bet_types.keys())[np.argmax(prediction)] for prediction in predictions[0]]
            bet_amounts = [roulette.bet_values[np.random.randint(len(roulette.bet_values))] for _ in range(len(bet_types))]
            print(f"Predicted bets: {', '.join([f'{bet_type} (${bet_amount})' for bet_type, bet_amount in zip(bet_types, bet_amounts)])}")

            # Get the actual spin result from roulette.py
            spin_result, spin_color, payout, balance = roulette.play_round(bet_types, bet_amounts, balance)
            print_roulette_table(spin_result, spin_color)
            print(f"Spin result: {spin_result} ({spin_color}), Total payout: {payout}, Current balance: {balance}")
        elif mode.lower() == 'edit':
            input_shape = (3,)
            num_layers = int(input('Enter the number of hidden layers (excluding input and output layers):\n'))
            nodes_per_layer = []
            activation_functions = []
            for i in range(num_layers + 1):
                if i == 0:
                    nodes_per_layer.append(int(input(f'Enter the number of nodes for the input layer:\n')))
                    activation_functions.append(input(f'Enter the activation function for the input layer (e.g., "relu"):\n'))
                elif i == num_layers:
                    activation_functions.append('softmax')  # Output layer activation is fixed to softmax
                else:
                    nodes_per_layer.append(int(input(f'Enter the number of nodes for hidden layer {i}:\n')))
                    activation_functions.append(input(f'Enter the activation function for hidden layer {i} (e.g., "relu"):\n'))
            model = create_model(input_shape, num_layers, nodes_per_layer, activation_functions)
            print("Model architecture updated successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

# Save the model when the program exits
model.save('my_model.h5')
print("Program exited. Model saved successfully!")