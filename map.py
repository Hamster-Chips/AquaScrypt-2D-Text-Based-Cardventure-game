import random

class Map:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Map._initialized:
            self._maps = {}
            self._current_map = None
            Map._initialized = True 

    def load_map(self, map_name, file_path):
        map_data = []
        with open(file_path, "r") as f:
            for line in f:
                map_data.append(list(line.strip()))
        self._maps[map_name] = map_data
        if self._current_map is None:
            self._current_map = map_name
        self._place_random_elements(map_name)

    def switch_map(self, map_name, player):
        if map_name in self._maps:
            self._current_map = map_name
            self._set_initial_player_position(player)
    
    def _place_random_elements(self, map_name):
        elements = ['V', 'U', 'A', 'I', '?']
        map_data = self._maps[map_name]

        for i in range(len(map_data)):
            for j in range(len(map_data[i])):
                if map_data[i][j] == '*':
                    map_data[i][j] = random.choice(elements)

    def _set_initial_player_position(self, player):
        """Sets the player's initial position to 's' on the current map."""
        for i, row in enumerate(self._maps[self._current_map]):
            for j, char in enumerate(row):
                if char == 'S':
                    player._location = [i, j]
                    return
                

    def __getitem__(self, row):
        """overloaded [] operator – returns the specified row from the map."""
        return self._map[row]

    def __len__(self):
        """Returns the number of rows in the map list"""
        return len(self._map)
    
    def show_map(self, loc):
        """
        returns the map as a string in the format of a 6x6 matrix of
        characters where revealed locations are the characters from the map, unrevealed
        locations are ‘x’s, and the hero’s location is a ‘*’
        """
      
        self._map = self._maps[self._current_map]
        
        str_map = ""
        for i in range(len(self._map)):
            for j in range(len(self._map[i])):
                if i == loc[0] and j == loc[1]:
                    str_map += "@ "
                else:
                    str_map += self._map[i][j] + " "
            str_map += "\n\n"
        return str_map
