import card 
import random
import check_input
from cards.tropical import dolphin, otter, turtle
from cards.oceanic import leviathan, manta_ray, shark
from cards.abyssal import angler, jellyfish, kraken
from terminal_utils import clear_terminal, pause, delay_print, delay_input, delay

import copy

class Deck:

    def __init__(self, load=False):
        self._cards = []

        if load == True:
            print("Using loaded deck")
        
        else:      
            enemies = [dolphin.Dolphin(), otter.Otter(), turtle.Turtle(),
                        leviathan.Leviathan(), manta_ray.MantaRay(), shark.Shark(),
                        angler.Angler(), jellyfish.Jellyfish(), kraken.Kraken()]

            for i in enemies:
                for j in range(3):
                    temp = copy.deepcopy(i)
                    self._cards.append(temp)

            # TEST
            #for card in self._cards:
            #    print(f"{card.name} Health: {card.hp}")

            #self._cards[0].hp += 2
            #print("-----------------------------------------------")

            #for card in self._cards:
            #    print(f"{card.name} Health: {card.hp}")
            
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
                if card.name not in seen:
                    one_card.append(card)
                    seen.add(card.name)  
            display_cards = one_card
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
        cards_copy = list(self._cards) 
        card, idx = self.choose_card("Choose a card to sacrifice (You will lose one of this card)",remove_duplicates=True, return_index=True) # Set remove_duplicate to False to get exact index tho may not look as nice
        idx *=3 
        count = 0
        sac_card = self._cards[idx]
        for i, card in enumerate(cards_copy):
                if card.name == sac_card.name:
                    self.remove_card(idx)
                    count += 1
                    if count == 3:
                        break

        print(f"You have chosen the {sac_card.name}\n")
        pause()
        clear_terminal()
        print(f"What would you like to transfer the: \n1. {sac_card.sigil} sigil \n2. Cost ({sac_card.cost}) \n3. Power ({sac_card.power}) \n4. Health ({sac_card.hp})")
        gain_choice = check_input.range_int("\nEnter choice: ", 1, 4)
        print()
        pause()
        clear_terminal()
        
        gain_card, idx = self.choose_card("Now choose a card to gain its new stat or sigil",remove_duplicates=True, return_index=True) 
        idx *= 3

        print()
        clear_terminal()

        print(gain_card)
        print("\nturned to\n")
        target_card_name = self._cards[idx].name 
        if gain_choice == 1:
            if isinstance(gain_card.sigil, list):
                for i, card in enumerate(self._cards):
                    if card.name == target_card_name:
                        self._cards[idx].sigil.extend(sac_card.sigil)
                        idx +=1
            else:
                for i, card in enumerate(self._cards):
                    if card.name == target_card_name:
                        self._cards[idx].sigil = [gain_card.sigil, sac_card.sigil]
                        idx +=1
        elif gain_choice == 2:
            for i, card in enumerate(self._cards):
                if card.name == target_card_name:
                    self._cards[idx].cost = sac_card.cost
                    idx +=1
        elif gain_choice == 3:
            for i, card in enumerate(self._cards):
                if card.name == target_card_name:
                    print(idx)
                    self._cards[idx].power = sac_card.power
                    idx +=1
        else:
            for i, card in enumerate(self._cards):
                if card.name == target_card_name:
                    self._cards[idx].hp = sac_card.hp
                    self._cards[idx].max_hp = sac_card.max_hp
                    idx +=1
        
        print(gain_card)
        print()

        # TESTING
        #counter = 1
        #for card in self._cards:
        #    print(f"{counter}. {card.name} COST: {card._cost} HEALTH: {card._hp}/{card._max_hp} POWER: {card._power} SIGIL: {card._sigil}")
        #    counter += 1

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
            idx *= 3
            new_power = card._power + 1
            card._power = new_power

            count = 0
            target_card_name = self._cards[idx].name
            for i, card in enumerate(self._cards):
                if card.name == target_card_name:
                    self._cards[idx]._power = new_power
                    count += 1
                    idx +=1
                    if count == 3:
                        idx -=3
                        break
        else:
            print("You came to visit Aquaman, and he grants you more ... HEALTH")
            print(f"Your max health has been upgraded from {str(card._max_hp)} to {str(card._max_hp + 2)}\n")
            idx *= 3
            new_maxhp = card._max_hp + 2
            new_hp = card.hp + 2
            card._max_hp = new_maxhp
            card._hp = new_hp

            count = 0
            target_card_name = self._cards[idx].name
            for i, card in enumerate(self._cards):
                if card.name == target_card_name:
                    self._cards[idx]._hp = new_hp
                    self._cards[idx]._max_hp = new_maxhp
                    count += 1
                    idx += 1
                    if count == 3:
                        idx -=3
                        break

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

        # TESTING  
        #counter = 1
        #for card in self._cards:
        #    print(f"{counter}. {card.name} HEALTH: {card._hp}/{card._max_hp} POWER: {card._power}")
        #    counter += 1
        
        print()
        pause()
        clear_terminal()
        
    def upgrade_chance(self, idx, random_num, card, chance, congrats_text, failed_text):
        if random_num <= chance:
            print(congrats_text)
            random_num2 = random.randint(1,2)
            if random_num2 == 1:
                new_power = card._power + 1
                card._power = new_power
                count = 0
                target_card_name = self._cards[idx].name
                for i, card in enumerate(self._cards):
                    if card.name == target_card_name:
                        self._cards[idx]._power = new_power
                        count += 1
                        idx +=1
                        if count == 3:
                            break
                print("Your power has been upgraded to " + str(card._power) + "\n")

            else:
                new_maxhp = card._max_hp + 2
                new_hp = card.hp + 2
                card._max_hp = new_maxhp
                card._hp = new_hp
                count = 0
                target_card_name = self._cards[idx].name
                for i, card in enumerate(self._cards):
                    if card.name == target_card_name:
                        self._cards[idx]._hp = new_hp
                        self._cards[idx]._max_hp = new_maxhp
                        count += 1
                        idx +=1
                        if count == 3:
                            break
                print("Your max health has been upgraded to " + str(card._max_hp) + "\n")
            return True
        else:
            count = 0
            target_card_name = self._cards[idx].name
            cards_copy = list(self._cards)
            for i, card in enumerate(cards_copy):
                if card.name == target_card_name:
                    self.remove_card(idx)
                    count += 1
                    if count == 3:
                        break

            print(failed_text)
            return False 

        

