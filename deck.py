import card 
import random
import check_input
from cards.tropical import dolphin, otter, turtle
from cards.oceanic import leviathan, manta_ray, shark
from cards.abyssal import angler, jellyfish, kraken
from terminal_utils import clear_terminal, pause, delay_print, delay_input, delay

class Deck:

    def __init__(self, load=False):
        self._cards = []
                
        enemies = [dolphin.Dolphin(), otter.Otter(), turtle.Turtle(),
                    leviathan.Leviathan(), manta_ray.MantaRay(), shark.Shark(),
                    angler.Angler(), jellyfish.Jellyfish(), kraken.Kraken()]

        for i in enemies:
            for j in range(3):
                self._cards.append(i)

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        self._i += 1
        if self._i >= len(self._cards):
            raise StopIteration
        else:
            return self._cards[self._i]
    
    def __len__(self):
        """
        return the number of cards remaining in the deck.
        """
        return len(self._cards)

    def __str__(self):
        for card in self._cards:
            print(card)
        
    def shuffle(self):
        """
        shuffles the deck.
        """
        random.shuffle(self._cards)
    
    def draw_card(self):
        """
        remove the topmost card from the deck and return it.
        """
        if len(self._cards) > 0:
            top_card = self._cards.pop(0)
            return top_card

    def remove_card(self, index):
        return self._cards.pop(index)

    def choose_card(self, text, remove_duplicates=False, return_index=False):
        if remove_duplicates:
            one_card = []
            seen = set()
            for card in self._cards:
                if card not in seen:
                    one_card.append(card)
                    seen.add(card)
            display_cards = one_card
        else:
            display_cards = self._cards
        

        if all(card is None for card in display_cards):
            return None
        else:
            print(text)
            counter = 1 
            for card in display_cards:
                print(f"{counter}. {card}")
                print()
                counter += 1

            valid = False
            while not valid:
                choice = check_input.range_int("Enter choice: ", 1, counter - 1)

                if display_cards[choice - 1] is not None:
                    if return_index:
                        return display_cards[choice - 1], choice - 1
                    else:
                        return display_cards[choice - 1]
                else:
                    print("There's no card there, choose again. ")

    def sacrifice(self):
        print("------------- Sacrifice -------------")
        print("Here you will sacrifice a card and either transfer its sigil or one of the its stats to another ...\n")
        pause()
        clear_terminal()

        card, idx = self.choose_card("Choose a card to sacrifice (You will lose one of this card)",remove_duplicates=True, return_index=True)
        idx *=3
        sac_card = self._cards[idx]
        self.remove_card(idx)
        print(f"You have chosen the {sac_card.name}\n")
        pause()
        clear_terminal()
        print(f"What would you like to transfer the: \n1. {sac_card.sigil} sigil \n2. Cost ({sac_card.cost}) \n3. Power ({sac_card.power}) \n4. Health ({sac_card.hp})")
        gain_choice = check_input.range_int("\nEnter choice: ", 1, 4)
        print()
        pause()
        clear_terminal()
            
        card, idx = self.choose_card("Now choose a card to gain its new stat or sigil",remove_duplicates=True, return_index=True)
        gain_card = card
        print()
        clear_terminal()

        print(gain_card)
        print("\nturned to\n")

        if gain_choice == 1:
            if isinstance(gain_card.sigil, list):
                gain_card.sigil.extend(sac_card.sigil)
            else:
                gain_card.sigil = [gain_card.sigil, sac_card.sigil]
        elif gain_choice == 2:
            gain_card.cost = sac_card.cost
        elif gain_choice == 3:
            gain_card.power = sac_card.power
        else:
            gain_card.hp = sac_card.hp
            gain_card.max_hp = sac_card.max_hp
        
        print(gain_card)
        print()
        pause()
        clear_terminal()

    def upgrade(self):
        print("------------- Upgrade -------------")
        card, idx = self.choose_card("Choose a card to upgrade ",remove_duplicates=True, return_index=True)
        print(f"\nYou chose the {card.name}\n")
        pause()
        clear_terminal()

        cards = random.randint(1,2)
        if cards == 1:
            print("You came to visit Aquaman, and he grants you more ... POWER")
            print(f"Your power has been upgraded from {str(card._power)} to {str(card._power + 1)}\n")
            card._power += 1
        else:
            print("You came to visit Aquaman, and he grants you more ... HEALTH")
            print(f"Your max health has been upgraded from {str(card._max_hp)} to {str(card._max_hp + 2)}\n")
            card._max_hp += 2
            card._hp +=2

        player_choice = check_input.yes_no(f"Aquaman is getting angry\nWould you like to upgrade again? (50% chance)\nIf you're unlucky then you will loss all you cards with the same name. Y/N: ")
        chance = 50
        while player_choice and chance > 0 :
            random_num = random.randint(1,100)
            if chance == 50:
                if not self.upgrade_chance(idx, random_num, card, chance, 
                    "Aquaman is willing to answer your prayers!", 
                    "Aquaman is too hungry to care about you ... he ate your fish as a snack."):
                    chance = 0
            elif chance == 25:
                if not self.upgrade_chance(idx, random_num, card, chance, 
                    "Aquaman is surprisingly in a happy mood today!", 
                    "Your luck runs out, Aquaman sent your lil fish to fish jail."): 
                    chance = 0
            elif chance == 12:
                if not self.upgrade_chance(idx, random_num, card, chance, 
                    "It seems like Aquaman is starting to like you!", 
                    "You got way too greedy, Aquaman has stolen your fish and now the fish serves him."):
                    chance = 0
            elif chance == 6:
                if not self.upgrade_chance(idx, random_num, card, chance, 
                    "You're crazy! Aquaman is astonished!", 
                    "Your time has come to end"):
                    chance = 0
            elif chance == 3:
                if not self.upgrade_chance(idx, random_num, card, chance, 
                    "You won't do it again ... Aquaman challenges you ...", 
                    "Aquaman now wants the fish ... not you, go away."):
                    chance = 0
            elif chance == 1:
                if not self.upgrade_chance(idx, random_num, card, chance, 
                    "Congrants you did it!! You have bested Aquaman!", 
                    "so close ... yet so far ..."):
                    chance = 0

            chance //= 2
            if chance is not 0: 
                player_choice = check_input.yes_no(f"Would you like to upgrade again? (" + str(chance) + '%' " chance) Y/N: ")
                         
        print()
        pause()
        clear_terminal()
        
    def upgrade_chance(self, idx, random_num, card, chance, congrats_text, failed_text):
        if random_num <= chance:
            print(congrats_text)
            random_num2 = random.randint(1,2)
            if random_num2 == 1:
                card._power += 1
                print("Your power has been upgraded to " + str(card._power) + "\n")
            else:
                card._max_hp += 2
                card._hp += 2
                print("Your max health has been upgraded to " + str(card._max_hp) + "\n")
            return True
        else:
            idx *= 3
            while idx < len(self._cards):
                if self._cards[idx].name == card.name:
                    self.remove_card(idx)
                else:
                    print(failed_text)
                    return False 

        

