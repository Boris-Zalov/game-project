import pygame
from pygame.locals import *
from .components.button import Button
from .components.chessboard import CBoard
from .components.chessboard_drawer import ChessboardDrawer
import pygame_widgets
from pygame_widgets.textbox import TextBox
import chess
import chess.engine
                
player_move = ""

def get_let(board, is_white, x, b_keys):    
    if pygame.mouse.get_focused() != 0:
        index = (x - board.x) // (board.width // 8)
        if -1 < index < len(b_keys):
            if is_white:
                return b_keys[index]
            else:
                b_keys.reverse()
                return b_keys[index]
        return None

def get_num(board, is_white, y): 
    if pygame.mouse.get_focused() != 0:  
        if board.top <= y <= board.bottom:
            if is_white:
                return 8 - (y - board.top) // (board.width // 8)
            else:
                return (y - board.top) // (board.width // 8) + 1
        return None
        

def run(game, difficulty, is_white):
    global player_move
    def set_move(f, nothing):
        global player_move
        print(player_move)
        player_move = move_filed.getText()
        f.setText("")
    running = True
    engine = game.get_engine()
    cboard = CBoard()
    board = chess.Board()
    fields = {
        "a": [None, None, None, None, None, None, None, None],
        "b": [None, None, None, None, None, None, None, None],
        "c": [None, None, None, None, None, None, None, None],
        "d": [None, None, None, None, None, None, None, None],
        "e": [None, None, None, None, None, None, None, None],
        "f": [None, None, None, None, None, None, None, None],
        "g": [None, None, None, None, None, None, None, None],
        "h": [None, None, None, None, None, None, None, None]
    }
    engine.configure({"Skill Level": difficulty})
    player_turn = is_white
    cd = ChessboardDrawer(game, is_white)
    cd.draw(cboard, fields)
    if eval(game.settings["keyboard_moves"]):
        move_filed = TextBox(game.screen, 500, 100, 800, 50, font=game.fonts["small_text"], fontSize=50, textColour=(0, 0, 0),
                  onSubmit=set_move, radius=20, borderThickness=5)
        move_filed.onSubmitParams=(move_filed, None)
        size_x, size_y = game.screen.get_size() 
        move_filed.setWidth(int(size_x // 3))
        move_filed.setX(int(size_x // 2 - move_filed.getWidth() // 2))
        move_filed.setY(int(size_y * 0.92))
    
    
    while running:
        game.screen.fill(game.colors["main"])
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            let  = get_let(cd.rect, is_white, pygame.mouse.get_pos()[0], list(fields.keys()))
            num = get_num(cd.rect, is_white, pygame.mouse.get_pos()[1])
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if let and num and (let + str(num) != player_move) and player_turn:
                    player_move += let + str(num)
            if event.type == VIDEORESIZE or event.type == VIDEOEXPOSE:
                cd.resize()
                size_x, size_y = game.screen.get_size() 
                move_filed.setWidth(int(size_x // 3))
                move_filed.setX(int(size_x // 2 - move_filed.getWidth() // 2))
                move_filed.setY(int(size_y * 0.92))
    
        if player_turn:
            if len(player_move) >= 4:
                player_move = chess.Move.from_uci(player_move)
                if player_move in board.legal_moves:
                    board.push(player_move)
                    cboard.push(str(player_move))
                    player_turn = not player_turn
                player_move = ""
                
        else:
            result = engine.play(board, chess.engine.Limit(time=0))
            board.push(result.move)
            cboard.push(str(result.move))
            player_turn = not player_turn
            
        cd.draw(cboard, fields, (player_move if len(player_move) == 2 and player_turn else False))
        
        game.coursor()
        pygame.display.update()
    if eval(game.settings["keyboard_moves"]):
        move_filed.hide()
        move_filed.disable()