# two player chess in python with Pygame!
# pawn double space checking
# castling
# en passant
# pawn promotion

import pygame
import constants as c

# draw main game board
def draw_board():
    colors = ['white', 'light gray']
    for row in range(8):
        for col in range(8):
            # Determine the color of the square
            color_index = (row + col) % 2
            color = colors[color_index]
            # Calculate the position and size of the square
            square_rect = pygame.Rect(
                c.board_x + col * c.square_size,
                c.board_y + row * c.square_size,
                c.square_size,
                c.square_size
            )
            # Draw the square
            pygame.draw.rect(c.screen, color, square_rect)
    # Draw board outline
    pygame.draw.rect(c.screen, 'black', (c.board_x, c.board_y, c.board_width, c.board_height), 2)


# draw pieces onto board
def draw_pieces():
    # Draw white pieces
    for i in range(len(c.white_pieces)):
        piece = c.white_pieces[i]
        position = c.white_locations[i]
        image = c.white_images[piece]
        col, row = position
        # Calculate the top-left pixel position of the square
        pos_x = c.board_x + col * c.square_size
        pos_y = c.board_y + row * c.square_size
        # Center the piece image within the square
        piece_rect = image.get_rect(center=(
            pos_x + c.square_size / 2,
            pos_y + c.square_size / 2
        ))
        c.screen.blit(image, piece_rect)
        if c.turn_step < 2 and c.selection == i:
            pygame.draw.rect(c.screen, 'red', piece_rect, 2)

    # Draw black pieces
    for i in range(len(c.black_pieces)):
        piece = c.black_pieces[i]
        position = c.black_locations[i]
        image = c.black_images[piece]
        col, row = position
        pos_x = c.board_x + col * c.square_size
        pos_y = c.board_y + row * c.square_size
        piece_rect = image.get_rect(center=(
            pos_x + c.square_size / 2,
            pos_y + c.square_size / 2
        ))
        c.screen.blit(image, piece_rect)
        if c.turn_step >= 2 and c.selection == i:
            pygame.draw.rect(c.screen, 'blue', piece_rect, 2)


# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list, castling_moves = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []
    castle_moves = check_castling()
    if color == 'white':
        enemies_list = c.black_locations
        friends_list = c.white_locations
    else:
        friends_list = c.black_locations
        enemies_list = c.white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list, castle_moves


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = c.black_locations
        friends_list = c.white_locations
    else:
        friends_list = c.black_locations
        enemies_list = c.white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = c.black_locations
        friends_list = c.white_locations
    else:
        friends_list = c.black_locations
        enemies_list = c.white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in c.white_locations and \
                (position[0], position[1] + 1) not in c.black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] + 2) not in c.white_locations and \
                    (position[0], position[1] + 2) not in c.black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in c.black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in c.black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # add en passant move checker
        if (position[0] + 1, position[1] + 1) == c.black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == c.black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in c.white_locations and \
                (position[0], position[1] - 1) not in c.black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] - 2) not in c.white_locations and \
                    (position[0], position[1] - 2) not in c.black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in c.white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in c.white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # add en passant move checker
        if (position[0] + 1, position[1] - 1) == c.white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == c.white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        friends_list = c.white_locations
    else:
        friends_list = c.black_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for just selected piece
def check_valid_moves():
    if c.selection is not None:
        if c.turn_step < 2:
            options_list = c.white_options
        else:
            options_list = c.black_options

        # Check if c.selection is within the valid range
        if 0 <= c.selection < len(options_list):
            valid_options = options_list[c.selection]
            return valid_options
        else:
            # Invalid c.selection index, return empty list
            print(f"Invalid c.selection index: {c.selection}, options_list length: {len(options_list)}")
            return []
    else:
        return []


# draw valid moves on c.screen
def draw_valid(moves):
    color = 'red' if c.turn_step < 2 else 'blue'
    for move in moves:
        col, row = move
        center_x = c.board_x + col * c.square_size + c.square_size / 2
        center_y = c.board_y + row * c.square_size + c.square_size / 2
        pygame.draw.circle(c.screen, color, (center_x, center_y), 5)

# draw captured pieces on side of c.screen
def draw_captured():
    for i in range(len(c.captured_pieces_white)):
        captured_piece = c.captured_pieces_white[i]
        index = c.piece_list.index(captured_piece)
        position = (
            c.captured_white_start_x,
            c.captured_white_start_y + c.captured_piece_spacing * i
        )
        c.screen.blit(c.small_black_images[index], position)
    for i in range(len(c.captured_pieces_black)):
        captured_piece = c.captured_pieces_black[i]
        index = c.piece_list.index(captured_piece)
        position = (
            c.captured_black_start_x,
            c.captured_black_start_y + c.captured_piece_spacing * i
        )
        c.screen.blit(c.small_white_images[index], position)


# draw a flashing square around king if in check
def draw_check():
    if c.turn_step < 2:
        if 'king' in c.white_pieces:
            king_index = c.white_pieces.index('king')
            king_location = c.white_locations[king_index]
            for i in range(len(c.black_options)):
                if king_location in c.black_options[i]:
                    if c.counter < 15:
                        col, row = king_location
                        pygame.draw.rect(c.screen, 'dark red', [
                            c.board_x + col * c.square_size,
                            c.board_y + row * c.square_size,
                            c.square_size,
                            c.square_size
                        ], 5)
    else:
        if 'king' in c.black_pieces:
            king_index = c.black_pieces.index('king')
            king_location = c.black_locations[king_index]
            for i in range(len(c.white_options)):
                if king_location in c.white_options[i]:
                    if c.counter < 15:
                        col, row = king_location
                        pygame.draw.rect(c.screen, 'dark blue', [
                            c.board_x + col * c.square_size,
                            c.board_y + row * c.square_size,
                            c.square_size,
                            c.square_size
                        ], 5)


def draw_game_over():
    c.screen_width, c.screen_height = c.screen.get_size()
    rect_width, rect_height = 400, 70
    rect_x = (c.screen_width - rect_width) / 2
    rect_y = (c.screen_height - rect_height) / 2

    pygame.draw.rect(c.screen, 'black', [rect_x, rect_y, rect_width, rect_height])
    text_surface1 = c.font.render(f'{c.winner} won the game!', True, 'white')
    text_surface2 = c.font.render(f'Press ENTER to Restart!', True, 'white')

    text_rect1 = text_surface1.get_rect(center=(rect_x + rect_width / 2, rect_y + rect_height / 3))
    text_rect2 = text_surface2.get_rect(center=(rect_x + rect_width / 2, rect_y + 2 * rect_height / 3))

    c.screen.blit(text_surface1, text_rect1)
    c.screen.blit(text_surface2, text_rect2)


# check en passant because people on the internet won't stop bugging me for it
def check_ep(old_coords, new_coords):
    if c.turn_step <= 1:
        index = c.white_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] - 1)
        piece = c.white_pieces[index]
    else:
        index = c.black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        piece = c.black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        # if piece was pawn and moved two spaces, return EP coords as defined above
        pass
    else:
        ep_coords = None  # Use None to indicate no en passant
    return ep_coords


# add castling
def check_castling():
    # king must not currently be in check, neither the rook nor king has moved previously, nothing between
    # and the king does not pass through or finish on an attacked piece
    castle_moves = []  # store each valid castle move as [((king_coords), (castle_coords))]
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0)
    if c.turn_step > 1:
        for i in range(len(c.white_pieces)):
            if c.white_pieces[i] == 'rook':
                rook_indexes.append(c.white_moved[i])
                rook_locations.append(c.white_locations[i])
            if c.white_pieces[i] == 'king':
                king_index = i
                king_pos = c.white_locations[i]
        if not c.white_moved[king_index] and False in rook_indexes and not c.check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in c.white_locations or empty_squares[j] in c.black_locations or \
                            empty_squares[j] in c.black_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        for i in range(len(c.black_pieces)):
            if c.black_pieces[i] == 'rook':
                rook_indexes.append(c.black_moved[i])
                rook_locations.append(c.black_locations[i])
            if c.black_pieces[i] == 'king':
                king_index = i
                king_pos = c.black_locations[i]
        if not c.black_moved[king_index] and False in rook_indexes and not c.check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in c.white_locations or empty_squares[j] in c.black_locations or \
                            empty_squares[j] in c.white_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves


def draw_castling(moves):
    color = 'red' if c.turn_step < 2 else 'blue'
    for move in moves:
        king_col, king_row = move[0]
        rook_col, rook_row = move[1]

        king_center_x = c.board_x + king_col * c.square_size + c.square_size / 2
        king_center_y = c.board_y + king_row * c.square_size + c.square_size / 2
        rook_center_x = c.board_x + rook_col * c.square_size + c.square_size / 2
        rook_center_y = c.board_y + rook_row * c.square_size + c.square_size / 2

        pygame.draw.circle(c.screen, color, (king_center_x, king_center_y), 8)
        c.screen.blit(c.font.render('king', True, 'black'), (king_center_x - 20, king_center_y + 10))
        pygame.draw.circle(c.screen, color, (rook_center_x, rook_center_y), 8)
        c.screen.blit(c.font.render('rook', True, 'black'), (rook_center_x - 20, rook_center_y + 10))
        pygame.draw.line(c.screen, color, (king_center_x, king_center_y), (rook_center_x, rook_center_y), 2)


# add pawn promotion
def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = None
    for i in range(len(c.white_pieces)):
        if c.white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if c.white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(c.black_pieces)):
        if c.black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if c.black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index


def draw_promotion():
    # Define promotion area dimensions
    promo_width = 200
    promo_height = 420
    promo_x = c.board_x + c.board_width + 20
    promo_y = c.board_y

    pygame.draw.rect(c.screen, 'dark gray', [promo_x, promo_y, promo_width, promo_height])

    if white_promote:
        color = 'white'
        for i, piece in enumerate(c.white_promotions):
            image = c.white_images[piece]
            image_rect = image.get_rect()
            image_x = promo_x + (promo_width - image_rect.width) / 2
            image_y = promo_y + 10 + i * (image_rect.height + 10)
            c.screen.blit(image, (image_x, image_y))
    elif black_promote:
        color = 'black'
        for i, piece in enumerate(c.black_promotions):
            image = c.black_images[piece]
            image_rect = image.get_rect()
            image_x = promo_x + (promo_width - image_rect.width) / 2
            image_y = promo_y + 10 + i * (image_rect.height + 10)
            c.screen.blit(image, (image_x, image_y))

    pygame.draw.rect(c.screen, color, [promo_x, promo_y, promo_width, promo_height], 8)


def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]

    promo_width = 200
    promo_height = 420
    promo_x = c.board_x + c.board_width + 20
    promo_y = c.board_y

    if left_click:
        if promo_x <= mouse_pos[0] <= promo_x + promo_width and promo_y <= mouse_pos[1] <= promo_y + promo_height:
            relative_y = mouse_pos[1] - promo_y
            piece_height = 80  # Adjust based on your image sizes
            index = int(relative_y // piece_height)
            if white_promote:
                if 0 <= index < len(c.white_promotions):
                    c.white_pieces[promo_index] = c.white_promotions[index]
                    white_promote = False
            elif black_promote:
                if 0 <= index < len(c.black_promotions):
                    c.black_pieces[promo_index] = c.black_promotions[index]
                    black_promote = False


# main game loop (not used)
if __name__ == "__main__":
    pygame.init()
    c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
    c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
    run = True
    while run:
        c.timer.tick(c.fps)
        if c.counter < 30:
            c.counter += 1
        else:
            c.counter = 0
        c.screen.fill('dark gray')
        draw_board()
        draw_pieces()
        draw_captured()
        draw_check()
        if not c.game_over:
            white_promote, black_promote, promo_index = check_promotion()
            if white_promote or black_promote:
                draw_promotion()
                check_promo_select()
        if c.selection is not None:
            c.valid_moves = check_valid_moves()
            draw_valid(c.valid_moves)
            if selected_piece == 'king':
                draw_castling(castling_moves)
        else:
            c.valid_moves = []
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not c.game_over:
                mouse_x, mouse_y = event.pos
                if c.board_x <= mouse_x < c.board_x + c.board_width and c.board_y <= mouse_y < c.board_y + c.board_height:
                    x_coord = int((mouse_x - c.board_x) // c.square_size)
                    y_coord = int((mouse_y - c.board_y) // c.square_size)
                    click_coords = (x_coord, y_coord)
                    if c.turn_step <= 1:

                        if c.forfeit_button_rect.collidepoint(mouse_x, mouse_y):
                            c.winner = 'black'

                        if click_coords in c.white_locations:
                            c.selection = c.white_locations.index(click_coords)
                            selected_piece = c.white_pieces[c.selection]
                            if c.turn_step == 0:
                                c.turn_step = 1
                        else:
                            c.selection = None  # Deselect if click is not on a piece
                        if click_coords in c.valid_moves and c.selection is not None:
                            c.white_ep = check_ep(c.white_locations[c.selection], click_coords)
                            c.white_locations[c.selection] = click_coords
                            c.white_moved[c.selection] = True
                            if click_coords in c.black_locations:
                                black_piece = c.black_locations.index(click_coords)
                                c.captured_pieces_white.append(c.black_pieces[black_piece])
                                if c.black_pieces[black_piece] == 'king':
                                    c.winner = 'white'
                                c.black_pieces.pop(black_piece)
                                c.black_locations.pop(black_piece)
                                c.black_moved.pop(black_piece)
                            # adding c.check if en passant pawn was captured
                            if c.black_ep is not None and click_coords == c.black_ep:
                                black_piece = c.black_locations.index((c.black_ep[0], c.black_ep[1] - 1))
                                c.captured_pieces_white.append(c.black_pieces[black_piece])
                                c.black_pieces.pop(black_piece)
                                c.black_locations.pop(black_piece)
                                c.black_moved.pop(black_piece)
                            c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                            c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
                            c.turn_step = 2
                            c.selection = None
                            c.valid_moves = []
                        # add option to castle
                        elif c.selection is not None and selected_piece == 'king':
                            for q in range(len(castling_moves)):
                                if click_coords == castling_moves[q][0]:
                                    c.white_locations[c.selection] = click_coords
                                    c.white_moved[c.selection] = True
                                    if click_coords == (1, 0):
                                        rook_coords = (0, 0)
                                    else:
                                        rook_coords = (7, 0)
                                    rook_index = c.white_locations.index(rook_coords)
                                    c.white_locations[rook_index] = castling_moves[q][1]
                                    c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                                    c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
                                    c.turn_step = 2
                                    c.selection = None
                                    c.valid_moves = []
                    if c.turn_step > 1:
                        if c.forfeit_button_rect.collidepoint(mouse_x, mouse_y):
                            c.winner = 'white'

                        if click_coords in c.black_locations:
                            c.selection = c.black_locations.index(click_coords)
                            # c.check what piece is selected, so you can only draw castling moves if king is selected
                            selected_piece = c.black_pieces[c.selection]
                            if c.turn_step == 2:
                                c.turn_step = 3
                        if click_coords in c.valid_moves and c.selection is not None:
                            c.black_ep = check_ep(c.black_locations[c.selection], click_coords)
                            c.black_locations[c.selection] = click_coords
                            c.black_moved[c.selection] = True
                            if click_coords in c.white_locations:
                                white_piece = c.white_locations.index(click_coords)
                                c.captured_pieces_black.append(c.white_pieces[white_piece])
                                if c.white_pieces[white_piece] == 'king':
                                    c.winner = 'black'
                                c.white_pieces.pop(white_piece)
                                c.white_locations.pop(white_piece)
                                c.white_moved.pop(white_piece)
                            if click_coords == c.white_ep:
                                white_piece = c.white_locations.index((c.white_ep[0], c.white_ep[1] + 1))
                                c.captured_pieces_black.append(c.white_pieces[white_piece])
                                c.white_pieces.pop(white_piece)
                                c.white_locations.pop(white_piece)
                                c.white_moved.pop(white_piece)
                            c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                            c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
                            c.turn_step = 0
                            c.selection = None
                            c.valid_moves = []
                        # add option to castle
                        elif c.selection is not None and selected_piece == 'king':
                            for q in range(len(castling_moves)):
                                if click_coords == castling_moves[q][0]:
                                    c.black_locations[c.selection] = click_coords
                                    c.black_moved[c.selection] = True
                                    if click_coords == (1, 7):
                                        rook_coords = (0, 7)
                                    else:
                                        rook_coords = (7, 7)
                                    rook_index = c.black_locations.index(rook_coords)
                                    c.black_locations[rook_index] = castling_moves[q][1]
                                    c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                                    c.white_options = check_options(c.white_pieces, c.white_locations, 'white')
                                    c.turn_step = 0
                                    c.selection = None
                                    c.valid_moves = []
                else:
                    # Handle clicks outside the board (e.g., promotion c.selection)
                    check_promo_select()
            if event.type == pygame.KEYDOWN and c.game_over:
                if event.key == pygame.K_RETURN:
                    c.game_over = False
                    c.winner = ''
                    c.white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    c.white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    c.white_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    c.black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    c.black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    c.black_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    c.captured_pieces_white = []
                    c.captured_pieces_black = []
                    c.turn_step = 0
                    c.selection = None
                    c.valid_moves = []
                    c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
                    c.white_options = check_options(c.white_pieces, c.white_locations, 'white')

        if c.winner != '':
            c.game_over = True
            draw_game_over()

        pygame.display.flip()
    pygame.quit()


# Initialize options
c.black_options = check_options(c.black_pieces, c.black_locations, 'black')
c.white_options = check_options(c.white_pieces, c.white_locations, 'white')