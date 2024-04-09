import pytest
import random
from Game_v4 import NumberGame


@pytest.fixture
def game():
    sequence = [random.randint(1, 6) for _ in range(8)]
    scores = [0, 0]  # Initial scores
    return NumberGame(sequence, scores, 0)


def test_number_game(game: NumberGame):
    # Print the initial state
    print("Initial state:", game.sequence, game.scores)

    # Get the valid moves
    moves = game.get_valid_moves()
    print("Valid moves:", moves)

    # Make a move and print the new state
    if moves:
        game.make_move(moves[0])
        print("State after move:", game.sequence, game.scores)

    # Check if the game is over
    print("Is game over?", game.is_game_over())

    # Evaluate the game state
    print("Evaluation:", game.evaluate(), "\n")


def test_get_valid_moves():
    game = NumberGame([1, 2, 3, 4, 5], [0, 0], 0)
    assert game.get_valid_moves() == [("pair", 0, 1), ("pair", 2, 3), ("remove", 4)]


def test_make_move():
    game = NumberGame([1, 5, 2, 1, 3, 4, 6, 2, 1, 4, 3], [0, 0], 0)
    assert game.get_valid_moves() == [
        ("pair", 0, 1),
        ("pair", 2, 3),
        ("pair", 4, 5),
        ("pair", 6, 7),
        ("pair", 8, 9),
        ("remove", 10),
    ]
    game.make_move(("remove", 10))
    assert game.sequence == [1, 5, 2, 1, 3, 4, 6, 2, 1, 4]
    assert game.scores == [-1, 0]

    game2 = NumberGame([1, 5, 2, 1, 3, 4, 6, 2, 1, 4, 3], [0, 0], 0)
    assert game2.get_valid_moves() == [
        ("pair", 0, 1),
        ("pair", 2, 3),
        ("pair", 4, 5),
        ("pair", 6, 7),
        ("pair", 8, 9),
        ("remove", 10),
    ]
    game2.make_move(("pair", 4, 5))
    assert game2.sequence == [1, 5, 2, 1, 1, 6, 2, 1, 4, 3]
    assert game2.scores == [1, 0]


def test_is_game_over():
    game = NumberGame([1], [0, 0], 0)
    assert game.is_game_over() == True


def test_evaluate():
    game = NumberGame([1], [3, 2], 0)
    assert game.evaluate() == 2


def test_minimax():
    # Run the Minimax algorithm
    game = NumberGame([5, 2, 3, 4, 5, 1], [0, 0], 0)
    best_score = game.minimax(5, True, True)  # Adjust the depth as needed
    print("Best score:", best_score)
    assert game.minimax(3, True) >= -float("inf")
    assert game.minimax(3, False) <= float("inf")


def test_alpha_beta_pruning():
    # Run the Alpha-Beta Pruning algorithm
    game = NumberGame([5, 2, 3, 4, 5, 1], [0, 0], 0)
    best_score = game.alpha_beta_pruning(
        5, -float("inf"), float("inf"), True, True
    )  # Adjust the depth as needed
    print("Best score:", best_score)
    assert game.alpha_beta_pruning(
        3, -float("inf"), float("inf"), True, True
    ) >= -float("inf")
    assert game.alpha_beta_pruning(
        3, -float("inf"), float("inf"), False, True
    ) <= float("inf")


def test_choose_best_move():
    # Create a game with a known best move
    game = NumberGame([5, 2, 1, 5, 2], [0, 0], 0)

    # Test the function with the Minimax algorithm
    best_move_minimax = game.choose_best_move(3, False, True)
    print("Best move (Minimax):", best_move_minimax)

    # Test the function with the Alpha-Beta pruning algorithm
    best_move_alpha_beta = game.choose_best_move(3, True, True)
    print("Best move (Alpha-Beta):", best_move_alpha_beta)

    # Check that the function returns a valid move
    assert best_move_minimax in game.get_valid_moves()
    assert best_move_alpha_beta in game.get_valid_moves()
