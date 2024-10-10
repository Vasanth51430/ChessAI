import pygame
import chess
import math
from transformers import AutoModelForCausalLM, AutoTokenizer
from bot.inference import next_move

model = AutoModelForCausalLM.from_pretrained("Vasanth/chessdevilaifen_v2")
tokenizer = AutoTokenizer.from_pretrained("Vasanth/chessdevilaifen_v2")
tokenizer.pad_token = tokenizer.eos_token

# Initialize pygame
pygame.init()

# Set up display
X = 800
Y = 800
scrn = pygame.display.set_mode((X, Y))
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Basic colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)
BROWN_LIGHT = (222, 196, 156)  # Light brown
BROWN_DARK = (160, 124, 84)    # Dark brown

# Initialize chess board
b = chess.Board()

# Load SVG piece images and convert to pygame surfaces
pieces = {
    'p': pygame.image.load('res/black_pawn.png').convert_alpha(),
    'n': pygame.image.load('res/black_knight.png').convert_alpha(),
    'b': pygame.image.load('res/black_bishop.png').convert_alpha(),
    'r': pygame.image.load('res/black_rook.png').convert_alpha(),
    'q': pygame.image.load('res/black_queen.png').convert_alpha(),
    'k': pygame.image.load('res/black_king.png').convert_alpha(),
    'P': pygame.image.load('res/white_pawn.png').convert_alpha(),
    'N': pygame.image.load('res/white_knight.png').convert_alpha(),
    'B': pygame.image.load('res/white_bishop.png').convert_alpha(),
    'R': pygame.image.load('res/white_rook.png').convert_alpha(),
    'Q': pygame.image.load('res/white_queen.png').convert_alpha(),
    'K': pygame.image.load('res/white_king.png').convert_alpha(),
}


def agent(board, model, tokenizer, fen):
    move =  next_move(model, tokenizer, fen)
    for i in range(4):
        if i!=3:
            move = chess.Move.from_uci(move[i])
            if move in board.legal_moves:
                return move
            else:
                pass
        else:
            return chess.Move.from_uci(move[i])

def update(scrn,board):
    '''
    updates the screen basis the board class
    '''
    square_colors = [BROWN_LIGHT, BROWN_DARK]
    
    for i in range(64):
        row = i // 8
        col = i % 8
        color = square_colors[(row + col) % 2]
        pygame.draw.rect(scrn, color, pygame.Rect(col * 100, row * 100, 100, 100))

    for i in range(64):
        piece = board.piece_at(i)
        if piece == None:
            pass
        else:
            scrn.blit(pieces[str(piece)],((i%8)*100,700-(i//8)*100))
    
    for i in range(7):
        i=i+1
        pygame.draw.line(scrn,BLACK,(0,i*100),(800,i*100))
        pygame.draw.line(scrn,BLACK,(i*100,0),(i*100,800))

    pygame.display.flip()

def main_one_agent(BOARD,agent_color=False):
    
    '''
    for agent vs human game
    color is True = White agent
    color is False = Black agent
    '''
    
    #make background black
    scrn.fill(BLACK)
    #name window
    pygame.display.set_caption('Chess')
    
    #variable to be used later
    index_moves = []

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)
     
        if BOARD.turn==agent_color:
            fen = BOARD.fen()
            BOARD.push(agent(BOARD, model, tokenizer, fen))
            scrn.fill(BLACK)

        else:

            for event in pygame.event.get():
         
                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if event.type == pygame.QUIT:
                    status = False

                # if mouse clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #reset previous screen from clicks
                    scrn.fill(BLACK)
                    #get position of mouse
                    pos = pygame.mouse.get_pos()

                    #find which square was clicked and index of it
                    square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                    index = (7-square[1])*8+(square[0])
                    
                    # if we have already highlighted moves and are making a move
                    if index in index_moves: 
                        
                        move = moves[index_moves.index(index)]
                        #print(BOARD)
                        #print(move)
                        BOARD.push(move)
                        index=None
                        index_moves = []
                        
                    # show possible moves
                    else:
                        
                        piece = BOARD.piece_at(index)
                        
                        if piece == None:
                            
                            pass
                        else:

                            all_moves = list(BOARD.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    
                                    moves.append(m)

                                    t = m.to_square

                                    TX1 = 100*(t%8)
                                    TY1 = 100*(7-t//8)

                                    
                                    pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,100,100),5)
                            #print(moves)
                            index_moves = [a.to_square for a in moves]
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
            if BOARD.outcome().winner:
                text_surface = my_font.render('White Wins', False, (0, 0, 0))
                scrn.blit(text_surface, (0,0))
                pygame.time.delay(1000)
            else:
                text_surface = my_font.render('Black Wins', False, (0, 0, 0))
                scrn.blit(text_surface, (0,0))
                pygame.time.delay(1000)

    pygame.quit()

main_one_agent(b, False)