from board import Board
from constants import PLAYER1_PIECE_COLOR, PLAYER2_PIECE_COLOR
from game import Game
import board_configs
import random
import unittest


# TO DO: Implement this function. The four lines currently implemented including the return are in place to make the
# gameplay visualization work. Replace all of it with your own code for the function.
def minimax_alpha_beta(board, depth, alpha, beta, max_player, game, eval_params=None):
    """
        Executes the Minimax algorithm with Alpha-Beta pruning to determine the optimal move in a two-player game.

        Args:
            board (Board): The current board state
            depth (int): The maximum depth to go to on the search tree
            alpha (float): The best value that the maximizing player can guarantee
            beta (float): The best value that the minimizing player can guarantee
            max_player (bool): True if the current player is the maximizing player (AI), False if minimizing (human)
            game (Game): The game instance
            eval_params (tuple, optional): A tuple of weights for evaluating the board state.

        Returns:
            tuple: A tuple (evaluation, best_move) where:
                - score (float): The score for the best move at this depth
                - best_move (Board): The board state after the best move
        """

    score = 1
    moves = game.generate_all_moves(board, PLAYER2_PIECE_COLOR)
    best_move = random.choice(moves)

    return score, best_move

def evaluate(board, game, pieces_weight=1.0, kings_weight=1.0, moves_weight=0.0, opportunities_weight=0.0, king_hopefuls_weight=0.0):
    """
    Evaluates the given board and returns a score based on a weighted combination of these metrics:

        1. The difference in the number of own pieces vs. opponent pieces
        2. The difference in the number of own kings vs. opponent kings
        3. The difference in the number of own king hopefuls vs. opponent king hopefuls (See Notes below)
        4. The difference in the number of capture opportunities for the player vs. the opponent
        5. The difference in the number of moves available for the player vs. the opponent.

    The AI player (using Minimax) is assumed to be Player 2.

    Args:
        board (Board): The current state of the game board
        game (Game): The game instance
        pieces_weight (float): Weight for the difference in piece count
        kings_weight (float): Weight for the difference in king count
        moves_weight (float): Weight for the difference in available moves
        opportunities_weight (float): Weight for the difference in capture opportunities
        king_hopefuls_weight (float): Weight for the difference in king hopefuls.

    Returns:
        float: A score representing the board's goodness for Player 2

    Notes:
        - King hopefuls have to do with pieces that can become king in the next move and are counted not just as the
        number of such pieces but as how many such king promotions can occur. So, if a piece can become king in its
        next move in two ways, then the piece is counted twice.
    """

    p1_num_pieces, p1_num_kings, p1_num_moves, p1_num_opportunities, p1_num_king_hopefuls = counts(board, game, PLAYER1_PIECE_COLOR)
    p2_num_pieces, p2_num_kings, p2_num_moves, p2_num_opportunities, p2_num_king_hopefuls = counts(board, game, PLAYER2_PIECE_COLOR)

    pieces_diff = p2_num_pieces - p1_num_pieces
    kings_diff = p2_num_kings - p1_num_kings
    moves_diff = p2_num_moves - p1_num_moves
    opportunities_diff = p2_num_opportunities - p1_num_opportunities
    king_hopefuls_diff = p2_num_king_hopefuls - p1_num_king_hopefuls

    score = (pieces_diff * pieces_weight +
             kings_diff * kings_weight +
             moves_diff * moves_weight +
             opportunities_diff * opportunities_weight +
             king_hopefuls_diff * king_hopefuls_weight)

    return score

# TO DO: Implement this function.
def counts(board, game, color):
    """
    Counts various metrics for pieces of a given color on the board.

    Args:
        board (Board): The current board state
        game (Game): The game instance
        color (tuple): The RGB color of the pieces to evaluate, formatted as a tuple (e.g., (255, 240, 125)).

    Returns:
        A tuple containing:
        - num_pieces (int): The number of pieces of the specified color on the board
        - num_kings (int): The number of kings of the specified color
        - num_moves (int): The total number of available single-hop moves for all pieces of the specified color
        - num_opportunities (int): The total number of capture opportunities across all pieces of the specified color
        - num_king_hopefuls (int): The total number of moves that lead to king promotions for the specified color.
    """

    pass

def compare_boards(board1, board2):
    """
    Compares two board objects to determine if they are identical in piece layout, piece color, and piece status (king or non-king).

    Args:
        board1 (Board): The first board object to compare.
        board2 (Board): The second board object to compare.

    Returns:
        bool: True if the boards are identical in terms of piece layout, piece color, and king status at each position; False otherwise

    The function checks each position (row, col) on an 8x8 board grid:
    - If both positions are empty (denoted by 0), it continues to the next position.
    - If only one position is empty, it returns False.
    - If both positions contain a piece, it checks that the pieces have the same color and king status. If any discrepancy is found, it returns False.

    Assumptions:
        - `board1` and `board2` are expected to have a `get_piece(row, col)` method that  returns either a piece object
        (with `color` and `king` attributes) or 0 if the position is empty.
    """

    if not isinstance(board1, Board) or not isinstance(board2, Board):
        return False

    for row in range(8):
        for col in range(8):
            piece1 = board1.get_piece(row, col)
            piece2 = board2.get_piece(row, col)

            if piece1 == 0 and piece2 == 0:
                continue

            if (piece1 == 0) != (piece2 == 0):
                return False

            if piece1.color != piece2.color or piece1.king != piece2.king:
                return False

    return True


class AiTest(unittest.TestCase):

    def test_counts_with_boards(self):
        for b in range(0, 6):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            game = Game()
            colors = [PLAYER1_PIECE_COLOR, PLAYER2_PIECE_COLOR]

            piece_counts = [[7, 13], [7, 12], [6, 12], [1, 11], [1, 10], [2, 12]]
            king_counts  = [[2, 2], [2, 3], [3, 2], [1, 0], [1, 0], [1, 0]]
            move_counts  = [[8, 17], [10, 14], [7, 11], [0, 12], [1, 12], [0, 12]]
            opportunity_counts  = [[3, 4], [4, 3], [1, 3], [0, 0], [1, 0], [0, 1]]
            king_hopeful_counts  = [[0, 0], [1, 0], [1, 0], [0, 2], [0, 2], [0, 2]]

            for c in range(2):
                color = colors[c]
                num_pieces, num_kings, num_moves, num_opportunities, num_king_hopefuls = counts(board, game, color)

                self.assertEqual(num_pieces, piece_counts[b][c])
                self.assertEqual(num_kings, king_counts[b][c])
                self.assertEqual(num_moves, move_counts[b][c])
                self.assertEqual(num_opportunities, opportunity_counts[b][c])
                self.assertEqual(num_king_hopefuls, king_hopeful_counts[b][c])

    def test_evaluate_1(self):

        expected_scores = [6.0, 6.0, 5.0, 9.0, 8.0, 9.0, 8.0, 10.0, 10.0, 4.0, 3.0, 4.0]

        game = Game()
        for b in range(0, 12):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            score = evaluate(board, game)
            self.assertEqual(score, expected_scores[b])

    def test_evaluate_2(self):

        expected_scores = [16.0, 8.0, 10.0, 23.0, 20.0, 24.0, 22.0, 25.0, 23.0, 9.0, 10.0, 13.0]

        game = Game()
        for b in range(0, 12):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            score = evaluate(board, game, moves_weight=1.0, opportunities_weight=1.0, king_hopefuls_weight=1.0)
            self.assertEqual(score, expected_scores[b])

    def test_evaluate_3(self):

        expected_scores = [11.0, 7.25, 7.75, 15.5, 13.5, 16.0, 14.5, 16.75, 16.0, 6.25, 6.25, 8.25]

        game = Game()
        for b in range(0, 12):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            score = evaluate(board, game, pieces_weight=1.0, kings_weight=1.0, moves_weight=0.5, opportunities_weight=0.5, king_hopefuls_weight=0.25)
            self.assertEqual(score, expected_scores[b])

    def test_evaluate_4(self):

        expected_scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        game = Game()
        for b in range(0, 12):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            score = evaluate(board, game, pieces_weight=0.0, kings_weight=0.0, moves_weight=0.0, opportunities_weight=0.0, king_hopefuls_weight=0.0)
            self.assertEqual(score, expected_scores[b])

    def test_minimax_alpha_beta_1(self):

        game = Game()
        board = Board()

        value, new_board = minimax_alpha_beta(board, 1, float('-inf'), float('inf'), True, game)

        true_board = Board(board_configs.board_config13)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_2(self):

        game = Game()
        board = Board()

        value, new_board = minimax_alpha_beta(board, 2, float('-inf'), float('inf'), True, game)

        true_board = Board(board_configs.board_config14)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_3(self):

        game = Game()
        board = Board()

        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game)

        true_board = Board(board_configs.board_config15)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_4(self):

        game = Game()
        board = Board()

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 1, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config16)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_5(self):

        game = Game()
        board = Board()

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 2, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config17)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_6(self):

        game = Game()
        board = Board()

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config18)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_7(self):

        game = Game()
        board = Board(board_configs.board_config1)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config19)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_8(self):

        game = Game()
        board = Board(board_configs.board_config2)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 4, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config20)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_9(self):

        game = Game()
        board = Board(board_configs.board_config3)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config21)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_10(self):

        game = Game()
        board = Board(board_configs.board_config4)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config22)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_11(self):

        game = Game()
        board = Board(board_configs.board_config6)

        eval_params = (0.0, 1.0, 1.0, 0.0, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config23)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_12(self):

        game = Game()
        board = Board(board_configs.board_config7)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 2, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config24)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_13(self):

        game = Game()
        board = Board(board_configs.board_config9)

        eval_params = (1.0, 1.0, 0.0, 0.0, 1.0)
        value, new_board = minimax_alpha_beta(board, 4, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config25)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_14(self):

        game = Game()
        board = Board(board_configs.board_config10)

        eval_params = (0.0, 0.0, 0.0, 0.0, 0.0)
        value, new_board = minimax_alpha_beta(board, 4, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config26)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_15(self):

        game = Game()
        board = Board(board_configs.board_config11)

        eval_params = (1.0, 1.0, 1.5, 1.5, 1.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config27)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_16(self):

        game = Game()
        board = Board(board_configs.board_config12)

        eval_params = (1.0, 1.0, 1.0, 1.0, 1.0)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config28)

        self.assertTrue(compare_boards(new_board, true_board))
