import pygame
import chess
from transformers import AutoModelForCausalLM, AutoTokenizer
from bot.inference import next_move

model1 = AutoModelForCausalLM.from_pretrained("Vasanth/chessdevilaifen_v2")
tokenizer1 = AutoTokenizer.from_pretrained("Vasanth/chessdevilaifen_v2")
tokenizer1.pad_token = tokenizer1.eos_token

model2 = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer2 = AutoTokenizer.from_pretrained("gpt2")
tokenizer2.pad_token = tokenizer2.eos_token

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
    for i in range(len(move)):
        if i!=len(move)-1:
            legal_move = chess.Move.from_uci(move[i])
            if legal_move in board.legal_moves:
                return legal_move
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


def main_two_agent(BOARD):
    '''
    for agent vs agent game
    
    '''
  
    #make background black
    scrn.fill(BLACK)
    pygame.display.set_caption('Chess')

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)
        
        fen1 = BOARD.fen()
        BOARD.push(agent(BOARD, model1, tokenizer1, fen1))

        fen2 = BOARD.fen()
        BOARD.push(agent(BOARD, model2, tokenizer2, fen2))

        scrn.fill(BLACK)
            
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                status = False
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pygame.quit()

main_two_agent(b)