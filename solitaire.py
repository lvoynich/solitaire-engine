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


# ==========================================
# 3. COMPILATION RUN: Let's test Step 1!
# ==========================================
if __name__ == "__main__":
    my_deck = create_and_shuffle_deck()

    print(f"Total cards created: {len(my_deck)}")
    print("--- Here is a sample of your shuffled deck ---")
    # Print just the first 10 cards to verify it worked
    print(my_deck[:10])
