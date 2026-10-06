import json
import os

class LocationHistoryStore:
    def __init__(self, history_file='data/history.json', favourites_file='data/favourites.json'):
        self.history_file = history_file
        self.favourites_file = favourites_file

        folder = os.path.dirname(self.history_file)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

    def save_reading(self, reading):
        history = self.load_history()
        history.append(reading.to_dict())

        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2)
        except IOError as e:
            print(f'Could not save reading: {e}')

    def load_history(self):
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f'Could not read history file, starting fresh: {e}')
            return []

    def add_favourite(self, location_name):
        favourites = self.load_favourites()
        if location_name not in favourites:
            favourites.append(location_name)

        try:
            with open(self.favourites_file, 'w', encoding='utf-8') as f:
                json.dump(favourites, f, indent=2)
        except IOError as e:
            print(f'Could not save favourite: {e}')

    def load_favourites(self):
        if not os.path.exists(self.favourites_file):
            return []
        try:
            with open(self.favourites_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f'Could not read favourites file, starting fresh: {e}')
            return []
