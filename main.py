from utils import *

red, black = 0, 1
go , eat = 0, 1

board,dead_pieces, alive_pieces = initialize()

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
            #print(alive_pieces)
            showboard(board,dead_pieces)
            turn = 1 - turn
def perform(source,target,action,turn):
    source_piece = board[source[0]][source[1]]
    #invalid action
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
    #need to check whether the action will cause yourself be checkmated
    if is_checkmate(alive_pieces,turn,source_piece,target):
        print("Invalid action, that will make you checkmated!")
        return False
    #valid action
    if action == eat:
        alive_pieces[board[target[0]][target[1]].color].remove(board[target[0]][target[1]])
        dead_pieces[board[target[0]][target[1]].color].append(board[target[0]][target[1]])    
    board[source[0]][source[1]] = None
    board[target[0]][target[1]] = source_piece
    source_piece.row, source_piece.col = target[0],target[1]
    #arm_perform(source,target,action) # robot arm perform the task
    if is_checkmate(alive_pieces,turn):
        print("****************************************************check!****************************************************")
        if is_gameover(alive_pieces,turn):
            print(f"Game over, {'Red' if not turn else 'Black'} win!")
    return True
if __name__ == "__main__":
    main()