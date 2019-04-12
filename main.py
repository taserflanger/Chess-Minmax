import asyncio
from piece import Pawn, Rook, Bishop, Queen , Knight, King, Move
from stds import Vector
event_loop = asyncio.get_event_loop()
# async def askForPosition():
#     await input("Your turn: ")
# async def calculateBestMove(grid):
#     asyncio.sleep(1)
#     await Move(grid["whites"][0], Vector(0, 3))
# tasks = [
#     asyncio.create_task(askForPosition),
#     asyncio.create_task(calculateBestMove)
# ]
# loop.run_until_complete(asyncio.wait(tasks))  
# loop.close()

colors = ["whites", "blacks"]
userColor="whites"
aiColor="blacks"

def printGrid(grid):
    result = [[". " for i in range(8)] for i in range(8)]
    for (prefix, color) in zip(["w", "b"], ["whites", "blacks"]):
        for piece in grid[color]:
            pos = piece.position
            result[pos.y][pos.x] = prefix + piece.getName()
    for y in range(8):
        print(str(8-y) + "   " + " ".join(result[y]))
    print("\n    a  b  c  d  e  f  g  h")

def getBestMoveFor(color, grid):
    pass

def main():
    checkmate = False
    # userColor = input("whites/blacks? ")
    turn = 0
    grid = generateGrid()
    printGrid(grid)
    while not checkmate:
        if userColor==colors[turn]:
            move=False
            while not move:
                move=input("Your turn: ")
                move=Move.ParseMove(move, grid, colors[turn])
            grid=move.apply(grid)
            printGrid(grid)
        else:
            move, value = minmax(turn, grid, 2)
            print(move, value)
        turn = 1-turn


def minmax(turn, node, depth):
    if depth == 0:
        return None, gridValue(node)
    else:
        if colors[turn]==userColor:
            for piece in node[userColor]:
                possibleMoves = piece.getPossibleMoves(node)
                bestChild = [None, 100000000]
                for move in possibleMoves:
                    childGrid, mappedMove = Move.transferMoveToNewGrid(node, move)
                    childGrid = mappedMove.apply(childGrid)
                    _, value = minmax(1-turn, childGrid, depth-1)
                    if value < bestChild[1]:
                        bestChild = [move, value]
                return bestChild
        if colors[turn] == aiColor:
            for piece in node[aiColor]:
                possibleMoves = piece.getPossibleMoves(node)
                bestChild = [None, -100000000]
                for move in possibleMoves:
                    childGrid, mappedMove = Move.transferMoveToNewGrid(node, move)
                    childGrid = mappedMove.apply(childGrid)
                    _, value = minmax(1-turn, childGrid, depth-1)
                    if value > bestChild[1]:
                        bestChild = [move, value]
                return bestChild


def gridValue(grid):
    total = 0
    for piece in grid[userColor]:
        total -= piece.value
    for piece in grid[aiColor]:
        total += piece.value
    return total

def generateGrid():
    return {"whites":
        [Pawn(Vector(i, 6), "whites") for i in range(8)]
        + [Rook(Vector(0, 7), "whites"), Rook(Vector(7, 7), "whites")]
        + [Bishop(Vector(2, 7), "whites"), Bishop(Vector(5, 7), "whites")]
        + [Queen(Vector(3, 7), "whites")]
        + [Knight(Vector(1, 7), "whites"), Knight(Vector(6, 7), "whites")]
        + [King(Vector(4, 7), "whites")],
        "blacks":
        [Pawn(Vector(i, 1), "blacks") for i in range(8)]
        + [Rook(Vector(0, 0), "blacks"), Rook(Vector(7, 0), "blacks")]
        + [Bishop(Vector(2, 0), "blacks"), Bishop(Vector(5, 0), "blacks")]
        + [Queen(Vector(3, 0), "blacks")]
        + [Knight(Vector(1, 0), "blacks"), Knight(Vector(6, 0), "blacks")]
        + [King(Vector(4, 0), "blacks")]
    }

if __name__ == "__main__":
    main()