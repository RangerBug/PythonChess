# Driver file, handles user input and displaying current game stats
import sys
import pygame as py

import ChessEngine
import ChessAI
from ChessEngine import *
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 700
MOVE_LOG_PANEL_WIDTH = 320
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
TIME_PANEL_WIDTH = BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH
TIME_PANEL_HEIGHT = 100
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images(p_style):
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bP", "bR", "bN", "bB", "bQ", "bK"]
    p = p_style.get_style()
    if p == 1:
        for piece in pieces:
            IMAGES[piece] = py.transform.scale(py.image.load("images/pieceStyle1/" + piece + ".png"),
                                               (SQ_SIZE, SQ_SIZE))
    if p == 2:
        for piece in pieces:
            IMAGES[piece] = py.transform.scale(py.image.load("images/pieceStyle2/" + piece + ".png"),
                                               (SQ_SIZE, SQ_SIZE))


def main():
    py.init()
    py.display.set_caption("Main Menu")
    screen = py.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT + TIME_PANEL_HEIGHT))
    clock = py.time.Clock()
    screen.fill(py.Color(50, 50, 50))

    # Buttons
    start_button = py.Rect(screen.get_width() / 2 - 200, screen.get_height() - 200, 400, 80)
    start_button_text = "Start Game"
    quit_button = py.Rect(screen.get_width() / 2 - 200, screen.get_height() - 100, 400, 80)
    quit_button_text = "Quit"

    # Title
    font = py.font.SysFont("Georgia", 120, True, False)
    text_object = font.render("CHESS", True, py.Color("White"))
    text_location = py.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT)
    screen.blit(text_object, text_location.move(screen.get_width() / 2 - text_object.get_width() / 2, 75))

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            # mouse handler
            mouse_pressed = py.mouse.get_pressed()
            if mouse_pressed[0]:
                # Check if the mouse cursor is within the button's rect
                mouse_pos = py.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    settings_menu()
                    running = False
                elif quit_button.collidepoint(mouse_pos):
                    py.quit()
                    sys.exit()

        draw_button(screen, start_button, start_button_text, "Georgia", 32, (255, 255, 255), (0, 0, 0))
        draw_button(screen, quit_button, quit_button_text, "Georgia", 32, (255, 255, 255), (0, 0, 0))

        clock.tick(MAX_FPS)
        py.display.flip()


def settings_menu():  # TODO: difficulty - time controls
    py.init()
    py.display.set_caption("Settings Menu")
    screen = py.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT + TIME_PANEL_HEIGHT))
    clock = py.time.Clock()
    p_style = Style(1)
    b_style = Style(1)
    this_game_style = Game_Style(True, False)

    # Highlighting the settings selections
    piece_highlight = Highlight_Selection(screen, 240, 220)
    board_highlight = Highlight_Selection(screen, 260, 335)
    game_style_highlight = Highlight_Selection(screen, 250, 435)

    # Buttons
    start_button = py.Rect(screen.get_width() / 2 - 200, screen.get_height() - 100, 400, 80)
    start_button_text = "Start"

    # Image Buttons
    # Piece Styles
    piece_type1 = py.image.load('images/pieceStyle1/wK.png').convert_alpha()
    piece_button1 = Button(240, 220, piece_type1, .7)
    piece_type2 = py.image.load('images/pieceStyle2/wK.png').convert_alpha()
    piece_button2 = Button(340, 220, piece_type2, 1.5)
    # Board Styles
    board_type1 = py.image.load('images/buttonImages/style1.png').convert_alpha()
    board_button1 = Button(260, 335, board_type1, .45)
    board_type2 = py.image.load('images/buttonImages/style2.png').convert_alpha()
    board_button2 = Button(370, 335, board_type2, .45)
    board_type3 = py.image.load('images/buttonImages/style3.png').convert_alpha()
    board_button3 = Button(480, 335, board_type3, .45)
    board_type4 = py.image.load('images/buttonImages/style4.png').convert_alpha()
    board_button4 = Button(590, 335, board_type4, .45)
    board_type5 = py.image.load('images/buttonImages/style5.png').convert_alpha()
    board_button5 = Button(700, 335, board_type5, .45)
    # Game Style - 1pw - 1pb - 2p - 0p
    one_player_white = py.image.load('images/pieceStyle1/wK.png').convert_alpha()
    one_player_white_button = Button(250, 435, one_player_white, .7)
    one_player_black = py.image.load('images/pieceStyle1/bK.png').convert_alpha()
    one_player_black_button = Button(360, 435, one_player_black, .7)
    two_player = py.image.load('images/pieceStyle1/bK.png').convert_alpha()
    two_player_button = Button(470, 435, two_player, .7)
    two_player_two = py.image.load('images/pieceStyle1/wK.png').convert_alpha()
    two_player_two_button = Button(490, 435, two_player_two, .7)
    ai_vs_ai = py.image.load('images/buttonImages/aivsai.png').convert_alpha()
    ai_vs_ai_button = Button(600, 435, ai_vs_ai, .065)

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            # mouse handler
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse cursor is within the button's rect
                mouse_pos = py.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    load_images(p_style)
                    get_color(b_style)
                    game(b_style, this_game_style)

        # Drawing all texts in settings
        draw_settings_texts(screen)

        draw_button(screen, start_button, start_button_text, "Georgia", 32, (255, 255, 255), (0, 0, 0))

        # Highlighting selection
        piece_highlight.draw_highlight(screen, False)
        board_highlight.draw_highlight(screen, True)
        game_style_highlight.draw_highlight(screen, False)

        # Image Buttons and Handlers
        if piece_button1.draw(screen):
            piece_highlight.set_pos(240, 220)
            p_style.set_style(1)
            load_images(p_style)
        if piece_button2.draw(screen):
            piece_highlight.set_pos(340, 220)
            p_style.set_style(2)
            load_images(p_style)
        if board_button1.draw(screen):
            board_highlight.set_pos(260, 335)
            b_style.set_style(1)
        if board_button2.draw(screen):
            board_highlight.set_pos(370, 335)
            b_style.set_style(2)
        if board_button3.draw(screen):
            board_highlight.set_pos(480, 335)
            b_style.set_style(3)
        if board_button4.draw(screen):
            board_highlight.set_pos(590, 335)
            b_style.set_style(4)
        if board_button5.draw(screen):
            board_highlight.set_pos(700, 335)
            b_style.set_style(5)
        if one_player_white_button.draw(screen):
            game_style_highlight.set_pos(250, 435)
            this_game_style.set_game_style(True, False)
        if one_player_black_button.draw(screen):
            game_style_highlight.set_pos(360, 435)
            this_game_style.set_game_style(False, True)
        if two_player_button.draw(screen) or two_player_two_button.draw(screen):
            game_style_highlight.set_pos(470, 435)
            this_game_style.set_game_style(True, True)
        if ai_vs_ai_button.draw(screen):
            game_style_highlight.set_pos(600, 435)
            this_game_style.set_game_style(False, False)

        clock.tick(MAX_FPS)
        py.display.flip()


def game(b_style, this_game_style):  # TODO: - Timers - save game? - pawn promotion selection
    py.init()
    py.display.set_caption("Chess")
    screen = py.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT + TIME_PANEL_HEIGHT))
    clock = py.time.Clock()
    screen.fill(py.Color("Black"))
    move_log_font = py.font.SysFont("Arial", 20, False, False)
    player_one, player_two = this_game_style.get_game_styles()
    if not player_one and player_two:
        bottom_color = "Black"
    else:
        bottom_color = "White"
    gs = GameState(bottom_color)
    valid_moves = gs.get_valid_moves(bottom_color)
    move_made = False  # flag for when a move is made
    animate = False  # flag to animate
    sq_selected = ()  # no square is selected, keeps track of last click tuple: (row, col)
    player_clicks = []  # keeps track of player clicks (two tuples)
    game_over = False
    AI_thinking = False
    move_finder_process = None
    move_undone = False
    running = True

    # Image Buttons
    main_menu_image = py.image.load('images/buttonImages/home.png').convert_alpha()
    main_menu_button = Button(screen.get_width() - 100, screen.get_height() - 100, main_menu_image, 1.5)
    reset_game_image = py.image.load('images/buttonImages/return.png').convert_alpha()
    reset_game_button = Button(screen.get_width() - 200, screen.get_height() - 100, reset_game_image, 1.5)
    undo_move_image = py.image.load('images/buttonImages/arrowLeft.png').convert_alpha()
    undo_move_button = Button(screen.get_width() - 300, screen.get_height() - 100, undo_move_image, 1.5)

    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            # mouse handler
            elif event.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()  # x and y of mouse, if add extra stuff on screen fix position
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sq_selected == (row, col) or col >= 8 or row >= 8:  # user clicked same square twice or deselect
                        sq_selected = ()  # deselect
                        player_clicks = []  # clear player clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)  # append first and second clicks
                    if len(player_clicks) == 2 and human_turn:
                        move = Move(player_clicks[0], player_clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i], bottom_color)
                                move_made = True
                                animate = True
                                sq_selected = ()
                                player_clicks = []
                                print(move.get_chess_notation())
                        if not move_made:
                            player_clicks = [sq_selected]
            # key handler
            elif event.type == py.KEYDOWN:
                if event.key == py.K_z:  # undo move
                    gs.undo_move()
                    sq_selected = ()
                    player_clicks = []
                    move_made = True
                    animate = False
                    game_over = False
                    if AI_thinking:
                        move_finder_process.terminate()
                        AI_thinking = False
                    move_undone = True

                if event.key == py.K_r:  # reset the board
                    gs = ChessEngine.GameState(bottom_color)
                    valid_moves = gs.get_valid_moves(bottom_color)
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if AI_thinking:
                        move_finder_process.terminate()
                        AI_thinking = False
                    move_undone = True
                    main()

        # AI move finder logic
        if not game_over and not human_turn and not move_undone:
            if not AI_thinking:
                AI_thinking = True
                print("Thinking...")
                return_queue = Queue()  # pass data between threads
                move_finder_process = Process(target=ChessAI.find_best_move, args=(gs, valid_moves, return_queue, bottom_color))
                move_finder_process.start()  # call find_best_move(gs, valid_moves, return_queue

            if not move_finder_process.is_alive():
                print("Done Thinking")
                AI_move = return_queue.get()
                if AI_move is None:
                    AI_move = ChessAI.find_random_move(valid_moves)
                gs.make_move(AI_move, bottom_color)
                move_made = True
                animate = True
                AI_thinking = False

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock, b_style)
            valid_moves = gs.get_valid_moves(bottom_color)
            move_made = False
            animate = False
            move_undone = False

        draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font, b_style)

        # Image Button Draw and Handler
        if main_menu_button.draw(screen):
            main()
        elif reset_game_button.draw(screen):
            print("Game Reset")
            gs = ChessEngine.GameState(bottom_color)
            valid_moves = gs.get_valid_moves(bottom_color)
            sq_selected = ()
            player_clicks = []
            move_made = False
            animate = False
            game_over = False
            if AI_thinking:
                move_finder_process.terminate()
                AI_thinking = False
            move_undone = True
        elif undo_move_button.draw(screen):
            print("Undo Move")
            gs.undo_move()
            sq_selected = ()
            player_clicks = []
            move_made = True
            animate = False
            game_over = False
            if AI_thinking:
                move_finder_process.terminate()
                AI_thinking = False
            move_undone = True

        if gs.check_mate:
            game_over = True
            if gs.white_to_move:
                draw_end_game_text(screen, "Black Wins By Checkmate!")
            else:
                draw_end_game_text(screen, "White Wins By Checkmate!")
        elif gs.stale_mate:
            game_over = True
            draw_end_game_text(screen, "Stalemate")

        clock.tick(MAX_FPS)
        py.display.flip()


def draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font, b_style):
    draw_board(screen, b_style)  # draw squares
    highlight_squares(screen, gs, valid_moves, sq_selected)  # highlighting squares
    draw_pieces(screen, gs.board)  # draw pieces on top of squares
    draw_move_log(screen, gs, move_log_font)
    draw_time_panel(screen)


def draw_board(screen, b_style):
    global colors
    colors = get_color(b_style)
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):  # square selected is a piece that can be moved
            # highlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value
            s.fill(py.Color("blue"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight valid moves
            s.fill(py.Color("yellow"))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (SQ_SIZE * move.end_col, SQ_SIZE * move.end_row))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_move_log(screen, gs, font):
    move_log_rect = py.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    py.draw.rect(screen, py.Color("black"), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + ". " + str(move_log[i]) + " "
        if i + 1 < len(move_log):  # make sure black made a move
            move_string += str(move_log[i + 1]) + " "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]
        text_object = font.render(text, True, py.Color("white"))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def draw_time_panel(screen):
    time_panel_rect = py.Rect(0, BOARD_HEIGHT, TIME_PANEL_WIDTH, TIME_PANEL_HEIGHT)
    py.draw.rect(screen, py.Color("black"), time_panel_rect)


def animate_move(move, screen, board, clock, b_style):
    global colors
    dR = move.end_row - move.start_row
    dC = move.end_col - move.start_col
    frame_count = 20

    for frame in range(frame_count + 1):
        r, c = (move.start_row + dR * frame / frame_count, move.start_col + dC * frame / frame_count)
        draw_board(screen, b_style)
        draw_pieces(screen, board)
        # erase piece moved from ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = py.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        py.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != "--":
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == "b" else move.end_row - 1
                end_square = py.Rect(move.end_col * SQ_SIZE, enpassant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        py.display.flip()
        clock.tick(60)


def draw_end_game_text(screen, text):
    font = py.font.SysFont("Arial", 32, True, False)
    text_object = font.render(text, True, py.Color("gray"))
    text_location = py.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                  BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    for y in range(-2, 3):
        for x in range(-2, 3):
            screen.blit(text_object, text_location.move(x, y))
    text_object = font.render(text, True, py.Color("black"))
    screen.blit(text_object, text_location)


def draw_button(screen, rect, text, font, font_size, text_color, button_color):
    # Render the text
    font = py.font.SysFont(font, font_size, False, False)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center

    # Draw the button
    py.draw.rect(screen, button_color, rect)
    screen.blit(text_surface, text_rect)


def get_color(b_style):
    color_list = {1: [py.Color("white"), py.Color("darkgrey")],
                  2: [py.Color("silver"), py.Color("olive")],
                  3: [py.Color("silver"), py.Color("blue")],
                  4: [py.Color("aqua"), py.Color("teal")],
                  5: [py.Color("silver"), py.Color("fuchsia")]}
    return color_list[b_style.get_style()]


def draw_settings_texts(screen):
    screen.fill(py.Color(50, 50, 50))

    # Title
    font = py.font.SysFont("Georgia", 100, True, False)
    text_object = font.render("Settings", True, py.Color("White"))
    text_location = py.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT)
    screen.blit(text_object, text_location.move(screen.get_width() / 2 - text_object.get_width() / 2, 55))

    # Texts
    text_font = py.font.SysFont("Georgia", 35, True, False)
    # Piece Style
    piece_style = text_font.render("Piece Style", True, py.Color("White"))
    text_location = py.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT)
    screen.blit(piece_style, text_location.move(20, 250))
    # Board Color
    piece_style = text_font.render("Board Style", True, py.Color("White"))
    screen.blit(piece_style, text_location.move(20, 350))
    # Opponent type
    piece_style = text_font.render("Game Style", True, py.Color("White"))
    screen.blit(piece_style, text_location.move(20, 450))
    # Time limits
    # piece_style = text_font.render("Time Limits", True, py.Color("White"))
    # screen.blit(piece_style, text_location.move(20, 550))


# button class
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = py.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = py.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if py.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if py.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# style class for pieces and board
class Style:
    def __init__(self, style):
        self.style = style

    # setter method
    def set_style(self, style):
        self.style = style

    # getter method
    def get_style(self):
        return self.style


class Game_Style:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two

    def set_game_style(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two

    def get_game_styles(self):
        return self.player_one, self.player_two


class Highlight_Selection:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw_highlight(self, screen, is_board):
        if is_board:
            t = py.Surface((SQ_SIZE + 5, SQ_SIZE + 5))
            t.set_alpha(100)  # transparency value
            t.fill(py.Color("yellow"))
            screen.blit(t, (self.x - 8, self.y - 8))
        else:
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value
            s.fill(py.Color("yellow"))
            screen.blit(s, (self.x, self.y))


if __name__ == "__main__":
    main()
