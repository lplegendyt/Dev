import pyautogui
import time
import random
import numpy as np
from PIL import ImageGrab
from collections import deque
import tensorflow as tf
from tensorflow import keras
from tensorflow import kmodels
from tensorflow import optimizersfrom 
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten  # Example layers
import keyboard

# Hyperparameters
state_space_size = 10  # Size of state representation (10x10 grid)
action_space_size = 18  # Number of actions
gamma = 0.95  # Discount factor
epsilon = 1.0  # Exploration-exploitation tradeoff
epsilon_min = 0.01  # Minimum epsilon
epsilon_decay = 0.995  # Epsilon decay rate
learning_rate = 0.001  # Learning rate for neural network
batch_size = 32  # Batch size for experience replay
memory = deque(maxlen=2000)  # Replay memory
mouse_control_enabled = True  # Flag to control mouse

# Build the neural network
def build_model():
    model = Sequential()
    model.add(Dense(24, input_dim=state_space_size * state_space_size, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(action_space_size, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(learning_rate=learning_rate))
    return model

# Initialize model
model = build_model()

def get_screenshot():
    screen = ImageGrab.grab(bbox=(0, 40, 800, 640))  # Adjust coordinates as necessary
    screen = screen.convert('L')  # Convert to grayscale
    return np.array(screen)

def get_state():
    # Capture screen and preprocess the image to get the current state
    screen = get_screenshot()
    screen = screen.resize((state_space_size, state_space_size), Image.NEAREST)
    state = np.array(screen).flatten()
    return state

def check_for_resource_collection():
    global previous_state
    current_state = get_screenshot()

    if previous_state is None:
        previous_state = current_state
        return False

    # Simple pixel change detection
    difference = np.abs(current_state - previous_state)
    if np.sum(difference) > 50000:  # Adjust threshold as needed
        previous_state = current_state
        return True

    previous_state = current_state
    return False

def check_for_damage():
    screen = get_screenshot()
    # Assuming damage is indicated by a red tint, adjust to actual indication
    damage_indicator = np.mean(screen)  # Placeholder for actual damage detection logic
    return damage_indicator < 100  # Adjust threshold based on actual indicator

def check_for_enemy_defeat():
    # Placeholder logic: detect specific text or visual indication of enemy defeat
    return False  # Replace with actual detection logic

def check_for_new_area():
    screen = get_screenshot()
    # Placeholder logic to detect a new area
    new_area_indicator = np.mean(screen)  # Replace with actual area detection
    return new_area_indicator > 200  # Adjust threshold based on actual indicator

def get_reward():
    reward = 0
    if check_for_resource_collection():
        reward += 10
    if check_for_damage():
        reward -= 10
    if check_for_enemy_defeat():
        reward += 20
    if check_for_new_area():
        reward += 5
    return reward

def choose_action(state):
    if np.random.rand() <= epsilon:
        return random.randint(0, action_space_size - 1)  # Explore
    else:
        q_values = model.predict(state.reshape(1, -1))
        return np.argmax(q_values[0])  # Exploit

def perform_action(action):
    if action == 0:
        pyautogui.keyDown('w')  # Move forward
        time.sleep(0.1)
        pyautogui.keyUp('w')
    elif action == 1:
        pyautogui.keyDown('s')  # Move backward
        time.sleep(0.1)
        pyautogui.keyUp('s')
    elif action == 2:
        pyautogui.keyDown('a')  # Move left
        time.sleep(0.1)
        pyautogui.keyUp('a')
    elif action == 3:
        pyautogui.keyDown('d')  # Move right
        time.sleep(0.1)
        pyautogui.keyUp('d')
    elif action == 4:
        pyautogui.press('space')  # Jump
    elif action == 5:
        pyautogui.click(button='left')  # Attack/Use item
    elif action == 6:
        pyautogui.press('e')  # Open inventory/interact
    elif action == 7:
        pyautogui.keyDown('shift')  # Sneak
        time.sleep(0.1)
        pyautogui.keyUp('shift')
    elif action == 8:
        pyautogui.keyDown('ctrl')  # Sprint
        time.sleep(0.1)
        pyautogui.keyUp('ctrl')
    elif action == 9:
        pyautogui.press('1')  # Select hotbar slot 1
    elif action == 10:
        pyautogui.press('2')  # Select hotbar slot 2
    elif action == 11:
        pyautogui.press('3')  # Select hotbar slot 3
    elif action == 12:
        pyautogui.press('4')  # Select hotbar slot 4
    elif action == 13:
        pyautogui.click(button='right')  # Place block/interact with right click
    elif action == 14:
        if mouse_control_enabled:
            pyautogui.moveRel(30, 0)  # Look right
    elif action == 15:
        if mouse_control_enabled:
            pyautogui.moveRel(-30, 0)  # Look left
    elif action == 16:
        if mouse_control_enabled:
            pyautogui.moveRel(0, 30)  # Look down
    elif action == 17:
        if mouse_control_enabled:
            pyautogui.moveRel(0, -30)  # Look up

def replay():
    minibatch = random.sample(memory, batch_size)
    for state, action, reward, next_state, done in minibatch:
        target = reward
        if not done:
            target = reward + gamma * np.amax(model.predict(next_state.reshape(1, -1))[0])
        target_f = model.predict(state.reshape(1, -1))
        target_f[0][action] = target
        model.fit(state.reshape(1, -1), target_f, epochs=1, verbose=0)

def main():
    global epsilon
    global mouse_control_enabled
    global previous_state

    previous_state = None

    for episode in range(1000):  # Number of episodes
        state = get_state()
        total_reward = 0

        for t in range(100):  # Number of timesteps per episode
            # Check for the toggle key press (e.g., 'm' key)
            if keyboard.is_pressed('ctrl+shift+m'):
                mouse_control_enabled = not mouse_control_enabled
                print(f"Mouse control {'enabled' if mouse_control_enabled else 'disabled'}")

            action = choose_action(state)
            perform_action(action)
            time.sleep(0.1)  # Adjust time step as needed
            next_state = get_state()
            reward = get_reward()
            done = False  # Define your termination condition

            # Check for a stopping condition
            if t == 99:  # Example: end of episode after 100 timesteps
                done = True

            memory.append((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward

            if len(memory) > batch_size:
                replay()

            if done:
                break

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        print(f"Episode {episode} Total Reward: {total_reward}")

if __name__ == "__main__":
    main()
