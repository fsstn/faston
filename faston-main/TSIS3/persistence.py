import json
import os

SETTINGS_FILE = 'settings.json'
LEADERBOARD_FILE = 'leaderboard.json'

def load_settings():
    # load settings from json, or create it with defaults if it's not there
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    default = {"sound": True, "car_color": "red", "difficulty": "normal"}
    save_settings(default)
    return default

def save_settings(settings):
    # save the current settings to the json file
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    # load the high scores from json, or return an empty list if it doesn't exist
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return []

def save_score(name, score, distance):
    # add a new score, sort the list, and save the top 10
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance})
    board = sorted(board, key=lambda x: x['score'], reverse=True)[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(board, f, indent=4)