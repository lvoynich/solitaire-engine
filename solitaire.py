import random

# ==========================================
# 1. THE BLUEPRINT: The Card Class
# ==========================================
class Card:
    def __init__(self, suit, value, color):
        self.suit = suit      # "Hearts", "Diamonds", "Spades", "Clubs"
        self.value = value    # 1 (Ace) through 13 (King)
        self.color = color    # "Red" or "Black"
        self.is_face_up = False
    
    def __repr__(self):
        # Using clear visual suit symbols for the text interface
        suit_symbols = {"Hearts": "♥", "Diamonds": "♦", "Spades": "♠", "Clubs": "♣"}
        symbol = suit_symbols.get(self.suit, self.suit)
        
        display_val = self.value
        if self.value == 1: display_val = "A"
        elif self.value == 11: display_val = "J"
        elif self.value == 12: display_val = "Q"
        elif self.value == 13: display_val = "K"
        
        return f"{symbol}-{display_val}"

    def can_stack_on_me(self, incoming_card):
        if not self.is_face_up:
            return False
        if self.color == incoming_card.color:
            return False
        if incoming_card.value != self.value - 1:
            return False
        return True


# ==========================================
# 2. THE FACTORY: Deck Generation
# ==========================================
def create_and_shuffle_deck():
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    deck = []
    
    for suit in suits:
        color = "Red" if suit in ["Hearts", "Diamonds"] else "Black"
        for value in range(1, 14):
            deck.append(Card(suit, value, color))
            
    random.shuffle(deck)
    return deck


# ==========================================
# 3. THE SETUP: Dealing the Board
# ==========================================
def setup_solitaire_board(shuffled_deck):
    tableau = [[] for _ in range(7)]
    for i in range(7):
        for j in range(i, 7):
            card = shuffled_deck.pop(0)
            if j == i:
                card.is_face_up = True
            tableau[j].append(card)
            
    draw_pile = shuffled_deck
    return tableau, draw_pile


# ==========================================
# 4. THE LAYOUT: Unified Terminal Interface
# ==========================================
def display_board(tableau, draw_pile, waste_pile, foundations):
    print("\n" + "=" * 65)
    
    # Format the 4 foundations for display (showing the top card or empty brackets)
    found_strings = []
    for f_pile in foundations:
        if f_pile:
            found_strings.append(f"[{f_pile[-1]}]") # Show top card
        else:
            found_strings.append("[ . ]") # Show empty placeholder
            
    top_waste = waste_pile[-1] if waste_pile else "Empty"
    
    # The ultimate terminal status dashboard
    print(f"  STOCK: [{len(draw_pile)} Hidden]  |  WASTE: [{top_waste}]")
    print(f"  FOUNDATIONS:  {found_strings[0]}   {found_strings[1]}   {found_strings[2]}   {found_strings[3]}")
    print("=" * 65)
    print("  Col 1   Col 2   Col 3   Col 4   Col 5   Col 6   Col 7")
    print("  -----------------------------------------------------")
    
    max_rows = max(len(column) for column in tableau) if tableau else 0
    if max_rows == 0:
        print("  (Empty Table)")
        
    for row_index in range(max_rows):
        row_string = "    "
        for col in tableau:
            if row_index < len(col):
                card = col[row_index]
                if card.is_face_up:
                    row_string += f"{str(card):<5}   "
                else:
                    row_string += "[###]   "
            else:
                row_string += "        "
        print(row_string)
    print("=" * 65 + "\n")



# ==========================================
# 5. THE ACTIONS: Movement Core Logic
# ==========================================
def move_stack(tableau, from_col_idx, to_col_idx):
    from_idx = from_col_idx - 1
    to_idx = to_col_idx - 1
    
    if from_idx < 0 or from_idx > 6 or to_idx < 0 or to_idx > 6:
        print("❌ Error: Invalid column number! Choose 1 through 7.")
        return False
        
    if not tableau[from_idx]:
        print("❌ Error: The source column has no cards to move!")
        return False
        
    # Find the deepest face-up card in the source column to slice the stack
    first_face_up_idx = -1
    for idx, card in enumerate(tableau[from_idx]):
        if card.is_face_up:
            first_face_up_idx = idx
            break
            
    if first_face_up_idx == -1:
        print("❌ Error: No face-up cards found to move!")
        return False
        
    moving_stack = tableau[from_idx][first_face_up_idx:]
    deepest_moving_card = moving_stack[0]
    
    # Empty column validation rule (Only Kings)
    if not tableau[to_idx]:
        if deepest_moving_card.value == 13:
            tableau[from_idx] = tableau[from_idx][:first_face_up_idx]
            tableau[to_idx].extend(moving_stack)
            return True
        else:
            print("❌ Error: Only a King can open an empty column!")
            return False
            
    # Active column validation rule
    target_card = tableau[to_idx][-1]
    if target_card.can_stack_on_me(deepest_moving_card):
        tableau[from_idx] = tableau[from_idx][:first_face_up_idx]
        tableau[to_idx].extend(moving_stack)
        return True
    else:
        print(f"❌ Move Rejected! Cannot place stack starting with {deepest_moving_card} on {target_card}.")
        return False

def move_to_foundation(card, foundation_pile):
    # Rule 1: If the foundation pile is empty, it MUST be an Ace (value 1)
    if not foundation_pile:
        if card.value == 1:
            return True
        else:
            print("❌ Error: Foundations must start with an Ace!")
            return False
            
    # Rule 2: If it's not empty, it must match the suit and be exactly 1 value higher
    top_card = foundation_pile[-1]
    if card.suit == top_card.suit and card.value == top_card.value + 1:
        return True
    else:
        print(f"❌ Move Rejected! You cannot place a {card} on {top_card}.")
        return False

# ==========================================
# 6. THE ENGINE: Continuous Game Loop
# ==========================================
def play_game():
    deck = create_and_shuffle_deck()
    tableau, draw_pile = setup_solitaire_board(deck)
    waste_pile = []
    foundations = [[] for _ in range(4)]  # <--- Add this! Tracks 4 foundation lists
    
    print("♠️ ♥️ Welcome to Terminal Solitaire Engine ♦️ ♣️")
    
    while True:
        display_board(tableau, draw_pile, waste_pile,foundations)
        command = input("Enter command ('m' to move, 'd' to draw, 'q' to quit): ").strip().lower()
        
        if command == 'q':
            print("Thanks for playing! Goodbye.")
            break
            
        elif command == 'd':
            if draw_pile:
                card = draw_pile.pop(0)
                card.is_face_up = True
                waste_pile.append(card)
            else:
                if waste_pile:
                    draw_pile = list(reversed(waste_pile))
                    for card in draw_pile:
                        card.is_face_up = False
                    waste_pile = []
                    print("🔄 Recycled waste pile back into draw pile.")
                else:
                    print("❌ Out of cards completely!")
                
        elif command == 'm':
            choice = input("Move from (t)ableau columns or (w)aste pile? ").strip().lower()
            
            if choice == 'w':
                if not waste_pile:
                    print("❌ Waste pile is empty!")
                    continue
                try:
                    dst = int(input("Destination Column (1-7): "))
                    to_idx = dst - 1
                    moving_card = waste_pile[-1]
                    
                    if not tableau[to_idx]:
                        if moving_card.value == 13:
                            waste_pile.pop()
                            tableau[to_idx].append(moving_card)
                        else:
                            print("❌ Only a King can open an empty column!")
                    else:
                        target_card = tableau[to_idx][-1]
                        if target_card.can_stack_on_me(moving_card):
                            waste_pile.pop()
                            tableau[to_idx].append(moving_card)
                        else:
                            print(f"❌ Cannot place {moving_card} on {target_card}.")
                except ValueError:
                    print("❌ Invalid input.")
                    
            elif choice == 't':
                try:
                    src = int(input("Source Column (1-7): "))
                    dst = int(input("Destination Column (1-7): "))
                    
                    if src == dst:
                        print("❌ Source and destination cannot be the same.")
                        continue
                        
                    if move_stack(tableau, src, dst):
                        # Auto-flip the newly exposed card on the source column
                        if tableau[src - 1] and not tableau[src - 1][-1].is_face_up:
                            tableau[src - 1][-1].is_face_up = True
                except ValueError:
                    print("❌ Please enter valid numerical inputs.")
        else:
            print("❌ Unknown command.")


if __name__ == "__main__":
    play_game()
