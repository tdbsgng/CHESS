red, black = 0, 1 

def is_valid_position(row,col):
    return row in range(10) and col in range(9)

def is_in_palace(row,col,color):
    return col in (3,4,5) and ((row in (0,1,2) and color==black) or (row in (7,8,9) and color == red))

def is_empty(board,row,col):
    return board[row][col] == None
class pieces:
    def __init__(self,row,col,color,board) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.board = board    

class general(pieces):
    def is_valid(self, target):
        return is_in_palace(target[0], target[1], self.color) and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 1) 

class guard(pieces):
    def is_valid(self, target):
        return is_in_palace(target[0], target[1], self.color) and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 2)

class elephant(pieces):
    def is_valid(self, target):
        # 拐象腳
        return is_valid_position(target[0],target[1]) and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 8)\
            and is_empty(self.board,(target[0]+self.row)//2,(target[1]+self.col)//2)
 
class knight(pieces):
    def is_valid(self, target):
        # 拐馬腳
        return is_valid_position(target[0],target[1]) and ((target[0]-self.row)**2+(target[1]-self.col)**2 == 10)\
            and  

class rook(pieces):
    def is_valid(self, target):
        pass

class cannon(pieces):
    def is_valid(self, target):
        pass

class soldier(pieces):
    def is_valid(self, target):
        if self.color == red:
            if self.row <= 4: #over border
                
            else:

        else:
            pass

class board():
    def __init__(self):
        pass

def test_valid_action(piece):
    pass