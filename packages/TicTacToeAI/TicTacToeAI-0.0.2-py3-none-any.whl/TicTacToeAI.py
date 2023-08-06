


# Constants for representing the players and empty cells
EMPTY = '-'
PLAYER = 'X'
COMPUTER = 'O'

def check_winner(board):
    # Check rows
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != " ":
            return row[0]

    # Check columns
    for col in range(len(board[0])):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    # Check for a tie
    if all(board[i][j] != " " for i in range(3) for j in range(3)):
        return "tie"

    return None

def make_move(board, row, col, player):
    if row < 0 or row >= 3 or col < 0 or col >= 3 or board[row][col] != " ":
        return False
    board[row][col] = player
    return True

# function to make move
def get_best_move(board):
    best_score = float("-inf")
    best_move = None
    for cell in get_empty_cells(board):
        row, col = cell
        board[row][col] = "X"
        score = minimax(board, 0, False)
        board[row][col] = " "
        if score > best_score:
            best_score = score
            best_move = cell
    return best_move

# Function to print the game board
def print_board(board):
    print("-------------")
    for i in range(3):
        print("|", end=" ")
        for j in range(3):
            print(board[i][j], end=" ")
            print("|", end=" ")
        print("\n-------------")

def get_empty_cells(board):
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                empty_cells.append((i, j))
    return empty_cells

# function to minmax
def minimax(board, depth, maximizing_player):
    scores = {
        "X": 1,
        "O": -1,
        "tie": 0
    }

    result = check_winner(board)
    if result is not None:
        return scores[result]

    if maximizing_player:
        max_score = float("-inf")
        for cell in get_empty_cells(board):
            row, col = cell
            board[row][col] = "X"
            score = minimax(board, depth + 1, False)
            board[row][col] = " "
            max_score = max(max_score, score)
        return max_score
    else:
        min_score = float("inf")
        for cell in get_empty_cells(board):
            row, col = cell
            board[row][col] = "O"
            score = minimax(board, depth + 1, True)
            board[row][col] = " "
            min_score = min(min_score, score)
        return min_score

    
# function to play_game
def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic Tac Toe!")

    while True:
        print_board(board)
        row = int(input("Enter the row (0-2): "))
        col = int(input("Enter the column (0-2): "))

        if not make_move(board, row, col, "O"):
            print("Invalid move. Try again.")
            continue

        if check_winner(board) is not None:
            break

        print("AI is thinking...")
        ai_row, ai_col = get_best_move(board)
        make_move(board, ai_row, ai_col, "X")

        if check_winner(board) is not None:
            break

    print_board(board)
    result = check_winner(board)
    if result == "tie":
        print("It's a tie!")
    else:
        print("The winner is", result + "!")