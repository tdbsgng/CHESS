red, black = 0, 1 #row 0~4 red  row 5~9 black 
go , eat = 0, 1
def is_valid_position(target):
    return target[0] in range(10) and target[1] in range(9)

def is_in_palace(target,color):
    return target[1] in (3,4,5) and ((target[0] in (0,1,2) and color==black) or (target[0] in (7,8,9) and color == red))

def is_empty(board,target):
    return board[target[0]][target[1]] == None

def is_pass_border(piece,row):
    return row > 4 if piece.color == red else row <= 4

class pieces:
    def __init__(self,row,col,color,board) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.board = board    
    def is_same_positioin(self,target):
        return (self.row,self.col) == target

class general(pieces):
    def is_valid(self, target,action):
        return is_valid_position(target) and is_in_palace(target, self.color) and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 1)\
            and not self.is_same_positioin(target)
    def __repr__(self) -> str:
        return "帥" if self.color == red else "將"

class guard(pieces):
    def is_valid(self, target,action):
        return is_valid_position(target) and is_in_palace(target, self.color) and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 2)\
            and not self.is_same_positioin(target)
    def __repr__(self) -> str:
        return "仕" if self.color == red else "士"

class elephant(pieces):
    def is_valid(self, target,action):
        # 拐象腳 #不能過河
        return is_valid_position(target) and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 8)\
            and is_empty(self.board,((target[0]+self.row)//2,(target[1]+self.col)//2)) and not self.is_same_positioin(target)\
            and not is_pass_border(self,target[0])
    def __repr__(self) -> str:
        return "相" if self.color == red else "象"
 
class knight(pieces):
    def is_valid(self, target,action):
        if is_valid_position(target) and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 5) and not self.is_same_positioin(target):
            if (target[0]-self.row) in [2,-2]: #直的
                return is_empty(self.board,((target[0]+self.row)//2,self.col))         # 拐馬腳
            else: # 橫的
                return is_empty(self.board,((target[1]+self.col)//2,self.col))
        else:
            return False
    def __repr__(self) -> str:
        return "傌" if self.color == red else "馬"
class rook(pieces):
    def is_valid(self, target,action):
        if is_valid_position(target)and (target[0] == self.row or target[1] == self.col) and not self.is_same_positioin(target):
            if target[0] == self.row: #橫的
                col_range = range(self.col+1,target[1]) if target[1]>self.col else range(self.col-1,target[1],-1)
                for col in col_range:
                    if not is_empty(self.board,(self.row,col)):
                        return False
                return True
            else: #直的
                row_range = range(self.row+1,target[0]) if target[0]>self.row else range(self.row-1,target[0],-1)
                for row in row_range:
                    if not is_empty(self.board,(row,self.col)):
                        return False
                return True
        else:
            return False
    def __repr__(self) -> str:
        return "俥" if self.color == red else "車"  
class cannon(pieces): #需要考慮action
    def is_valid(self, target,action):
        if action == go:
            return rook.is_valid(self,target,action)
        if is_valid_position(target) and (target[0] == self.row or target[1] == self.col) and not self.is_same_positioin(target):
            if target[0] == self.row: #橫的
                col_range = range(self.col+1,target[1]) if target[1]>self.col else range(self.col-1,target[1],-1)
                count = 0
                for col in col_range:
                    if not is_empty(self.board,(self.row,col)):
                        count += 1
                return True if count == 1 else False
            else: #直的
                row_range = range(self.row+1,target[0]) if target[0]>self.row else range(self.row-1,target[0],-1)
                count = 0
                for row in row_range:
                    if not is_empty(self.board,(row,self.col)):
                        count +=1
                return True if count == 1 else False
        else:
            return False
    def __repr__(self) -> str:
        return "炮" if self.color == red else "包"

class soldier(pieces):
    def is_valid(self, target,action):
        if is_pass_border(self,self.row): #可左右
            return is_valid_position(target) and not self.is_same_positioin(target) \
                and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 1) \
                and not ((target[0]-self.row) == -1 if self.color == red else (target[0]-self.row) == 1)
        else: #只會往前
            return is_valid_position(target) and not self.is_same_positioin(target) \
                and target[1] == self.col and ((target[0]-self.row) == 1 if self.color == red else (target[0]-self.row) ==-1)
    def __repr__(self) -> str:
        return "兵" if self.color == red else "卒"

def initialize():
    board = [[None for _ in range(9)] for _ in range(10)]
    board[0][0],board[0][1], board[0][2], board[0][3],board[0][4],board[0][5], board[0][6],board[0][7],board[0][8] \
    = rook(0,0,red,board),knight(0,1,red,board),elephant(0,2,red,board),guard(0,3,red,board),general(0,4,red,board),\
    guard(0,5,red,board),elephant(0,6,red,board),knight(0,7,red,board),rook(0,8,red,board)
    
    board[9][0],board[9][1], board[9][2], board[9][3],board[9][4],board[9][5], board[9][6],board[9][7],board[9][8] \
    = rook(9,0,black,board),knight(9,1,black,board),elephant(9,2,black,board),guard(9,3,black,board),general(9,4,black,board),\
    guard(9,5,black,board),elephant(9,6,black,board),knight(9,7,black,board),rook(9,8,black,board) 

    for col in [0,2,4,6,8]:
        board[3][col] = soldier(3,col,red,board)
        board[6][col] = soldier(6,col,black,board)
    board[2][1],board[2][7] = cannon(2,1,red,board),cannon(2,7,red,board)
    board[7][1],board[7][7] = cannon(7,1,black,board),cannon(7,7,black,board)
    return board    


def showboard(board, dead_pieces):
    print("    0   1   2   3   4   5   6   7   8 ")
    for row in range(len(board)):
        print(str(row)+"  ",end="")
        for col in range(len(board[0])):
            if board[row][col] == None:
                print("    ",end="")
            else:
                print(f" {board[row][col]} ",end="")
        print("")
    red_dead_pieces = []
    black_dead_pieces = []
    for piece in dead_pieces:
        if piece.color == red:
            red_dead_pieces.append(piece)
        else:
            black_dead_pieces.append(piece)
    print(f"\nRed dead pieces: {red_dead_pieces}")
    print(f"Black dead pieces: {black_dead_pieces}")

def arm_perform(source,target,action):
    pass

def is_checkmate(board):
    return False
def test_valid_action(piece):
    pass