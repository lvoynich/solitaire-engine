import random


# ==========================================
# 1. THE BLUEPRINT: What is a single Card?
# ==========================================
class Card:
    def __init__(self, suit, value, color):
        self.suit = suit  # "Hearts", "Diamonds", "Spades", "Clubs"
        self.value = value  # 1 (Ace) through 13 (King)
        self.color = color  # "Red" or "Black"
        self.is_face_up = False  # By default, cards start hidden in Solitaire

    # This special function tells Python exactly how to PRINT the card as text
    def __repr__(self):
        # We will use simple abbreviations: e.g., "H-7" for 7 of Hearts
        suit_letter = self.suit[0]  # Takes just the first letter (H, D, S, C)

        # Make readable shortcuts for Ace, Jack, Queen, King
        display_val = self.value
        if self.value == 1:
            display_val = "A"
        elif self.value == 11:
            display_val = "J"
        elif self.value == 12:
            display_val = "Q"
        elif self.value == 13:
            display_val = "K"

        return f"{suit_letter}-{display_val}"


# ==========================================
# 2. THE FACTORY: Stamping out 52 Cards
# ==========================================
def create_and_shuffle_deck():
    # Setup our layout variations
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]

    deck = []  # This list will hold our 52 card objects

    # Double Loop: For every suit, create values 1 through 13
    for suit in suits:
        # Determine color based on the suit
        if suit in ["Hearts", "Diamonds"]:
            color = "Red"
        else:
            color = "Black"

        for value in range(1, 14):  # Generates numbers 1 to 13
            # 1. Use the blueprint to stamp out a brand new card object
            new_card = Card(suit, value, color)
            # 2. Add that card object into our deck list
            deck.append(new_card)

    # Mix them up using Python's built-in random library
    random.shuffle(deck)

    return deck

def setup_solitaire_board(shuffled_deck):
    # Create a list containing 7 empty lists (one for each column)
    tableau = [[] for _ in range(7)]
    
    # Nested loop to deal cards incrementally
    for i in range(7):
        for j in range(i, 7):
            # Take the top card off our shuffled deck list
            card = shuffled_deck.pop(0)
            
            # If it's the very last card being added to this specific column, flip it face up
            if j == i:
                card.is_face_up = True
                
            # Place the card into the correct column list
            tableau[j].append(card)
            
    # The remaining cards left in the deck become our Draw Pile (Stock)
    draw_pile = shuffled_deck
    
    return tableau, draw_pile

# --- UPDATE YOUR MAIN TEST LOOP AT THE BOTTOM ---
if __name__ == "__main__":
    deck = create_and_shuffle_deck()
    
    # Run the setup function
    columns, remainder_pile = setup_solitaire_board(deck)
    
    print(f"Board initialized successfully!")
    print(f"Cards left in draw pile: {len(remainder_pile)}")
    print(f"Number of cards in Column 7: {len(columns[6])}")
    print(f"Is the top card of Column 7 face up? {columns[6][-1].is_face_up}")

