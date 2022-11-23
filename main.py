from utils import *

red, black = 0, 1
go , eat = 0, 1

dead_pieces = []
board = initialize()

def main():
    showboard(board,dead_pieces)
    turn = black
    while True:
        try:
            turn_str = "Black"  if turn == black else "Red"
            command = input(f"\n{turn_str} turn!\nKey in the action in following format\nsource_row, source_col, action, target_row, target_col:")
            source_row, source_col, action, target_row, target_col = eval(command)
            source = source_row, source_col
            target = target_row, target_col
        except:
            if command in ["q","Q"]:
                print("Quit game!")
                return
            print("Invalid format!")
            continue
        if perform(source,target,action,turn):
            showboard(board,dead_pieces)
            turn = 1 - turn
def perform(source,target,action,turn):
    source_piece = board[source[0]][source[1]]
    if source_piece == None:
        print("Invalid action, there is no piece to move!")
        return False
    if turn != source_piece.color:
        print("Invalid action, you can only move your pieces!")
        return False
    if not source_piece.is_valid(target,action):
        print(f"Invalid action, {source_piece} can't arrive the target!")
        return False
    if action == eat:
        if board[target[0]][target[1]] == None:
            print("Invalid action, there is no piece to eat!")
            return False
        if board[target[0]][target[1]].color == source_piece.color:
            print("Invalid action, you can't eat your ally!")
            return False
    else:
        if not is_empty(board,target):
            print("Invalid action, the target position is not empty!")
            return False
    #arm_perform(source,target,action) # robot arm perform the task
    if action == eat:
        dead_pieces.append(board[target[0]][target[1]])    
    board[source[0]][source[1]] = None
    board[target[0]][target[1]] = source_piece
    source_piece.row, source_piece.col = target[0],target[1]
    if is_checkmate(board):
        print("************checkmate!*************")
    return True
if __name__ == "__main__":
    main()