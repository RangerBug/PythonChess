import random
import time

piece_score = {"K": 0, "Q": 100, "R": 50, "B": 30, "N": 30, "P": 10}

knight_scores = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]

queen_scores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 3, 1, 1, 3, 3, 2],
                [1, 2, 1, 1, 1, 1, 2, 1],
                [1, 2, 1, 1, 1, 1, 2, 1],
                [2, 3, 3, 1, 1, 3, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

rook_scores = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]

bishop_scores = [[4, 3, 2, 1, 1, 2, 3, 4],
                 [3, 4, 3, 2, 2, 3, 4, 3],
                 [2, 3, 4, 3, 3, 4, 3, 2],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [2, 3, 4, 3, 3, 4, 3, 2],
                 [3, 4, 3, 2, 2, 3, 4, 3],
                 [4, 3, 2, 1, 1, 2, 3, 4]]

white_pawn_scores_w = [[10, 10, 10, 10, 10, 10, 10, 10],
                       [8, 8, 8, 8, 8, 8, 8, 8],
                       [5, 6, 6, 7, 7, 6, 6, 5],
                       [2, 3, 3, 5, 5, 3, 3, 2],
                       [1, 2, 3, 5, 5, 3, 2, 1],
                       [1, 1, 2, 2, 2, 2, 1, 1],
                       [1, 1, 1, 0, 0, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0]]

black_pawn_scores_w = [[0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 0, 0, 1, 1, 1],
                       [1, 1, 2, 2, 2, 2, 1, 1],
                       [1, 2, 3, 5, 5, 3, 2, 1],
                       [2, 3, 3, 5, 5, 3, 3, 2],
                       [5, 6, 6, 7, 7, 6, 6, 5],
                       [8, 8, 8, 8, 8, 8, 8, 8],
                       [10, 10, 10, 10, 10, 10, 10, 10]]

black_pawn_scores_b = [[0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 0, 0, 1, 1, 1],
                       [1, 1, 2, 2, 2, 2, 1, 1],
                       [1, 2, 3, 5, 5, 3, 2, 1],
                       [2, 3, 3, 5, 5, 3, 3, 2],
                       [5, 6, 6, 7, 7, 6, 6, 5],
                       [8, 8, 8, 8, 8, 8, 8, 8],
                       [10, 10, 10, 10, 10, 10, 10, 10]]

white_pawn_scores_b = [[10, 10, 10, 10, 10, 10, 10, 10],
                       [8, 8, 8, 8, 8, 8, 8, 8],
                       [5, 6, 6, 7, 7, 6, 6, 5],
                       [2, 3, 3, 5, 5, 3, 3, 2],
                       [1, 2, 3, 5, 5, 3, 2, 1],
                       [1, 1, 2, 2, 2, 2, 1, 1],
                       [1, 1, 1, 0, 0, 1, 1, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0]]

king_scores = [[1, 1, 5, 1, 1, 1, 5, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 5, 1, 1, 1, 5, 1]]

piece_position_scores_w = {"N": knight_scores, "B": bishop_scores, "wP": white_pawn_scores_w, "bP": black_pawn_scores_w,
                           "R": rook_scores, "Q": queen_scores, "K": king_scores}

piece_position_scores_b = {"N": knight_scores, "B": bishop_scores, "wP": white_pawn_scores_b, "bP": black_pawn_scores_b,
                           "R": rook_scores, "Q": queen_scores, "K": king_scores}

CHECKMATE = 10000
STALEMATE = 0
DEPTH = 4


def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def find_best_move_1(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponents_moves = gs.get_valid_moves()
        if gs.stale_mate:
            opponent_max_score = STALEMATE
        elif gs.check_mate:
            opponent_max_score = -CHECKMATE
        else:
            opponent_max_score = -CHECKMATE
            for opponents_move in opponents_moves:
                gs.make_move(opponents_move)
                gs.get_valid_moves()
                if gs.check_mate:
                    score = CHECKMATE
                elif gs.stale_mate:
                    score = STALEMATE
                score = -turn_multiplier * score_material(gs.board)
                if score > opponent_max_score:
                    opponent_max_score = score
                gs.undo_move()
        if opponent_max_score < opponent_min_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()

    return best_player_move


# helper method to make first recursive call
def find_best_move(gs, valid_moves, return_queue, play_as):
    global next_move, counter

    start_time = time.time()

    next_move = None
    random.shuffle(valid_moves)
    counter = 0
    find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1, play_as)
    # find_move_nega_max(gs, valid_moves, DEPTH, 1 if gs.white_to_move else -1)
    # find_move_min_max(gs, valid_moves, DEPTH, gs.white_to_move)
    end_time = time.time()
    duration = end_time - start_time

    moves_per_second = counter // duration

    print(f"Search took: {duration:.2f}s")
    print(counter)
    print(f"M/S: {moves_per_second}")

    return_queue.put(next_move)


def find_move_min_max(gs, valid_moves, depth, white_to_move):
    global next_move, counter
    counter += 1
    if depth == 0:
        return score_material(gs.board)

    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score

    else:
        min_score = CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score


def find_move_nega_max(gs, valid_moves, depth, turn_multiplier, play_as):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * score_board(gs, play_as)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max(gs, next_moves, depth - 1, -turn_multiplier, play_as)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    return max_score


def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplier, play_as):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * score_board(gs, play_as)

    # move ordering: - implement later
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move, play_as)
        next_moves = gs.get_valid_moves(play_as)
        score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier, play_as)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
                print(move, score)
        gs.undo_move()
        if max_score > alpha:  # pruning happens
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


# Positive score is good for white, a negative score is good for black
def score_board(gs, play_as):
    if gs.check_mate:
        if gs.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.stale_mate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # score positionally if not a blank
                piece_position_score_w = 0
                piece_position_score_b = 0
                if square[1] == "P":  # for pawns
                    piece_position_score_w = piece_position_scores_w[square][row][col]
                    piece_position_score_b = piece_position_scores_b[square][row][col]
                else:  # for other pieces
                    piece_position_score_w = piece_position_scores_w[square[1]][row][col]
                    piece_position_score_b = piece_position_scores_b[square[1]][row][col]

                if square[0] == "w":
                    if play_as == "White":
                        score += piece_score[square[1]] + piece_position_score_w
                    else:
                        score += piece_score[square[1]] + piece_position_score_b

                elif square[0] == "b":
                    if play_as == "White":
                        score -= piece_score[square[1]] + piece_position_score_w
                    else:
                        score -= piece_score[square[1]] + piece_position_score_b

    return score


def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]

    return score
