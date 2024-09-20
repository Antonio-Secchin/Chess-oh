# two player chess in python with Pygame!
# pawn double space checking
# castling
# en passant
# pawn promotion

import pygame
from constants import *

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
                board_x + col * square_size,
                board_y + row * square_size,
                square_size,
                square_size
            )
            # Draw the square
            pygame.draw.rect(screen, color, square_rect)
    # Draw board outline
    pygame.draw.rect(screen, 'black', (board_x, board_y, board_width, board_height), 2)


# draw pieces onto board
def draw_pieces():
    # Draw white pieces
    for i in range(len(white_pieces)):
        piece = white_pieces[i]
        position = white_locations[i]
        image = white_images[piece]
        col, row = position
        # Calculate the top-left pixel position of the square
        pos_x = board_x + col * square_size
        pos_y = board_y + row * square_size
        # Center the piece image within the square
        piece_rect = image.get_rect(center=(
            pos_x + square_size / 2,
            pos_y + square_size / 2
        ))
        screen.blit(image, piece_rect)
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red', piece_rect, 2)

    # Draw black pieces
    for i in range(len(black_pieces)):
        piece = black_pieces[i]
        position = black_locations[i]
        image = black_images[piece]
        col, row = position
        pos_x = board_x + col * square_size
        pos_y = board_y + row * square_size
        piece_rect = image.get_rect(center=(
            pos_x + square_size / 2,
            pos_y + square_size / 2
        ))
        screen.blit(image, piece_rect)
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'blue', piece_rect, 2)


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
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
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
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
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
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
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
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # add en passant move checker
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # add en passant move checker
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for just selected piece
def check_valid_moves():
    if selection is not None:
        if turn_step < 2:
            options_list = white_options
        else:
            options_list = black_options
        
        # Check if selection is within the valid range
        if 0 <= selection < len(options_list):
            valid_options = options_list[selection]
            return valid_options
        else:
            # Invalid selection index, return empty list
            print(f"Invalid selection index: {selection}, options_list length: {len(options_list)}")
            return []
    else:
        return []


# draw valid moves on screen
def draw_valid(moves):
    color = 'red' if turn_step < 2 else 'blue'
    for move in moves:
        col, row = move
        center_x = board_x + col * square_size + square_size / 2
        center_y = board_y + row * square_size + square_size / 2
        pygame.draw.circle(screen, color, (center_x, center_y), 5)

# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        position = (
            captured_white_start_x,
            captured_white_start_y + captured_piece_spacing * i
        )
        screen.blit(small_black_images[index], position)
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        position = (
            captured_black_start_x,
            captured_black_start_y + captured_piece_spacing * i
        )
        screen.blit(small_white_images[index], position)


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        col, row = king_location
                        pygame.draw.rect(screen, 'dark red', [
                            board_x + col * square_size,
                            board_y + row * square_size,
                            square_size,
                            square_size
                        ], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        col, row = king_location
                        pygame.draw.rect(screen, 'dark blue', [
                            board_x + col * square_size,
                            board_y + row * square_size,
                            square_size,
                            square_size
                        ], 5)


def draw_game_over():
    screen_width, screen_height = screen.get_size()
    rect_width, rect_height = 400, 70
    rect_x = (screen_width - rect_width) / 2
    rect_y = (screen_height - rect_height) / 2

    pygame.draw.rect(screen, 'black', [rect_x, rect_y, rect_width, rect_height])
    text_surface1 = font.render(f'{winner} won the game!', True, 'white')
    text_surface2 = font.render(f'Press ENTER to Restart!', True, 'white')

    text_rect1 = text_surface1.get_rect(center=(rect_x + rect_width / 2, rect_y + rect_height / 3))
    text_rect2 = text_surface2.get_rect(center=(rect_x + rect_width / 2, rect_y + 2 * rect_height / 3))

    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)


# check en passant because people on the internet won't stop bugging me for it
def check_ep(old_coords, new_coords):
    if turn_step <= 1:
        index = white_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] - 1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        piece = black_pieces[index]
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
    if turn_step > 1:
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'rook':
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i] == 'king':
                king_index = i
                king_pos = white_locations[i]
        if not white_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in black_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'rook':
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == 'king':
                king_index = i
                king_pos = black_locations[i]
        if not black_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in white_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves


def draw_castling(moves):
    color = 'red' if turn_step < 2 else 'blue'
    for move in moves:
        king_col, king_row = move[0]
        rook_col, rook_row = move[1]

        king_center_x = board_x + king_col * square_size + square_size / 2
        king_center_y = board_y + king_row * square_size + square_size / 2
        rook_center_x = board_x + rook_col * square_size + square_size / 2
        rook_center_y = board_y + rook_row * square_size + square_size / 2

        pygame.draw.circle(screen, color, (king_center_x, king_center_y), 8)
        screen.blit(font.render('king', True, 'black'), (king_center_x - 20, king_center_y + 10))
        pygame.draw.circle(screen, color, (rook_center_x, rook_center_y), 8)
        screen.blit(font.render('rook', True, 'black'), (rook_center_x - 20, rook_center_y + 10))
        pygame.draw.line(screen, color, (king_center_x, king_center_y), (rook_center_x, rook_center_y), 2)


# add pawn promotion
def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = None
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index


def draw_promotion():
    # Define promotion area dimensions
    promo_width = 200
    promo_height = 420
    promo_x = board_x + board_width + 20
    promo_y = board_y

    pygame.draw.rect(screen, 'dark gray', [promo_x, promo_y, promo_width, promo_height])

    if white_promote:
        color = 'white'
        for i, piece in enumerate(white_promotions):
            image = white_images[piece]
            image_rect = image.get_rect()
            image_x = promo_x + (promo_width - image_rect.width) / 2
            image_y = promo_y + 10 + i * (image_rect.height + 10)
            screen.blit(image, (image_x, image_y))
    elif black_promote:
        color = 'black'
        for i, piece in enumerate(black_promotions):
            image = black_images[piece]
            image_rect = image.get_rect()
            image_x = promo_x + (promo_width - image_rect.width) / 2
            image_y = promo_y + 10 + i * (image_rect.height + 10)
            screen.blit(image, (image_x, image_y))

    pygame.draw.rect(screen, color, [promo_x, promo_y, promo_width, promo_height], 8)


def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]

    promo_width = 200
    promo_height = 420
    promo_x = board_x + board_width + 20
    promo_y = board_y

    if left_click:
        if promo_x <= mouse_pos[0] <= promo_x + promo_width and promo_y <= mouse_pos[1] <= promo_y + promo_height:
            relative_y = mouse_pos[1] - promo_y
            piece_height = 80  # Adjust based on your image sizes
            index = int(relative_y // piece_height)
            if white_promote:
                if 0 <= index < len(white_promotions):
                    white_pieces[promo_index] = white_promotions[index]
                    white_promote = False
            elif black_promote:
                if 0 <= index < len(black_promotions):
                    black_pieces[promo_index] = black_promotions[index]
                    black_promote = False


# main game loop
if __name__ == "__main__":
    pygame.init()
    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')
    run = True
    while run:
        timer.tick(fps)
        if counter < 30:
            counter += 1
        else:
            counter = 0
        screen.fill('dark gray')
        draw_board()
        draw_pieces()
        draw_captured()
        draw_check()
        if not game_over:
            white_promote, black_promote, promo_index = check_promotion()
            if white_promote or black_promote:
                draw_promotion()
                check_promo_select()
        if selection is not None:
            valid_moves = check_valid_moves()
            draw_valid(valid_moves)
            if selected_piece == 'king':
                draw_castling(castling_moves)
        else:
            valid_moves = []
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                mouse_x, mouse_y = event.pos
                if board_x <= mouse_x < board_x + board_width and board_y <= mouse_y < board_y + board_height:
                    x_coord = int((mouse_x - board_x) // square_size)
                    y_coord = int((mouse_y - board_y) // square_size)
                    click_coords = (x_coord, y_coord)
                    if turn_step <= 1:

                        if forfeit_button_rect.collidepoint(mouse_x, mouse_y):
                            winner = 'black'

                        if click_coords in white_locations:
                            selection = white_locations.index(click_coords)
                            selected_piece = white_pieces[selection]
                            if turn_step == 0:
                                turn_step = 1
                        else:
                            selection = None  # Deselect if click is not on a piece
                        if click_coords in valid_moves and selection is not None:
                            white_ep = check_ep(white_locations[selection], click_coords)
                            white_locations[selection] = click_coords
                            white_moved[selection] = True
                            if click_coords in black_locations:
                                black_piece = black_locations.index(click_coords)
                                captured_pieces_white.append(black_pieces[black_piece])
                                if black_pieces[black_piece] == 'king':
                                    winner = 'white'
                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)
                                black_moved.pop(black_piece)
                            # adding check if en passant pawn was captured
                            if black_ep is not None and click_coords == black_ep:
                                black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                                captured_pieces_white.append(black_pieces[black_piece])
                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)
                                black_moved.pop(black_piece)
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 2
                            selection = None
                            valid_moves = []
                        # add option to castle
                        elif selection is not None and selected_piece == 'king':
                            for q in range(len(castling_moves)):
                                if click_coords == castling_moves[q][0]:
                                    white_locations[selection] = click_coords
                                    white_moved[selection] = True
                                    if click_coords == (1, 0):
                                        rook_coords = (0, 0)
                                    else:
                                        rook_coords = (7, 0)
                                    rook_index = white_locations.index(rook_coords)
                                    white_locations[rook_index] = castling_moves[q][1]
                                    black_options = check_options(black_pieces, black_locations, 'black')
                                    white_options = check_options(white_pieces, white_locations, 'white')
                                    turn_step = 2
                                    selection = None
                                    valid_moves = []
                    if turn_step > 1:
                        if forfeit_button_rect.collidepoint(mouse_x, mouse_y):
                            winner = 'white'

                        if click_coords in black_locations:
                            selection = black_locations.index(click_coords)
                            # check what piece is selected, so you can only draw castling moves if king is selected
                            selected_piece = black_pieces[selection]
                            if turn_step == 2:
                                turn_step = 3
                        if click_coords in valid_moves and selection is not None:
                            black_ep = check_ep(black_locations[selection], click_coords)
                            black_locations[selection] = click_coords
                            black_moved[selection] = True
                            if click_coords in white_locations:
                                white_piece = white_locations.index(click_coords)
                                captured_pieces_black.append(white_pieces[white_piece])
                                if white_pieces[white_piece] == 'king':
                                    winner = 'black'
                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece)
                                white_moved.pop(white_piece)
                            if click_coords == white_ep:
                                white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                                captured_pieces_black.append(white_pieces[white_piece])
                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece)
                                white_moved.pop(white_piece)
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 0
                            selection = None
                            valid_moves = []
                        # add option to castle
                        elif selection is not None and selected_piece == 'king':
                            for q in range(len(castling_moves)):
                                if click_coords == castling_moves[q][0]:
                                    black_locations[selection] = click_coords
                                    black_moved[selection] = True
                                    if click_coords == (1, 7):
                                        rook_coords = (0, 7)
                                    else:
                                        rook_coords = (7, 7)
                                    rook_index = black_locations.index(rook_coords)
                                    black_locations[rook_index] = castling_moves[q][1]
                                    black_options = check_options(black_pieces, black_locations, 'black')
                                    white_options = check_options(white_pieces, white_locations, 'white')
                                    turn_step = 0
                                    selection = None
                                    valid_moves = []
                else:
                    # Handle clicks outside the board (e.g., promotion selection)
                    check_promo_select()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    winner = ''
                    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    white_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    black_moved = [False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False]
                    captured_pieces_white = []
                    captured_pieces_black = []
                    turn_step = 0
                    selection = None
                    valid_moves = []
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

        if winner != '':
            game_over = True
            draw_game_over()

        pygame.display.flip()
    pygame.quit()


# Initialize options
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')