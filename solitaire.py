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
        # Human-readable visual representation
        suit_symbols = {"Hearts": "♥", "Diamonds": "♦", "Spades": "♠", "Clubs": "♣"}
        symbol = suit_symbols.get(self.suit, self.suit[0])
        
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
# 4. THE LAYOUT: Terminal Interface
# ==========================================
def display_board(tableau, draw_pile):
    print("\n" + "=" * 55)
    print(f"  DRAW PILE: [{len(draw_pile)} cards left]  |  Type 'd' to draw a card")
    print("=" * 55)
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
                    row_string += f"{str(card):<5}   "  # Clean spacing alignment
                else:
                    row_string += "[###]   "
            else:
                row_string += "        "
        print(row_string)
    print("=" * 55 + "\n")


# ==========================================
# 5. THE ACTIONS: Movement Core Logic
# ==========================================
def move_card(tableau, from_col_idx, to_col_idx):
    from_idx = from_col_idx - 1
    to_idx = to_col_idx - 1
    
    if from_idx < 0 or from_idx > 6 or to_idx < 0 or to_idx > 6:
        print("❌ Error: Invalid column number! Choose 1 through 7.")
        return False
        
    if not tableau[from_idx]:
        print("❌ Error: The source column has no cards to move!")
        return False
        
    # =======================================================
    # ADVANCED STACK MOVEMENT LOGIC
    # =======================================================
    
    # 1. Find the first (deepest) face-up card in the source column
    first_face_up_idx = -1
    for idx, card in enumerate(tableau[from_idx]):
        if card.is_face_up:
            first_face_up_idx = idx
            break
            
    if first_face_up_idx == -1:
        print("❌ Error: No face-up cards found to move!")
        return False
        
    # 2. Slice the entire stack of face-up cards from that point to the end
    moving_stack = tableau[from_idx][first_face_up_idx:]
    deepest_moving_card = moving_stack[0] # The card that will actually land on the new pile
    
    # Case A: Moving onto an empty destination column
    if not tableau[to_idx]:
        if deepest_moving_card.value == 13:  # Only Kings can start empty columns
            # Remove the stack from the source column
            tableau[from_idx] = tableau[from_idx][:first_face_up_idx]
            # Extend the destination column with the entire moving stack
            tableau[to_idx].extend(moving_stack)
            return True
        else:
            print("❌ Error: Only a King can open an empty column!")
            return False
            
    # Case B: Moving onto a column that already has cards
    target_card = tableau[to_idx][-1]
    
    # Check the rules using the deepest card in our moving stack
    if target_card.can_stack_on_me(deepest_moving_card):
        # Slice off the stack from the old column
        tableau[from_idx] = tableau[from_idx][:first_face_up_idx]
        # Append the entire stack to the new column
        tableau[to_idx].extend(moving_stack)
        return True
    else:
        print(f"❌ Move Rejected! You cannot place the stack starting with {deepest_moving_card} on {target_card}.")
        return False


# ==========================================
# 6. THE ENGINE: Continuous Game Loop
# ==========================================
def play_game():
    deck = create_and_shuffle_deck()
    tableau, draw_pile = setup_solitaire_board(deck)
    
    print("♠️ ♥️ Welcome to Terminal Solitaire Engine ♦️ ♣️")
    
    while True:
        display_board(tableau, draw_pile)
        
        # Get input command from the user
        command = input("Enter command ('m' to move, 'd' to draw, 'q' to quit): ").strip().lower()
        
        if command == 'q':
            print("Thanks for playing! Goodbye.")
            break
            
        elif command == 'd':
            if draw_pile:
                # Cycle a card from draw pile to column 1 as an easy simulation rule
                card = draw_pile.pop(0)
                card.is_face_up = True
                # Find the shortest column to drop the drawn card into
                shortest_col = min(tableau, key=len)
                shortest_col.append(card)
                print(f"🃏 Dealt {card} onto the board.")
            else:
                print("❌ Out of cards in the draw pile!")
                
        elif command == 'm':
            try:
                src = int(input("Source Column (1-7): "))
                dst = int(input("Destination Column (1-7): "))
                
                if move_card(tableau, src, dst):
                    print("✅ Move executed.")
                    
                    # SYSTEM TRIGGER: Auto-flip exposed cards face up
                    if tableau[src - 1] and not tableau[src - 1][-1].is_face_up:
                        tableau[src - 1][-1].is_face_up = True
                        print(f"🔄 Flipped top card of Column {src} face up!")
            except ValueError:
                print("❌ Please enter valid numerical inputs.")
        else:
            print("❌ Unknown command.")


if __name__ == "__main__":
    play_game()
