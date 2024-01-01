# Stores all info about current state of game. Responsible for legal moves. Keeps a move log.

class GameState:
    def __init__(self, play_as):
        if play_as == "White":
            self.board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

            self.white_king_location = (7, 4)
            self.black_king_location = (0, 4)

        elif play_as == "Black":
            self.board = [
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]

            self.white_king_location = (0, 4)
            self.black_king_location = (7, 4)

        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, "N": self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.white_to_move = True
        self.move_log = []
        self.in_check = False
        self.pins = []
        self.checks = []
        self.check_mate = False
        self.stale_mate = False
        self.enpassant_possible = ()  # coordinates for square where enpassant is possible
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs)]

    def make_move(self, move, play_as):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log move so we can undo if needed
        self.white_to_move = not self.white_to_move
        # update the kings locations
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        # pawn promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        # enpassant move
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--"  # capturing the pawn

        # update enpassant_possible variable
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:  # only on 2 square pawn advances
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()

        self.enpassant_possible_log.append(self.enpassant_possible)

        # castle move
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # king side castle move
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]  # moves rook
                self.board[move.end_row][move.end_col + 1] = "--"
            else:  # queen side castle move
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]  # moves rook
                self.board[move.end_row][move.end_col - 2] = "--"

        # update castling rights - if a rook or king move
        self.update_castle_rights(move, play_as)
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                   self.current_castling_rights.wqs, self.current_castling_rights.bqs))

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            # update the kings locations
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            # undo enpassant move
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--"  # leave landing blank
                self.board[move.start_row][move.end_col] = move.piece_captured
            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]

            # undo castling rights
            self.castle_rights_log.pop()  # get rid of new castle rights of move that we are undoing
            self.current_castling_rights = self.castle_rights_log[-1]  # set castle rights to last one in list

            # undo castle move
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # king side
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:  # queen side
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"

            self.check_mate = False
            self.stale_mate = False

    def update_castle_rights(self, move, play_as):
        if play_as == "White":
            white_castling_rights_row = 7
            black_castling_rights_row = 0
        else:
            white_castling_rights_row = 0
            black_castling_rights_row = 7

        if move.piece_moved == "wK":
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.piece_moved == "bK":
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.piece_moved == "wR":
            if move.start_row == white_castling_rights_row:
                if move.start_col == 0:  # left rook
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights.wks = False
        elif move.piece_moved == "bR":
            if move.start_row == black_castling_rights_row:
                if move.start_col == 0:  # left rook
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights.bks = False

        # if a rook is captured
        if move.piece_captured == "wR":
            if move.end_row == white_castling_rights_row:
                if move.end_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_captured == "bR":
            if move.end_row == black_castling_rights_row:
                if move.end_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.bks = False

    def get_valid_moves(self, play_as):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        if self.in_check:
            if len(self.checks) == 1:  # only 1 check -> block check or move king
                moves = self.get_all_possible_moves(play_as)
                # to block a check you must move a piece into one of the squares between the enemy piece and the king
                check = self.checks[0]  # check information
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]  # enemy piece causing check
                valid_squares = []  # squares that piece can move too
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)  # check[2] and check[3] \
                        # are check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                # Get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != "K":  # move doesn't block king, so it must block or capture
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:  # not in check so all moves are fine
            moves = self.get_all_possible_moves(play_as)
            if self.white_to_move:
                self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves, play_as)
            else:
                self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves, play_as)

        if self.in_check and len(moves) == 0:
            self.check_mate = True
        elif (len(self.move_log) != 0) and not self.in_check and len(moves) == 0:
            self.stale_mate = True

        return moves

    def check_for_pins_and_checks(self):
        pins = []  # squares where allied pinned piece is and direction pinned from
        checks = []  # squares where enemy is applying check
        in_check = False
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        # Check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():  # 1st allied piece could be pinned
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        p_type = end_piece[1]
                        # Checking all opposing necessary pieces except knights
                        if (0 <= j <= 3 and p_type == "R") or \
                                (4 <= j <= 7 and p_type == "B") or \
                                (i == 1 and p_type == "P" and ((enemy_color == "w" and 6 <= j <= 7) or (
                                        enemy_color == "b" and 4 <= j <= 5))) or \
                                (p_type == "Q") or (i == 1 and p_type == "K"):
                            if possible_pin == ():  # no piece blocking
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying check
                            break
        # Check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (2, -1), (2, 1), (1, -2), (1, 2))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking king
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))

        return in_check, pins, checks

    def get_all_possible_moves(self, play_as):
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == "P":
                        self.move_functions[piece](r, c, moves, play_as)
                    else:
                        self.move_functions[piece](r, c, moves)

        return moves

    def get_pawn_moves(self, r, c, moves, play_as):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            if play_as == "White":
                move_amount = -1
                start_row = 6
            else:
                move_amount = 1
                start_row = 1
            enemy_color = "b"
            king_row, king_col = self.white_king_location
        else:
            if play_as == "White":
                move_amount = 1
                start_row = 1
            else:
                move_amount = -1
                start_row = 6
            enemy_color = "w"
            king_row, king_col = self.black_king_location

        if self.board[r + move_amount][c] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + 2*move_amount][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2*move_amount, c), self.board))

        if c - 1 >= 0:  # capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[r + move_amount][c - 1][0] == enemy_color:  # enemy piece to capture
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board))
                if (r + move_amount, c - 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == r:
                        if king_col < c:  # king is left of pawn
                            # inside between king and pawn; outside range between pawn and border
                            inside_range = range(king_col + 1, c - 1)
                            outside_range = range(c + 1, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, c, -1)
                            outside_range = range(c - 2, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != "--":  # some other piece is besides enpassant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):  # attacking piece
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True

                    if not attacking_piece or blocking_piece:
                        moves.append(Move((r, c), (r + move_amount, c - 1), self.board, is_enpassant_move=True))

        if c + 1 <= 7:  # capture to the right
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[r + move_amount][c + 1][0] == enemy_color:  # enemy piece to capture
                    moves.append(Move((r, c), (r + move_amount, c + 1), self.board))
                if (r + move_amount, c + 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == r:
                        if king_col < c:  # king is left of pawn
                            # inside between king and pawn; outside range between pawn and border
                            inside_range = range(king_col + 1, c)
                            outside_range = range(c + 2, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, c + 1, -1)
                            outside_range = range(c - 1, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != "--":  # some other piece is besides enpassant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):  # attacking piece
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True

                    if not attacking_piece or blocking_piece:
                        moves.append(Move((r, c), (r + move_amount, c + 1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":  # can't remove queen from pin on rook, only remove it on bishop
                    self.pins.append(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # left up right down
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece in the way
                            break
                else:  # off board
                    break

    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (2, -1), (2, 1), (1, -2), (1, 2))
        ally_color = "w" if self.white_to_move else "b"
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # diagonals
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece in the way
                            break
                else:  # off board
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"

        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    # Place king back on original location
                    if ally_color == "w":
                        self.white_king_location = (r, c)
                    else:
                        self.black_king_location = (r, c)

    def get_castle_moves(self, r, c, moves, play_as):
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.in_check:
            return  # can't castle if in check
        if (self.white_to_move and self.current_castling_rights.wks) or \
                (not self.white_to_move and self.current_castling_rights.bks):
            self.get_king_side_castle_move(r, c, moves, play_as)
        if (self.white_to_move and self.current_castling_rights.wqs) or \
                (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_queen_side_castle_move(r, c, moves, play_as)

    def get_king_side_castle_move(self, r, c, move, play_as):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            if not self.square_under_attack(r, c + 1, play_as) and not self.square_under_attack(r, c + 2, play_as):
                move.append(Move((r, c), (r, c + 2), self.board, is_castle_move=True))

    def get_queen_side_castle_move(self, r, c, move, play_as):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.square_under_attack(r, c - 1, play_as) and not self.square_under_attack(r, c - 2, play_as):
                move.append(Move((r, c), (r, c - 2), self.board, is_castle_move=True))

    def square_under_attack(self, r, c, play_as):
        self.white_to_move = not self.white_to_move
        opps_moves = self.get_all_possible_moves(play_as)
        self.white_to_move = not self.white_to_move
        for move in opps_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    # mapping keys to values
    # key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # promotion
        self.is_pawn_promotion = (self.piece_moved == "wP" and self.end_row == 0) or \
                                 (self.piece_moved == "bP" and self.end_row == 7)
        # enpassant
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

        # captured
        self.is_capture = self.piece_captured != "--"

        # castling
        self.is_castle_move = is_castle_move

        self.move_ID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]

    def __str__(self):
        # castle move
        if self.is_castle_move:
            return "O-O" if self.end_col == 6 else "O-O-O"

        end_square = self.get_rank_file(self.end_row, self.end_col)
        # pawn moves
        if self.piece_moved[1] == "P":
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            else:
                return end_square

            # pawn promotions

        # adding + for check move and # for checkmate move

        # piece moves
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square
