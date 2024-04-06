import random
import tkinter as tk
import tkinter.messagebox as messagebox

class NumberGame:
    def __init__(self, sequence, scores, player):
        self.sequence = sequence
        self.scores = scores
        self.player = player  # 0 for the first player, 1 for the second player

    def copy(self):
        # Create a new game with the same sequence and scores
        return NumberGame(self.sequence[:], self.scores[:], self.player)

    def get_valid_moves(self):
        # A valid move is to pair two numbers or remove an unpaired number
        moves = []
        for i in range(0, len(self.sequence), 2):
            if i + 1 < len(self.sequence):
                moves.append(("pair", i, i + 1))
        if len(self.sequence) % 2 == 1:
            moves.append(("remove", len(self.sequence) - 1))
        return moves

    def make_move(self, move):
        # Update the sequence and scores based on the move
        if move[0] == "pair":
            pair_sum = (self.sequence[move[1]] + self.sequence[move[2]]) % 6
            if pair_sum == 0:
                pair_sum = 6
            self.sequence = (
                self.sequence[: move[1]] + [pair_sum] + self.sequence[move[2] + 1 :]
            )
            self.scores[self.player] += 1
        elif move[0] == "remove":
            self.sequence = self.sequence[: move[1]]
            self.scores[self.player] -= 1
        self.player = 1 - self.player  # Switch to the other player

    def is_game_over(self):
        # The game is over when there's only one number left in the sequence
        return len(self.sequence) == 1

    def evaluate(self):
        # The score of the game state is the difference between the two players' scores
        score_diff = self.scores[0] - self.scores[1]

        # Calculate the sum of pairs that can be formed in the sequence
        pair_sum = sum(
            self.sequence[i] + self.sequence[i + 1]
            for i in range(0, len(self.sequence) - 1, 2)
        )

        # Count the number of unpaired numbers in the sequence
        unpaired_count = len(self.sequence) % 2

        # Calculate a weighted sum of the factors
        h_value = score_diff + pair_sum - unpaired_count

        return h_value

    def minimax(
        self, depth: int = 3, maximizingPlayer: bool = True, debug: bool = False
    ):
        if debug:
            # Print the current state, depth, and score
            print("Depth:", depth)
            print("Sequence:", self.sequence)
            print("Scores:", self.scores)
            print("Evaluation:", self.evaluate())
            print()

        if depth == 0 or self.is_game_over():
            return self.evaluate()

        if maximizingPlayer:
            maxEval = float("-inf")
            for move in self.get_valid_moves():
                new_game = self.copy()  # Create a copy of the game
                new_game.make_move(move)  # Make the move
                eval = new_game.minimax(depth - 1, False, debug)  # Recurse
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float("inf")
            for move in self.get_valid_moves():
                new_game = self.copy()  # Create a copy of the game
                new_game.make_move(move)  # Make the move
                eval = new_game.minimax(depth - 1, True, debug)  # Recurse
                minEval = min(minEval, eval)
            return minEval

    def alpha_beta_pruning(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.is_game_over():
            return self.evaluate()

        if maximizingPlayer:
            maxEval = float("-inf")
            for move in self.get_valid_moves():
                new_game = self.copy()  # Create a copy of the game
                new_game.make_move(move)  # Make the move
                eval = new_game.alpha_beta_pruning(
                    depth - 1, alpha, beta, False
                )  # Recurse
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float("inf")
            for move in self.get_valid_moves():
                new_game = self.copy()  # Create a copy of the game
                new_game.make_move(move)  # Make the move
                eval = new_game.alpha_beta_pruning(
                    depth - 1, alpha, beta, True
                )  # Recurse
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def choose_best_move(self, depth, use_alpha_beta, debug_tree: bool = False):
        best_score = -float("inf")
        best_move = None

        for move in self.get_valid_moves():
            new_game = self.copy()
            new_game.make_move(move)

            if use_alpha_beta:
                score = new_game.alpha_beta_pruning(
                    depth, -float("inf"), float("inf"), False
                )
            else:
                score = new_game.minimax(depth, True, debug_tree)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def get_user_move(self):
        # Create a new window
        window = tk.Tk()

        # Display the current sequence
        sequence_label = tk.Label(
            window, text="Current sequence: " + str(self.sequence)
        )
        sequence_label.pack()

        # Display the valid moves
        valid_moves = self.get_valid_moves()
        tk.Label(window, text="Valid moves:").pack()

        # Create a button for each valid move
        move = tk.StringVar()
        for valid_move in valid_moves:
            tk.Button(
                window,
                text=str(valid_move),
                command=lambda m=valid_move: move.set(str(m)),
            ).pack()

        # Function to validate the move and close the window
        def submit_move():
            if eval(move.get()) in valid_moves:
                window.destroy()
            else:
                messagebox.showerror(
                    "Error", "Invalid move. Please select a valid move."
                )
                # Update the sequence label
                sequence_label.config(text="Current sequence: " + str(self.sequence))

        # Create a button to submit the move
        tk.Button(window, text="Submit Move", command=submit_move).pack()

        # Run the GUI
        window.mainloop()

        # Return the user's move
        return eval(move.get())

    # def get_user_move(self):
    #     # Create a new window
    #     window = tk.Tk()

    #     # Display the current sequence
    #     sequence_label = tk.Label(window, text="Current sequence: " + str(self.sequence))
    #     sequence_label.pack()

    #     # Display the valid moves
    #     valid_moves = self.get_valid_moves()
    #     tk.Label(window, text="Valid moves: " + str(valid_moves)).pack()

    #     # Create an input field for the user's move
    #     move = tk.StringVar()
    #     tk.Label(window, text="Enter your move:").pack()
    #     tk.Entry(window, textvariable=move).pack()

    #     # Function to validate the move and close the window
    #     def submit_move():
    #         user_move = eval(move.get())
    #         if user_move in valid_moves:
    #             window.quit()
    #         else:
    #             messagebox.showerror("Error", "Invalid move. Please enter a valid move.")
    #             # Update the sequence label
    #             sequence_label.config(text="Current sequence: " + str(self.sequence))

    #     # Create a button to submit the move
    #     tk.Button(window, text="Submit Move", command=submit_move).pack()

    #     # Run the GUI
    #     window.mainloop()

    #     # Return the user's move
    #     return eval(move.get())

    # def get_user_move(self):
    #     # Print the valid moves
    #     print("Current sequence : ", self.sequence)
    #     valid_moves = self.get_valid_moves()
    #     print("Valid moves:", valid_moves)

    #     while True:
    #         try:
    #             # Ask the user for their move
    #             move = eval(input("Enter your move: "))
    #             # Check if the move is valid
    #             if move in valid_moves:
    #                 return move
    #             else:
    #                 print("Invalid move. Please enter a valid move.")
    #         except:
    #             print(
    #                 "Invalid input format. Please enter a move in the format ('pair', x, y)."
    #             )


# def create_sequence():

#     while True:
#         try:
#             length = int(input("Izvēlies virknes garumu (15-25): "))
#             # if 15 <= length <= 25:
#             #     break
#             if 5 <= length <= 25:
#                 break
#             else:
#                 print("Garums jābūt intervālā no 15 līdz 25. Lūdzu, mēģiniet vēlreiz.")
#         except ValueError:
#             print("Nepareiza ievade. Lūdzu, ievadiet skaitli.")

#     sequence = [random.randint(1, 6) for _ in range(length)]
#     # print("Sākotnējā virkne: ", sequence)
#     return sequence


# def acquire_inputs():
#     # Ask if tree needs to be shown
#     while True:
#         debug_tree = input("Show tree? (yes/no): ")
#         if debug_tree.lower() in ("yes", "no"):
#             should_draw_tree = debug_tree.lower() == "yes"
#             break
#         else:
#             print("Invalid input. Please enter 'yes' or 'no'.")

#     # Ask how far should the algorithm calculate
#     while True:
#         tree_depth = input("What is tree depth? (numbers 1- b): ")
#         if tree_depth.isdigit() and 1 <= int(tree_depth) <= float("inf"):
#             break
#         else:
#             print("Invalid input. Please enter a number between 1 and b.")

#     # Ask the user who should make the first move
#     while True:
#         first_player = input("Who should make the first move? (user/AI): ")
#         if first_player.lower() in ("user", "ai"):
#             ai_starts = first_player.lower() == "ai"
#             player = 0 if ai_starts else 1
#             break
#         else:
#             print("Invalid input. Please enter 'user' or 'AI'.")

#     # Ask the user which algorithm the AI should use
#     while True:
#         algorithm = input("Which algorithm should the AI use? (minimax/alpha-beta): ")
#         if algorithm.lower() in ("minimax", "alpha-beta"):
#             use_alpha_beta = algorithm.lower() == "alpha-beta"
#             break
#         else:
#             print("Invalid input. Please enter 'minimax' or 'alpha-beta'.")

#     return should_draw_tree, int(tree_depth), player, use_alpha_beta


def acquire_inputs():
    # Create a new window
    window = tk.Tk()

    # Create input fields for each parameter
    debug_tree = tk.BooleanVar()
    tk.Checkbutton(window, text="Show tree?", variable=debug_tree).pack()

    sequence_length = tk.StringVar()
    tk.Label(window, text="Izvēlies virknes garumu (15-25):").pack()
    tk.Entry(window, textvariable=sequence_length).pack()

    tree_depth = tk.StringVar()
    tk.Label(window, text="Tree depth:").pack()
    tk.Entry(window, textvariable=tree_depth).pack()

    first_player = tk.StringVar()
    tk.Label(window, text="First player (user/AI):").pack()
    tk.Entry(window, textvariable=first_player).pack()

    algorithm = tk.StringVar()
    tk.Label(window, text="Algorithm (minimax/alpha-beta):").pack()
    tk.Entry(window, textvariable=algorithm).pack()

    # Function to validate inputs and start the game
    def start_game():
        # Check if sequence length is a number between 15 and 25
        if not sequence_length.get().isdigit() or not (
            15 <= int(sequence_length.get()) <= 25
        ):
            messagebox.showerror(
                "Error",
                "Garums jābūt intervālā no 15 līdz 25. Lūdzu, mēģiniet vēlreiz.",
            )
            return
        # Check if tree depth is a number between 1 and infinity
        if not tree_depth.get().isdigit() or not (1 <= int(tree_depth.get())):
            messagebox.showerror(
                "Error",
                "Invalid tree depth. Please enter a number between 1 and infinity.",
            )
            return

        # Check if first player is 'user' or 'AI'
        if first_player.get().lower() not in ("user", "ai"):
            messagebox.showerror(
                "Error", "Invalid first player. Please enter 'user' or 'AI'."
            )
            return
        # Check if algorithm is 'minimax' or 'alpha-beta'
        if algorithm.get().lower() not in ("minimax", "alpha-beta"):
            messagebox.showerror(
                "Error", "Invalid algorithm. Please enter 'minimax' or 'alpha-beta'."
            )
            return

        # If all inputs are valid, close the window
        # window.quit()
        window.destroy()

    # Create a button to start the game
    tk.Button(window, text="Start Game", command=start_game).pack()

    # Run the GUI
    window.mainloop()

    # Return the input values
    return (
        int(sequence_length.get()),
        debug_tree.get(),
        int(tree_depth.get()),
        first_player.get().lower(),
        algorithm.get().lower(),
    )


def print_text(output_text):

    # Create a new window
    window = tk.Tk()

    # Create a label with large text
    sequence_label = tk.Label(window, text=output_text, font=("Arial", 24))
    sequence_label.pack()

    # Run the GUI
    window.mainloop()


# Use the new acquire_inputs function in your main function
def main():
    # Create the initial game state
    sequence_length, draw_tree, tree_depth, player, use_alpha_beta = acquire_inputs()
    sequence = [random.randint(1, 6) for _ in range(sequence_length)]
    sequence_text = ("Original sequence: {}").format(sequence)
    print_text(sequence_text)
    scores = [0, 0]  # Initial scores
    player_nr = 0 if player == "ai" else 1
    game = NumberGame(
        sequence, scores, player_nr
    )  # Assuming 0 is the AI and 1 is the human

    # Main game loop
    while not game.is_game_over():
        if game.player == 1:
            # User's turn
            move = game.get_user_move()
        else:
            # AI's turn
            move = game.choose_best_move(tree_depth, use_alpha_beta, draw_tree)

        # Make the move
        game.make_move(move)

    # Print the final scores
    print("Final scores:", game.scores)
    if game.scores[0] == game.scores[1]:
        print_text("Draw")
    elif game.scores[0] > game.scores[1]:
        print_text(f"Winner player  AI")
    else:
        print_text(f"Winner player  HUMAN")


if __name__ == "__main__":
    main()
