import math

# 0 empty, -1 human, 1 computer
board = [[0]*7 for i in range(6)]
index = [0,0,0,0,0,0,0]

#def hueristic

def applyMove(board,index ,row ,col, turn):
    index = index.copy()
    index[col] +=1
    if turn:
        player = 1
    else:
        player = -1
        
    board = [r[:] for r in board]
    board[row][col] = player
    return board,index


#still needs most stuff
def minMax(board, index ,alpha, beta, depth,turn):
    
    if depth == 0 or index == [6,6,6,6,6,6,6]:
        return hueristic(board), None
    
    if turn:
        allMax = -math.inf
        col = 0
        
        for c ,r in enumerate(index):
            if r > 5:
                continue
            newBoard,newIndex = applyMove(board, index, r , c ,turn)
            stepMax, _ = minMax(newBoard,newIndex, alpha, beta ,depth -1 ,not turn)
            if stepMax > allMax:
                col = c
                allMax = stepMax
            alpha = max(alpha, allMax)
            if beta <= alpha:
                break
            
        return allMax ,col 
    
    else:
        allMin = math.inf
        col = 0
        
        for c ,r in enumerate(index):
            if r>5:
                continue
            newBoard,newIndex = applyMove(board, index, r, c, turn)
            stepMin,_ = minMax(newBoard, newIndex, alpha, beta, depth-1, not turn)
            if stepMin < allMin:
                col = c
                allMin = stepMin
            beta = min(beta ,allMin)
            if beta <= alpha:
                break
            
        return allMin ,col
    
    
def scanWindow(board,direction1,direction2, row ,col): #00 = horizontal /01 = vertical /10 = diag right /11 = diag left (enter 2 arbitary values)
    if not direction1 and  not direction2:
        r = 0
        c = 1
    if not direction1 and  direction2:
                r = 1
                c = 0
    if direction1 and  not direction2:
                r = 1
                c = 1
    if direction1 and direction2:
                r = 1
                c = -1
    if not (row + 3*r) < 6 or not 0<=(col +3*c)<7:
        return None
    
    empty = 0
    owner = 0                      #0 = not assingned yet
    consicutive = False
    prevElement = None
    for i in range(4):
        element = board[row + r*i][col + c*i]
        if element == prevElement and element != 0:
            consicutive = True
        
        if element == 0:
            empty +=1
            
        elif owner == 0:
            owner = element
        
        elif element != owner:
            return None
        
        prevElement = element
    score = 4-empty
    return consicutive ,score, owner
            