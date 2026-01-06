# logic.py

DIRECTIONS = [
    (1, 0),   # right
    (0, 1),   # down
    (1, 1),   # diagonal \
    (1, -1),  # diagonal /
]

def new_board(size_x: int, size_y: int):
    """Return empty size x size board."""
    board = []
    for _ in range(size_y):
        board.append(size_x * [""])

    return board


def is_valid_move(board: list[list[str]], x: int, y: int):
    """Return True if move is inside board and cell is empty."""
    if 0 <= y < len(board) and 0 <= x < len(board[0]):

        return board[y][x] == ""
    else: return False


def apply_move(board: list[list[str]], x: int, y: int, player: str):
    """Place player symbol on the board."""
    board[y][x] = player
        

def _count_line(board: list[list[str]], x: int, y: int, dx: int, dy: int, player: str):
    """Count contiguous stones in one line."""
    if board[y][x] != player:
        return 0, None

    score = 1
    temp_x = x
    temp_y = y
    coordinates = [(temp_x, temp_y)]

    for direction in [(dx, dy), (-dx, -dy)]:
        while True:
            if 0 <= temp_x+direction[0] < len(board[0]) and 0 <= temp_y+direction[1] < len(board): #test if in board range
                temp_x += direction[0]
                temp_y += direction[1]
                if board[temp_y][temp_x] == player:
                    score += 1
                    coordinates.append((temp_x, temp_y))
                else: break
            else: break
        
        temp_x = x
        temp_y = y
    
    return score, coordinates
            

def is_win(board: list[list[str]], x: int, y: int, player: str, win_len: int):
    """Check win condition from last move."""
    for direction in DIRECTIONS:
        result = _count_line(board, x, y, direction[0], direction[1], player)
        if result[0] >= win_len:
            
            return True, result[1]
    return False, None