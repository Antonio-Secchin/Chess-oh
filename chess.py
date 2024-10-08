import pygame

# Constants
WIDTH = 1000
HEIGHT = 900
BOARD_SIZE = 8
SQUARE_SIZE = 60
BOARD_X = 350
BOARD_Y = 250
WHITE = 'white'
BLACK = 'black'

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Chess')

# Load images (you'll need to replace these with actual image files)
piece_images = {}
piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
for color in [WHITE, BLACK]:
    for piece in piece_types:
        key = f"{color}_{piece}"
        piece_images[key] = pygame.image.load(f"xadrez/assets/images/{key}.png")
        piece_images[key] = pygame.transform.scale(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))

class Piece:
    points = 0

    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False

    def __str__(self):
        return self.__class__.__name__.lower()

    def get_valid_moves(self, board):
        raise NotImplementedError

    def move(self, new_position):
        self.position = new_position
        self.has_moved = True

    def draw(self, screen):
        piece_type = self.__class__.__name__.lower()
        image_key = f"{self.color}_{piece_type}"
        image = piece_images[image_key]
        col, row = self.position
        pos_x = BOARD_X + col * SQUARE_SIZE
        pos_y = BOARD_Y + row * SQUARE_SIZE
        screen.blit(image, (pos_x, pos_y))

class Custom(Piece):
    def __init__(self,color, position, *args):
        super().__init__(color,position)
        self.components = args   # Guardar as peças passadas como argumento
        self.points = sum(piece.points for piece in args)  # Somar os pontos das peças
        for piece in self.components:
            piece.move(position)
            
    def get_valid_moves(self,board):
        moves = []
        for piece in self.components:
            moves += piece.get_valid_moves(board)
        return moves
    
    def draw(self, screen):
        piece_type = "queen"
        image_key = f"{self.color}_{piece_type}"
        image = piece_images[image_key]
        col, row = self.position
        pos_x = BOARD_X + col * SQUARE_SIZE
        pos_y = BOARD_Y + row * SQUARE_SIZE
        screen.blit(image, (pos_x, pos_y))
        
    def move(self, new_position):
        for piece in self.components:
            piece.move(new_position)
        self.position = new_position

class Pawn(Piece):
    points = 1

    def get_valid_moves(self, board):
        moves = []
        col, row = self.position
        direction = -1 if self.color == WHITE else 1
        
        # Forward move
        if board.is_empty((col, row + direction)):
            moves.append((col, row + direction))
            # Double move from starting position
            if not self.has_moved and board.is_empty((col, row + 2*direction)):
                moves.append((col, row + 2*direction))
        
        # Captures
        for dcol in [-1, 1]:
            if board.is_enemy_piece((col + dcol, row + direction), self.color):
                moves.append((col + dcol, row + direction))
        
        return moves

class Rook(Piece):
    points = 5

    def get_valid_moves(self, board):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_pos = (self.position[0] + i*dx, self.position[1] + i*dy)
                if not board.is_valid_position(new_pos):
                    break
                if board.is_empty(new_pos):
                    moves.append(new_pos)
                elif board.is_enemy_piece(new_pos, self.color):
                    moves.append(new_pos)
                    break
                else:
                    break
        return moves

class Knight(Piece):
    points = 3

    def get_valid_moves(self, board):
        moves = []
        col, row = self.position
        possible_moves = [
            (col+2, row+1), (col+2, row-1), (col-2, row+1), (col-2, row-1),
            (col+1, row+2), (col+1, row-2), (col-1, row+2), (col-1, row-2)
        ]
        for move in possible_moves:
            if board.is_valid_position(move) and (board.is_empty(move) or board.is_enemy_piece(move, self.color)):
                moves.append(move)
        return moves

class Bishop(Piece):
    points = 3

    def get_valid_moves(self, board):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_pos = (self.position[0] + i*dx, self.position[1] + i*dy)
                if not board.is_valid_position(new_pos):
                    break
                if board.is_empty(new_pos):
                    moves.append(new_pos)
                elif board.is_enemy_piece(new_pos, self.color):
                    moves.append(new_pos)
                    break
                else:
                    break
        return moves

class Queen(Piece):
    points = 9

    def get_valid_moves(self, board):
        return Rook.get_valid_moves(self, board) + Bishop.get_valid_moves(self, board)

class King(Piece):
    # Bom.. nunca se sabe.
    #kkkkkkkkkk
    points = 20

    def get_valid_moves(self, board):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            new_pos = (self.position[0] + dx, self.position[1] + dy)
            if board.is_valid_position(new_pos) and (board.is_empty(new_pos) or board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        return moves

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.setup_pieces()

    def setup_pieces(self):
        # Place pawns
        for col in range(BOARD_SIZE):
            self.grid[1][col] = Pawn(BLACK, (col, 1))
            self.grid[6][col] = Pawn(WHITE, (col, 6))

        # Place other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(piece_order):
            self.grid[0][col] = piece_class(BLACK, (col, 0))
            self.grid[7][col] = piece_class(WHITE, (col, 7))
        
    def get_piece_at(self, position):
        col, row = position
        return self.grid[row][col]

    def set_piece_at(self, position, piece):
        col, row = position
        self.grid[row][col] = piece
        if piece:
            piece.position = position

    def is_empty(self, position):
        return self.get_piece_at(position) is None

    def is_enemy_piece(self, position, color):
        if (all(0 <= p < BOARD_SIZE for p in position)):
            piece = self.get_piece_at(position)
        else:
            piece = None
        return piece is not None and piece.color != color

    def is_valid_position(self, position):
        col, row = position
        return 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE

    def move_piece(self, from_pos, to_pos):
        piece = self.get_piece_at(from_pos)
        captured_piece = self.get_piece_at(to_pos)
        self.set_piece_at(from_pos, None)
        self.set_piece_at(to_pos, piece)
        piece.move(to_pos)
        return captured_piece
    
    def is_check(self, color):
        king_position = None
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_position = (col, row)
                    break
            if king_position:
                break
        
        opponent_color = WHITE if color == BLACK else BLACK
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if piece and piece.color == opponent_color:
                    if king_position in piece.get_valid_moves(self):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves(self)
                    for move in valid_moves:
                        # Try the move
                        original_position = piece.position
                        original_piece = self.move_piece(piece.position, move)
                        
                        # Check if the king is still in check
                        still_in_check = self.is_check(color)
                        
                        # Undo the move
                        self.move_piece(move, original_position)
                        self.set_piece_at(move, original_piece)
                        
                        if not still_in_check:
                            return False
        return True
    
    def check_surroundings(self, center_position, my_team):
        col, row = center_position
        surroundings = []

        # Verificar todos os quadrados ao redor (3x3)
        for i in range(col - 1, col + 2):
            for j in range(row - 1, row + 2):
                # Ignorar o centro e posições fora do tabuleiro
                if (i == col and j == row) or not self.is_valid_position((i, j)):
                    continue
                piece = self.get_piece_at((i, j))
                # Verificar se a peça pertence ao time
                if piece and piece.color == my_team:
                    surroundings.append(piece)

        # Verificar se todas as posições ao redor estão ocupadas por peças do meu time
        return len(surroundings) >  0

    def draw(self, screen):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = (255, 206, 158) if (row + col) % 2 == 0 else (209, 139, 71)
                pygame.draw.rect(screen, color, (BOARD_X + col * SQUARE_SIZE, BOARD_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = self.get_piece_at((col, row))
                if piece:
                    piece.draw(screen)
                    
    

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = WHITE
        self.qtd_plays = {WHITE: 1, BLACK: 1}
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.captured_pieces = {WHITE: [], BLACK: []}
        
    def set_qtd_plays(self, qtd, color):
        self.qtd_plays[color] = qtd

    def new_piece(self, piece_name, color, position, replace=False, *args):
        piece_class = globals()[piece_name.lower().capitalize()]
        if not args:
            piece = piece_class(color, position)
        else:
            piece = piece_class(color, position, *args)
        board = self.board
        if (board.get_piece_at(position) is not None and not replace):
            return False
        board.set_piece_at(position, piece)
        return True

    def remove_piece(self, piece):
        if self.selected_piece is piece:
            self.selected_piece = None
        self.board.set_piece_at(piece.position, None)

    def isWhitesTurn(self):
        return self.current_turn == WHITE

    def handle_click(self, pos):
        col = (pos[0] - BOARD_X) // SQUARE_SIZE
        row = (pos[1] - BOARD_Y) // SQUARE_SIZE
        clicked_pos = (col, row)

        if self.board.is_valid_position(clicked_pos):
            if self.selected_piece:
                if clicked_pos in self.valid_moves:
                    captured_piece = self.board.move_piece(self.selected_piece.position, clicked_pos)
                    if captured_piece:
                        self.captured_pieces[self.current_turn].append(captured_piece)
                    
                    if self.qtd_plays[self.current_turn] == 1:
                        self.end_turn()
                    else:
                        self.qtd_plays[self.current_turn] -=1
                    
                self.selected_piece = None
                self.valid_moves = []
            else:
                piece = self.board.get_piece_at(clicked_pos)
                if piece and piece.color == self.current_turn:
                    self.selected_piece = piece
                    self.valid_moves = piece.get_valid_moves(self.board)
        return self.selected_piece, clicked_pos

    def _find_kings(self):
        return [piece for row in self.board.grid for piece in row if isinstance(piece, King)]

    def end_turn(self):
        self.current_turn = BLACK if self.current_turn == WHITE else WHITE
        kings = self._find_kings()
        if len(kings) == 1:
            self.game_over = True
            self.winner = WHITE if kings[0].color == WHITE else BLACK            
            
    def checkPlacement(self, center_position, team):
        return self.board.check_surroundings(center_position, team)

    def draw(self, screen):
        self.board.draw(screen)
        if self.selected_piece:
            pygame.draw.rect(screen, (255, 0, 0), (BOARD_X + self.selected_piece.position[0] * SQUARE_SIZE,
                                                   BOARD_Y + self.selected_piece.position[1] * SQUARE_SIZE,
                                                   SQUARE_SIZE, SQUARE_SIZE), 4)
            for move in self.valid_moves:
                pygame.draw.circle(screen, (0, 255, 0), 
                                   (BOARD_X + move[0] * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    BOARD_Y + move[1] * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

        if self.game_over:
            font = pygame.font.Font("freesansbold.ttf", 36)
            text = font.render(f"{self.winner} wins!", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

def main():
    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(pygame.mouse.get_pos())

        screen.fill((255, 255, 255))
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

