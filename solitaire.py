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

    # =======================================================
    # STEP 4: THE RULE METHOD
    # This allows a card to look at an incoming card and say True or False
    # =======================================================
    def can_stack_on_me(self, incoming_card):
        # Rule A: The target card on the board MUST be face up to build on it
        if not self.is_face_up:
            return False

        # Rule B: Colors must be completely opposite
        if self.color == incoming_card.color:
            return False

        # Rule C: Incoming card must be exactly one value lower
        if incoming_card.value != self.value - 1:
            return False

        # If it survives all checks, the move is perfectly legal!
        return True


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

def display_board(tableau, draw_pile):
    print("\n" + "=" * 40)
    print(f"DRAW PILE: [{len(draw_pile)} cards remaining]")
    print("=" * 40)
    
    # 1. Print the column headers (1 through 7)
    print("  Col 1   Col 2   Col 3   Col 4   Col 5   Col 6   Col 7")
    print("  -----------------------------------------------------")
    
    # 2. Find the tallest column height so we know how many horizontal rows to print
    max_rows = max(len(column) for column in tableau)
    
    # 3. Loop row by row
    for row_index in range(max_rows):
        row_string = "    "
        
        for col in tableau:
            # If this column has a card at this row index, print it
            if row_index < len(col):
                card = col[row_index]
                
                # Check our Class attribute: is it face up?
                if card.is_face_up:
                    row_string += f"{card}    "  # Prints the shortcut (e.g. "S-K")
                else:
                    row_string += "[###]   "  # Hides face-down cards like a real game!
            else:
                # If the column is shorter than this row index, print empty space
                row_string += "        "
                
        print(row_string)
    print("=" * 40 + "\n")

# --- UPDATE YOUR MAIN TEST LOOP TO VISUALLY PRINT IT ---
if __name__ == "__main__":
    # Test our rule validation logic manually
    base_card = Card("Spades", 8, "Black")
    base_card.is_face_up = True # Must flip it up to test stacking
    
    valid_card = Card("Hearts", 7, "Red")
    invalid_card = Card("Clubs", 7, "Black") # Wrong color!
    
    print("--- Testing Solitaire Rule Framework ---")
    print(f"Can Red 7 stack on Black 8? {base_card.can_stack_on_me(valid_card)}")   # Should print: True
    print(f"Can Black 7 stack on Black 8? {base_card.can_stack_on_me(invalid_card)}") # Should print: False
