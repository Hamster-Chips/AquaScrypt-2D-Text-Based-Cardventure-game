import deck
from card import AttackCard
import map
import json
import check_input
from terminal_utils import clear_terminal, pause

class Player():
    def __init__(self, name, load=False):
        if not load:
            self._name = name
            self._items = ["Dagger", "Boulder", "Shrimp Bottle"]
            self._location = [5, 2]
            self._deck = deck.Deck()
        else:
            print("\nWhich load file would you like to use 1, 2, or 3")
            load_choice = check_input.range_int("Choice: ", 1, 3)
            with open(f"player{load_choice}.json", "r") as files:
                data = json.load(files)
                self._name = data["player_name"]
                self._items = data["items"]
                self._location = data["location"]
                # self._deck = [AttackCard.from_dict(card) for card in data["deck"]]
                self._deck = ["deck"]

    @staticmethod
    def from_dict(data):
        return {
            "player_name": data.get('player_name'),
            "items": data.get('items'),
            "location": data.get('location'),
            "deck": data.get('deck')
        }
    
    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location
    
    def display_items(self):
        for item in self._items:
            print(item, end=", ")

    def display_deck(self):
        cards = set()
        for card in self._deck:
            cards.add(card.name)
        
        for card in cards:
            print(f"{card} (x3)")

    def save_game(self, file_name):

        deck_data = [card.__dict__ for card in self._deck]

        player_data = {
            "player_name": self._name,
            "items": self._items,
            "location": self._location,
            "deck": deck_data
        }


        deck_data = []
        for card in self._deck:
            blank = card.Card("blank", 0, 0, 0, ["None"], False)
            blank._name = card._name
            blank._cost = card._cost
            blank._power = card._power
            blank._max_hp = card._max_hp
            blank._sigil = card._sigil
            blank.barrier = card.barrier

            blank.attack_message = card.attack_message
            blank.death_message = card.death_message
            blank.description = card.description

            deck_data.append(blank)

        #    data = {
        #        "name": card._name,
        #        "cost": card._cost,
        #        "power": card._power,
        #        "max_hp": card._max_hp,
        #        "sigil": card._sigil,
        #        "barrier": card.barrier
        #    }

        
        with open(f"{file_name}.json", "w") as outfile:
            json.dump(player_data, outfile)

        
        #player_data = {
        #    "player_name": self._name,
        #    "items": self._items,
        #    "location": self._location,
        #    # card.serialize() for card in self._deck
        #    #"deck": deck
        #    "deck": deck_data
        #}
        #
        #with open(f"{file_name}.json", "w") as outfile:
        #    json.dump(player_data, outfile)


    def shop_item(self):
        print("Welcome to meh shop! \nPick whichever tickles your fancy!\n")
        print("1. Dagger - Cut out your eye and place it on scale, giving you one points toward victory.")
        print("2. Boulder - Place it to block enemies attack up to 5 hit points")
        print("3. Shrimp Bottle - A shrimp will go right into your hand")

        done = False
        while not done:
            choice = input("Your choice: ")
            if choice == "1":
                self._items.append("Dagger")
                done = True
            elif choice == "2":
                self._items.append("Boulder")
                done = True
            elif choice == "3":
                self._items.append("Shrimp Bottle")
                done = True
            else:
                print("Invalid input - between 1 - 3")
            
        print("\nYour current items:", ", ".join(self._items))
        print()
        pause()
        clear_terminal()

    def __str__(self):
        return f"Name: {self._name} \nItems: {self.displayItems()} \nDeck: {self.display_deck()}"
  
    def go_forward(self):
        m = map.Map()
        if len(self._location) - 1 < len(m) - 1:
            if self._location[0] > 0 and m[self.location[0] - 1][self.location[1]] != "-":
                self._location[0] -= 1
                return m[self.location[0]][self.location[1]]
            else:
                print("\nYou cannot go that way\n")
                return 'o'
        return 'o'

    def go_right(self):
        m = map.Map()
        if len(self._location) - 1 < len(m) - 1:
            if self._location[1] < 12 and self._location[0] > 0 and m[self.location[0] - 1][self.location[1] + 1] != "-":
                self._location[1] += 1
                self._location[0] -= 1 
                return m[self.location[0]][self.location[1]]
            else:
                print("\nYou cannot go that way\n")
                return 'o'
        else:
            return 'o'

    def go_left(self):
        m = map.Map()
        if len(self._location) - 1 < len(m) - 1:
            if self._location[1] > 0 and self._location[0] > 0 and m[self.location[0] - 1][self.location[1] - 1] != "-":
                self._location[1] -= 1
                self._location[0] -= 1
                return m[self.location[0]][self.location[1]]
            else:
                print("\nYou cannot go that way\n")
                return 'o'
        else:
            return 'o'
