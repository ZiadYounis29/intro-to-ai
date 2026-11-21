import math

BASE =4
FOUR_WEIGHT = 1500
MAXDEPTH = None
Nodes = list()

# 0 empty, -1 human, 1 computer
board = [[0]*7 for i in range(6)]
index = [0,0,0,0,0,0,0]


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
def minMax(board, index ,alpha, beta, depth,turn,column):
    
    if depth == 0 or index == [6,6,6,6,6,6,6]:
        value = heuristic(board)
        Nodes.append(( MAXDEPTH - depth, column, value , alpha, beta, 0 ))
        return value, None
    
    if turn:
        allMax = -math.inf
        col = 0
        nPrune = 0
        for c ,r in enumerate(index):
            if r > 5:
                continue
            newBoard,newIndex = applyMove(board, index, r , c ,turn)
            stepMax, _ = minMax(newBoard,newIndex, alpha, beta ,depth -1 ,not turn,c)
            if stepMax > allMax:
                col = c
                allMax = stepMax
            alpha = max(alpha, allMax)
            if beta <= alpha:
                nPrune = sum(1 for c2 in range(c+1 ,7) if index[c2] <=5 )                
                break

        Nodes.append(( MAXDEPTH - depth, column, allMax , alpha, beta, nPrune ))
        return allMax ,col 
    
    else:
        allMin = math.inf
        col = 0
        nPrune = 0
        for c ,r in enumerate(index):
            if r>5:
                continue
            newBoard,newIndex = applyMove(board, index, r, c, turn)
            stepMin,_ = minMax(newBoard, newIndex, alpha, beta, depth-1, not turn, c)
            if stepMin < allMin:
                col = c
                allMin = stepMin
            beta = min(beta ,allMin)
            if beta <= alpha:
                nPrune = sum(1 for c2 in range(c+1 ,7) if index[c2] <=5 )
                break

        Nodes.append(( MAXDEPTH - depth, column, allMin , alpha, beta, nPrune ))
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
    consicutiveEmpty = False
    prevElement = None
    for i in range(4):
        element = board[row + r*i][col + c*i]
        if element == prevElement and element != 0:
            consicutive = True
            
        if element == prevElement and element == 0:
            consicutiveEmpty = True
        
        
        if element == 0:
            empty +=1
            
        elif owner == 0:
            owner = element
        
        elif element != owner:
            return None
        
        prevElement = element
  
    score = 4-empty
    if consicutive or not consicutiveEmpty:
        score +=1
        
    return score, owner #how scores are calculated  0: all empty , 1: 1 element , 2: two elements(cannot be connected) ex: x--x
                        # 3 two elements can be connected to be 3 ex: xx-- or x-x- , 4: 3 elements . 5: 4 elements
                        
def getBoardCounts(board):
    com = [0,0,0,0,0,0]
    human = [0,0,0,0,0,0]
    for i in range(6):
        for j in range(7):     
            for x in range(2): #x and y aributary for the directions
                for y in range(2):
                    result = scanWindow(board ,x,y,i,j)
                    if result == None:
                        continue
                    level, owner = result
                    if owner == 1:           
                        com[level] += 1
                    elif owner == -1:
                        human[level] += 1
    return com ,human

def heuristic(board):
    com , human = getBoardCounts(board)
    score = [ a - b for a,b in zip(com ,human)]
    for i in range(6):
        if i == 5:
            score[i] = score[i]*FOUR_WEIGHT
        else:
            score[i] = score[i]* BASE**i
    return sum(score)

def foursCount(board):
    com , human = getBoardCounts(board)
    return com[5] ,human[5]

    


#what next: 
#game loop
#gui
            