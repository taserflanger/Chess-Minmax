from stds import Vector
from copy import deepcopy

class Piece():
    def __init__(self, value, position, color):
        self.value = value
        self.position = position
        self.color = color
        self.dead = False
        if color == "whites":
            self.otherColor="blacks"
        else:
            self.otherColor="whites"
    @classmethod
    def getPossibleMoves(self, grid, testing=False):
        raise NotImplementedError
    @classmethod
    def getName(self):
        raise NotImplementedError
    @staticmethod
    def getMovesInDirection(self, direction, friendPositions, grid, testing):
        moves = []
        factor = 1
        position = self.position + direction.__mul__(factor)
        noEnnemyPiece = True
        while (not position in friendPositions) and noEnnemyPiece and position.isInBoard():
            for piece in grid[self.otherColor]:
                if piece.position == position:
                    move = Move(self, position, targetPiece=piece)
                    moves.append(move)
                    noEnnemyPiece = False
            if noEnnemyPiece:
                move = Move(self, position)
                if not testing:
                    #check for check to see if move is valid (check)
                    if not Move.isInCheck(move, grid, self.color, self.otherColor):
                        moves.append(move)
                else:
                    moves.append(move)
                factor+=1
                position = self.position + direction.__mul__(factor)
        return moves

    def __repr__(self):
        return type(self).__name__ + " on {}".format(str(self.position))
class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__(1, position, color)
    def getPossibleMoves(self, grid, testing=False):
        moves = []
        coefficient = 1 if self.color=="blacks" else -1
        secondCase = self.position.y == coefficient % 7
        # on teste si le pion est sur sa ligne d'origine
        frontCase = True
        for piece in grid[self.color]+grid[self.otherColor]:
            if piece.position==self.position+Vector(0, coefficient):
                frontCase = False
            if secondCase and piece.position==self.position+Vector(0, 2*coefficient):
                secondCase = False
        for piece in grid[self.otherColor]:
                for newPos in [self.position + i for i in (Vector(1, coefficient), Vector(-1, coefficient))]:
                    if piece.position==newPos:
                        move = Move(self, newPos, targetPiece=piece)
                        if not testing:
                            if not Move.isInCheck(move, grid, self.color, self.otherColor):
                                moves.append(move)
                        else:
                            moves.append(move)
        if frontCase:
            move = Move(self, self.position+Vector(0, coefficient))
            if not testing:
                if not Move.isInCheck(move, grid, self.color, self.otherColor):
                    moves.append(move)
            else:
                moves.append(move)
        if secondCase:
            move = Move(self, self.position+Vector(0, 2*coefficient))
            if not testing:
                if not Move.isInCheck(move, grid, self.color, self.otherColor):
                    moves.append(move)
            else:
                moves.append(move)
        return moves
    def getName(self):
        return "p"
class Rook(Piece):
    def __init__(self, position, color):
        super().__init__(5, position, color)
    def getPossibleMoves(self, grid, testing=False):
        moves = []
        friendPositions = [piece.position for piece in grid[self.color]]
        for direction in [Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)]:
            factor = 1
            position = self.position + direction.__mul__(factor)
            noEnnemyPiece = True
            while (not position in friendPositions) and noEnnemyPiece and position.isInBoard():
                for piece in grid[self.otherColor]:
                    if piece.position == position:
                        moves.append(Move(self, position, targetPiece=piece))
                        noEnnemyPiece = False
                if noEnnemyPiece:
                    move = Move(self, position)
                    if not testing:
                        if not Move.isInCheck(move, grid, self.color, self.otherColor):
                            moves.append(move)
                    else:
                        moves.append(move)
                    factor+=1
                    position = self.position + direction.__mul__(factor)
        return moves

            
    def getName(self):
        return "r"
class Queen(Piece):
    def __init__(self, position, color):
        super().__init__(10, position, color)
    def getPossibleMoves(self, grid, testing=False):
        moves = []
        friendPositions = [piece.position for piece in grid[self.color]]
        for direction in [Vector(1, 1), Vector(-1, 1), Vector(-1, -1), Vector(1, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)]:
            moves += self.getMovesInDirection(self, direction, friendPositions, grid, testing)
        return moves
    def getName(self):
        return "q"
class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(3, position, color)
    def getPossibleMoves(self, grid, testing=False):
        moves = []
        friendPositions = [piece.position for piece in grid[self.color]]
        for direction in [Vector(1, 1), Vector(-1, 1), Vector(-1, -1), Vector(1, -1)]:
            moves += self.getMovesInDirection(self, direction, friendPositions, grid, testing)
        return moves

    
            
    def getName(self):
        return "b"
class Knight(Piece):
    def __init__(self, position, color):
        super().__init__(3, position, color)
    def getPossibleMoves(self, grid, testing=False):
        moves = []
        friendPositions = [piece.position for piece in grid[self.color]]
        for (x, y) in [(2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2)]:
            offset = Vector(x, y)
            newPos = self.position + offset
            if not newPos in friendPositions and newPos.isInBoard():
                taking = False
                move = None
                for piece in grid[self.otherColor]:
                    if piece.position == newPos:
                        taking = True
                        move = Move(self, newPos, targetPiece=piece)
                        break
                if not taking:
                    move = Move(self, newPos)
                if not testing:
                    if not Move.isInCheck(move, grid, self.color, self.otherColor):
                        moves.append(move)
                else:
                    moves.append(move)
        return moves

    def getName(self):
        return "n"
class King(Piece):
    def __init__(self, position, color):
        super().__init__(10000000000000, position, color)
    def getPossibleMoves(self, grid, testing=False):
        moves = []
        friendPositions = [piece.position for piece in grid[self.color]]
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x==y==0:
                    continue
                offset = Vector(x, y)
                newPos = self.position + offset
                if not newPos in friendPositions:
                    taking = False
                    move = None
                    for piece in grid[self.otherColor]:
                        if piece.position == newPos:
                            taking = True
                            move = Move(self, newPos, targetPiece=piece)
                            break
                    if not taking:
                        move = Move(self, newPos)
                    if not testing:
                        if not Move.isInCheck(move, grid, self.color, self.otherColor):
                            moves.append(move)
                        # check if king in possible target pieces
                    else:
                        moves.append(move)
        return moves
    def getName(self):
        return "k"
class Move():
    def __init__(self, piece, target, targetPiece=None):
        self.piece = piece
        self.target = target
        self.name = self.getMoveName()
        self.targetPiece = targetPiece
    @staticmethod
    def ParseMove(move, grid, color):
        # Parses a move (ex be6) into a *Move* instance
        piecesDict = {"p": Pawn, "r": Rook, "b": Bishop, "q": Queen, "k": King, "n": Knight, "any": Piece}
        if len(move)==3:
            piecePlayed = move[0]
            if piecePlayed not in piecesDict.keys():
                print(Warning("Piece not correct..."))
                return False
            x = ord(move[1])-97
            y = 8-int(move[2])
        elif len(move)==2:
            x = ord(move[0])-97
            y = 8-int(move[1])
            piecePlayed = "any"
        else:
            print(Warning("Please specify the piece you are moving (ex: pe4)"))
            return False
        adequatMoves = []
        for piece in grid[color]:
            if type(piece) == piecesDict[piecePlayed] or piecePlayed == "any":
                for possibleMove in piece.getPossibleMoves(grid):
                    if Vector(x, y) == possibleMove.target:
                        adequatMoves.append(possibleMove)
        if len(adequatMoves) == 1:
            return adequatMoves[0]
        elif len(adequatMoves) == 0:
            print(Warning("No such piece can go to {}".format(move[1:])))
            return False
        else:
            if len(move)==2:
                print(Warning("Multiple pieces can go to {}, please specify which type of piece you are moving".format(move)))
                return False
            else:
                print(Warning("Multiple pieces can go to {}, taking a random one (possibility of chosing which file is not yet implemented)".format(move[1:])))
                return adequatMoves[0]
        
    @staticmethod
    def isInCheck(move, grid, color, otherColor):
        #checks if the otherColor puts the color in check
        newGrid, newMove = Move.transferMoveToNewGrid(grid, move)
        newGrid = newMove.apply(newGrid)
        for piece in newGrid[otherColor]:
            possibleMoves = piece.getPossibleMoves(newGrid, testing=True)
            for move in possibleMoves:
                if type(move.targetPiece)==King:
                    return True
        del newGrid, newMove
        return False

    @staticmethod
    def transferMoveToNewGrid(grid, move):
        newGrid = deepcopy(grid)
        [piece] = [p for p in newGrid[move.piece.color] if p.position == move.piece.position]
        if move.targetPiece == None:
            targetPiece = None
        else:
            [targetPiece] = [p for p in newGrid[move.targetPiece.color] if p.position == move.targetPiece.position]
        newMove = Move(piece, move.target, targetPiece)
        return newGrid, newMove
    def __repr__(self):
        return self.getMoveName()
    def getMoveName(self):
        return "{}{}{}".format(self.piece.getName(), chr(self.target.x+97), str(8-self.target.y))
    def apply(self, grid):
        self.piece.position=self.target
        if self.targetPiece!=None:
            self.targetPiece.dead = True
            print(str(self.targetPiece) + "is Dead")
            grid[self.targetPiece.color].remove(self.targetPiece)
        return grid