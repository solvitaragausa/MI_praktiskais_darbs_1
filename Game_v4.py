import ast
import time
import random
import webbrowser

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class NumberGame:
    visited_node_cnt = 0
    max_depth = 0

    def __init__(self, sequence="", scores="", player=""):
        self.sequence = sequence
        self.scores = scores
        self.player = player  # 0 for the first player, 1 for the second player
        self.start_time = 0
        self.end_time = 0
        self.move_times = []

    def copy(self):
        # Create a new game with the same sequence and scores
        return NumberGame(self.sequence[:], self.scores[:], self.player)

    def get_average_move_time(self):
        return (
            round(sum(self.move_times) / len(self.move_times), 4)
            if self.move_times
            else 0
        )

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

        # Count the number of unpaired numbers in the sequence
        unpaired_count = len(self.sequence) % 2

        # Calculate a weighted sum of the factors
        h_value = score_diff + unpaired_count

        return h_value

    def minimax(
        self,
        depth: int = 3,
        maximizing_player: bool = True,
        debug: bool = False,
    ):
        NumberGame.visited_node_cnt += 1
        if debug:
            # Print the current state, depth, and score
            print(" " * 3 * (NumberGame.max_depth - depth), "Depth:", depth)
            print(" " * 3 * (NumberGame.max_depth - depth), "Sequence:", self.sequence)
            print(" " * 3 * (NumberGame.max_depth - depth), "Scores:", self.scores)
            print(" " * 3 * (NumberGame.max_depth - depth), "Evaluation:", self.evaluate())
            print()

        if depth == 0 or self.is_game_over():
            return self.evaluate()

        if maximizing_player:
            max_eval = float("-inf")
            for idx, move in enumerate(self.get_valid_moves()):
                new_game = self.copy()  # Create a copy of the game
                new_game.make_move(move)  # Make the move
                evaluation = new_game.minimax(depth - 1, False, debug)  # Recurse
                max_eval = max(max_eval, evaluation)
            return max_eval
        else:
            min_eval = float("inf")
            for move in self.get_valid_moves():
                new_game = self.copy()  # Create a copy of the game
                new_game.make_move(move)  # Make the move
                evaluation = new_game.minimax(depth - 1, True, debug)  # Recurse
                min_eval = min(min_eval, evaluation)
            return min_eval

    def alpha_beta_pruning(self, depth, alpha, beta, maximizing_player, debug):
        NumberGame.visited_node_cnt += 1
        if debug:
            # Print the current state, depth, and score
            print(" " * 3 * (NumberGame.max_depth - depth), "Depth:", depth)
            print(" " * 3 * (NumberGame.max_depth - depth), "Sequence:", self.sequence)
            print(" " * 3 * (NumberGame.max_depth - depth), "Scores:", self.scores)
            print(
                " " * 3 * (NumberGame.max_depth - depth), "Evaluation:", self.evaluate()
            )
            print()
        if depth == 0 or self.is_game_over():
            return self.evaluate()

        if maximizing_player:
            max_eval = float("-inf")
            for move in self.get_valid_moves():
                new_game = self.copy()  # Create a copy of the game
                new_game.make_move(move)  # Make the move
                evaluation = new_game.alpha_beta_pruning(
                    depth - 1, alpha, beta, False, debug
                )  # Recurse
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in self.get_valid_moves():
                new_game = self.copy()  # Create a copy of the game
                new_game.make_move(move)  # Make the move
                evaluation = new_game.alpha_beta_pruning(
                    depth - 1, alpha, beta, True, debug
                )  # Recurse
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def choose_best_move(self, depth, use_alpha_beta, debug_tree: bool = False):

        self.start_time = time.time()
        best_score = -float("inf")
        best_move = None

        for move in self.get_valid_moves():
            new_game = self.copy()
            new_game.make_move(move)

            if use_alpha_beta:
                score = new_game.alpha_beta_pruning(
                    depth, -float("inf"), float("inf"), False, debug_tree
                )
            else:
                score = new_game.minimax(depth, True, debug_tree)

            if score > best_score:
                best_score = score
                best_move = move
        self.end_time = time.time()
        self.move_times.append(self.end_time - self.start_time)

        return best_move


class GameInputs:
    def __init__(self):
        self.sequence_length = (None,)
        self.draw_tree = False
        self.tree_depth = (None,)
        self.player = (None,)
        self.use_alpha_beta = None

    def print(self):
        return f"{self.sequence_length}, {self.draw_tree}, {self.tree_depth}, {self.player}, {self.use_alpha_beta}"


game_inputs = GameInputs()
game = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game")
def game_get():
    global game
    # Display the current sequence
    if game == None:
        return redirect(url_for("index"))
    sequence_label = game.sequence

    # Display the valid moves
    valid_moves = game.get_valid_moves()

    return render_template(
        "game.html",
        player=game.player,
        valid_moves=valid_moves,
        sequence_label=sequence_label,
    )


@app.route("/final_score")
def final_score():
    global game
    if game == None:
        return redirect(url_for("index"))
    print("Final scores:", game.scores)
    winner = ""
    if game.scores[0] == game.scores[1]:
        winner = "Draw"
    elif game.scores[0] > game.scores[1]:
        winner = "Winner player AI"
    else:
        winner = "Winner player HUMAN"
    return render_template(
        "final_score.html",
        winner=winner,
        scores=game.scores,
        comp_visited_nodes=NumberGame.visited_node_cnt,
        avg_time_taken=game.get_average_move_time(),
    )


@app.route("/restart", methods=["POST"])
def restart():
    global game
    game = None
    return redirect(url_for("index"))


@app.route("/game", methods=["POST"])
def game_post():
    global game
    if "show_tree" in request.form:
        game_inputs.draw_tree = bool(request.form["show_tree"])
    game_inputs.player = str(request.form["player"])
    game_inputs.use_alpha_beta = str(request.form["algorithm"]) == "alpha-beta"
    game_inputs.tree_depth = int(request.form["tree_depth"])
    game_inputs.sequence_length = int(request.form["arr_lenght"])
    print(
        "inputs: ",
        game_inputs.draw_tree,
        game_inputs.player,
        game_inputs.use_alpha_beta,
        game_inputs.tree_depth,
        game_inputs.sequence_length,
    )

    sequence = [random.randint(1, 6) for _ in range(game_inputs.sequence_length)]
    print(("Original sequence: {}").format(sequence))
    scores = [0, 0]  # Initial scores
    player_nr = 0 if game_inputs.player == "ai" else 1
    game = NumberGame(sequence, scores, player_nr)
    NumberGame.max_depth = game_inputs.tree_depth
    return redirect(url_for("game_get"))


@app.route("/move", methods=["POST"])
def move():
    global game
    if game == None:
        return redirect(url_for("index"))
    if game.player == 1:
        # User's turn
        move = ast.literal_eval(request.form["move"])
        print(f"Human move: {move}")

    else:
        # AI's turn
        move = game.choose_best_move(
            game_inputs.tree_depth, game_inputs.use_alpha_beta, game_inputs.draw_tree
        )
        print(f"AI move: {move}")

        # Make the move
    if not game.is_game_over():
        game.make_move(move)
        return redirect(url_for("game_get"))
    else:
        return redirect(url_for("final_score"))


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False, use_debugger=False)
