import tkinter as tk
from tkinter import messagebox
import random

# Function to compare card values
def compare_cards(card1, card2):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return values[card1[0]] - values[card2[0]]

# Function to conduct an auction round
def auction_round(player_card):
    global player_score
    global banker_deck
    
    banker_card = banker_deck.pop()
    comp_card = random.choice([player_card, banker_card])
    
    result_label.config(text=f"Banker's Card: {banker_card}\nYour Card: {player_card}\nComputer's Card: {comp_card}\n")
    
    # Determine the highest bid
    highest_bid = max(player_card, comp_card, key=lambda x: compare_cards(x, banker_card))
    
    banker_card_value = banker_card[:-1]
    if banker_card_value in ['T', 'J', 'Q', 'K', 'A']:
        banker_card_value = 10 if banker_card_value == 'T' else 11  # Assign values for T, J, Q, K, A
    
    if highest_bid == player_card:
        messagebox.showinfo("Result", "Congratulations! You win the auction.")
        score = int(banker_card_value)
        if player_score + score < 0:
            score = -player_score  # Limit the deduction to reach 0
        player_score += score
    elif highest_bid == comp_card:
        messagebox.showinfo("Result", "Computer wins the auction.")
    else:
        messagebox.showinfo("Result", "It's a tie!")
    update_score_label()

    if not banker_deck:
        end_game()

# Function to handle button click
def bid():
    global turn_count
    if turn_count < 13:
        card_value = card_entry.get().upper()
        if card_value not in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
            messagebox.showerror("Error", "Invalid card entry. Please enter a valid card value (2-9,T,J,Q,K,A).")
            return

        player_card = card_value + 'C' # Assuming player has a club suit
        
        auction_round(player_card)
        turn_count += 1

# Function to end the game and declare the winner
def end_game():
    global player_score
    if player_score > 0:
        messagebox.showinfo("Game Over", f"Congratulations! You win with a score of {player_score}.")
    elif player_score < 0:
        messagebox.showinfo("Game Over", f"Computer wins with a score of {-player_score}.")
    else:
        messagebox.showinfo("Game Over", "It's a tie!")
    root.destroy()

# Function to update score label
def update_score_label():
    global player_score
    score_label.config(text=f"Your Score: {player_score}")

# Main function
def main():
    global banker_deck
    global player_score
    global turn_count
    
    turn_count = 0
    player_score = 0
    banker_deck = ['2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']
    random.shuffle(banker_deck)
    
    root.protocol("WM_DELETE_WINDOW", end_game)  # Handle window close event
    root.mainloop()

# GUI setup
root = tk.Tk()
root.title("Diamond Auction Game")

instruction_label = tk.Label(root, text="Enter one card value (2-9,T,J,Q,K,A):")
instruction_label.pack()

card_entry = tk.Entry(root)
card_entry.pack()

bid_button = tk.Button(root, text="Bid", command=bid)
bid_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

score_label = tk.Label(root, text="Your Score: 0")
score_label.pack()

if __name__ == "__main__":
    main()
